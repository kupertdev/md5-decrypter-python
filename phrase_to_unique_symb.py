def unique_chars_generator(phrase):
    unique_chars = []
    seen_chars = set()

    for char in phrase:
        if char not in seen_chars:
            seen_chars.add(char)
            unique_chars.append(char)

    return ''.join(unique_chars)

phrase = 'Hello World!'
unique_string = unique_chars_generator(phrase)

print(unique_string)