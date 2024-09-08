import hashlib
import itertools
import numpy as np
import sys
import time
import re
import argparse
from typing import Optional
import string
from tqdm import tqdm

TAGS = {
    "<space>": " ",
    "<digits>": string.digits,
    "<symbols>": string.punctuation,
    "<englishlower>": string.ascii_lowercase,
    "<englishupper>": string.ascii_uppercase
}

def md5_hash(word: str, times: int) -> str:
    """Computes the MD5 hash for a given word, repeated `times` times."""
    hash_result = word
    for _ in range(times):
        hash_result = hashlib.md5(hash_result.encode('utf-8')).hexdigest()
    return hash_result

def replace_tags(text: str) -> str:
    """Replaces meta tags in the given text with their corresponding values in TAGS."""
    for tag, replacement in TAGS.items():
        text = text.replace(tag, replacement)
    return text

def generate_combinations_gpu(length: int, characters: str, start_char: Optional[str] = None) -> np.ndarray:
    """Generates all possible combinations of a given length on GPU.
    
    Args:
        length (int): Length of the combinations to generate.
        characters (str): Characters to use in combinations.
        start_char (Optional[str]): Character to start each combination with.

    Returns:
        np.ndarray: Array of generated combinations.
    """
    try:
        if start_char:
            if len(start_char) >= length:
                raise ValueError("start_char length must be less than target length")

            remaining_length = length - len(start_char)
            total_combinations = len(characters) ** remaining_length
            combinations = []

            for comb in tqdm(itertools.product(characters, repeat=remaining_length), total=total_combinations, desc="Generating combinations"):
                combinations.append(start_char + ''.join(comb))
        else:
            total_combinations = len(characters) ** length
            combinations = []
            
            for comb in tqdm(itertools.product(characters, repeat=length), total=total_combinations, desc="Generating combinations"):
                combinations.append(''.join(comb))
    except KeyboardInterrupt:
        user_input = input("Processing interrupted. Continue iteration with generated combinations? Y/N: ").strip().upper()
        if user_input == 'Y':
            return np.array(combinations, dtype=object)
        else:
            sys.exit(0)
        
    return np.array(combinations, dtype=object)

def find_word_from_combinations(target_hash: str, min_length: int, max_length: int, combinations: np.ndarray, max_collisions: int) -> None:
    """Finds the word corresponding to the given MD5 hash among the provided combinations.
    
    Args:
        target_hash (str): The MD5 hash to match.
        length (int): Length of the word combinations.
        combinations (np.ndarray): Array of word combinations to search through.
        max_collisions (int): Maximum number of times to hash MD5.
    """
    start_time = time.time()

    for word in tqdm(combinations, desc="Searching"):
        for num_collisions in range(1, max_collisions + 1):
            if md5_hash(word, num_collisions) == target_hash:
                end_time = time.time()
                print(f"\n==> Found: {word} with {num_collisions} collisions")
                print(f"==> Target: {target_hash} -> Source: {md5_hash(word, 1)} -> Decrypted: {word}")
                print(f"==> Execution time: {end_time - start_time:.2f} seconds")
                sys.exit(0)
    if min_length - max_length == 0:
        print("\n==> Word not found. Try using brute by dictionary or the --brute-collision parameter")
    else:
        print("Word not found, contiune with next length range")
    end_time = time.time()
    print(f"==> Execution time: {end_time - start_time:.2f} seconds")

def find_word(target_hash: str, min_length: int, max_length: int, characters: str, start_char: Optional[str] = None, word_list_file: Optional[str] = None, max_collisions: int = 1) -> None:
    """Finds the word corresponding to the given MD5 hash within a range of lengths or from a word list.
    
    Args:
        target_hash (str): The MD5 hash to match.
        min_length (int): Minimum length of the combinations to generate.
        max_length (int): Maximum length of the combinations to generate.
        characters (str): Characters to use in combinations.
        start_char (Optional[str]): Character to start each combination with.
        word_list_file (Optional[str]): File containing a list of words to check against.
        max_collisions (int): Maximum number of times to hash MD5.
    """
    if word_list_file:
        try:
            with open(word_list_file, 'r', encoding='utf-8') as file:
                combinations = [line.strip() for line in file]
        except FileNotFoundError:
            print(f"Word list file '{word_list_file}' not found.")
            return
        find_word_from_combinations(target_hash, np.array(combinations, dtype=object), max_collisions)
    else:
        for length in range(min_length, max_length + 1):
            print(f"Processing length: {length}")
            combinations_gpu = generate_combinations_gpu(length, characters, start_char)
            print("Total combinations:", len(combinations_gpu))
            
            find_word_from_combinations(target_hash, min_length, max_length, combinations_gpu, max_collisions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MD5 Hash Decryption using GPU")
    parser.add_argument('range', type=str, help="Range of lengths in format 'min-length-max-length' or integer")
    parser.add_argument('hash', type=str, help="MD5 hash to match")
    parser.add_argument('alphabet', type=str, help="Alphabet of characters to use")
    parser.add_argument('--start-char', type=str, default=None, help="Character to start each combination with")
    parser.add_argument('--word-list', type=str, default=None, help="File containing a list of words")
    parser.add_argument('--brute-collision', type=int, default=1, help="Maximum number of times to hash MD5")

    args = parser.parse_args()

    pattern = f"[{re.escape(string.punctuation + string.digits)}]"
    if re.search(pattern, args.alphabet) and not any(tag in args.alphabet for tag in TAGS):
        print(f"Note: You can use tags to specify character ranges: <digits>, <symbols>, <space>, <englishlower>, <englishupper>.\nFor example: python md5_decrypt_gpu.py {args.range} {args.hash} <digits><symbols>")

    args.alphabet = replace_tags(args.alphabet)

    if args.start_char:
        args.start_char = replace_tags(args.start_char)

    try:
        min_length, max_length = map(int, args.range.split('-'))
    except ValueError:
        min_length, max_length = int(args.range), int(args.range)

    find_word(args.hash, min_length, max_length, args.alphabet, args.start_char, args.word_list, args.brute_collision)

    input("Press Enter to exit...")
