MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': '/'
}

REVERSE_MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

def text_to_morse(text):
    morse = []
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse.append(MORSE_CODE_DICT[char])
        else:
            print(f"Ignored unsupported: '{char}'")
    return ' '.join(morse)


def morse_to_text(morse):
    print(f"Debug - Original Morse: '{morse}'")  # Debug line
    words = morse.strip().split(' / ')
    print(f"Debug - Split Words: {words}")  # Debug line
    text = []
    words = morse.strip().split(' / ')  # Split words
    for word in words:
        chars = word.split()  # Split characters
        for char in chars:
            if char in REVERSE_MORSE_DICT:
                text.append(REVERSE_MORSE_DICT[char])
        text.append(' ')  # Add space after each word
    return ''.join(text).strip()