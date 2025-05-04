# Morse code represents letters, numbers, and punctuation with dots (.) and dashes (-).
# Each character is separated by a space, and words are separated by a slash (/).

morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}


def text_to_morse(text):
    text = text.upper()
    words = text.split()
    morse_words = []

    for word in words:
        morse_chars = []
        for char in word:
            if char in morse_code_dict:
                morse_chars.append(morse_code_dict[char])
            else:
                print(f"Character '{char}' is unsupported and will be skipped.")
        morse_word = ' '.join(morse_chars)
        morse_words.append(morse_word)

    return ' / '.join(morse_words)


# Get user input and display result
user_input = input("Enter the string to convert to Morse code: ")
morse_result = text_to_morse(user_input)
print("Morse Code:", morse_result)