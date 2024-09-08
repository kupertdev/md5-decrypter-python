# MD5 Decryptor with CPU Acceleration
GPU Coming Later

## Overview

This project is a Python-based MD5 hash decryption tool. It allows you to find plaintext matching MD5 hash by searching different combinations of characters. The tool supports the use of custom character sets and initial characters for more efficient search and collisions brute force.

WARNING: I optimized the project as best I could, but since it's still a CPU job - generating lots of combinations and searching can take twice as long. 

Use ctrl+c while generating combinations if you want to stop generation or search through already generated values!!!!

## Features

- Supports custom character sets and starting characters.
- Control over combination generation.
- Collision brute force.
- Tags replacement.

## Requirements

- `Python 3.x`
- `numpy`
- `tqdm`

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/kupertdev/md5-decrypter-python
   cd md5-decrypter-python
    ```

2. **Install dependencies:**

   ```sh
   pip install tqdm numpy
   ```

## Usage

To run the MD5 decryption script, use the following command:

```sh
python md5_decrypt_cpu.py <length> <md5-hash> <characters> [--start-char <start-char>, --word-list <word-list>, --brute-collision <brute-collision>]
```

Parameters

- Lenght - The length of the combinations to generate.
- MD5 hash - The MD5 hash to be decrypted.
- Characters - The characters to be used in the combinations. Ex.: 0123456789abcdefghijklmnopqrstuvwxyz
- Start char - The starting character to be used in the combinations.
- Word List - The path to the word list file. Ex.: /path/to/wordlist.txt
- Brute Collision - The maximum number of collisions to be used in the brute-force search. Ex.: 10

## Example

To find a plaintext corresponding to an MD5 hash with a length of 8 and characters 0123456789abcdefghijklmnopqrstuvwxyz, and with a starting character of abc:

Default command prompt

```sh
python md5_decrypt_cpu.py 10-12 b10a8db164e0754105b7a99be72e3fe5 "Helo<space>Wrd" --start-char "Hello<space>"
```

### Result:
```sh
Processing length: 10
Generating combinations: 100%|██████████████████████████████████████████████████████████████████████████████████████| 4096/4096 [00:00<00:00, 4050900.54it/s]
Total combinations: 4096
Searching: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 4096/4096 [00:00<00:00, 818985.99it/s] 
Word not found, contiune with next length range
==> Execution time: 0.01 seconds
Processing length: 11
Generating combinations: 100%|████████████████████████████████████████████████████████████████████████████████████| 32768/32768 [00:00<00:00, 4094832.36it/s] 
Total combinations: 32768
Searching:   0%|                                                                                                                   | 0/32768 [00:00<?, ?it/s] 
==> Found: Hello World with 1 collisions
==> Target: b10a8db164e0754105b7a99be72e3fe5 -> Source: b10a8db164e0754105b7a99be72e3fe5 -> Decrypted: Hello World
==> Execution time: 0.03 seconds
```

## Stop generation and search 

If you think that the number of generated combinations is enough - use Ctrl+C. A menu will appear in front of you:

```sd
Generating combinations:   1%|▍                                                                            | 6276566/1073741824 [00:01<03:52, 4588835.92it/s]
Processing interrupted. Continue iteration with generated combinations? Y/N: 
```

If you write Y - The script will search through the generated combinations.

```sh
Processing interrupted. Continue iteration with generated combinations? Y/N: Y
Total combinations: 6276566
Searching: 100%|███████████████████████████████████████████████████████████████████████████████████████████████| 6276566/6276566 [00:07<00:00, 871423.53it/s]
Word not found, contiune with next length range
==> Execution time: 7.20 seconds
Processing length: 11
Generating combinations:   0%|▎                                                                           | 38023165/8589934592 [00:08<33:10, 4296583.11it/s]
```

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. Ensure that you follow the project's code style and include tests for any new features or bug fixes.

# CUDA Work

Coming soon...
