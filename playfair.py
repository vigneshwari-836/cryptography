def create_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = key.upper().replace('J', 'I')
    combined = ""
    for char in (key + alphabet):
        if char not in combined and char.isalpha():
            combined += char
    return [list(combined[i:i+5]) for i in range(0, 25, 5)]

def find_position(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return 0, 0

def playfair_cipher(text, key, encrypt=True):
    matrix = create_matrix(key)
    text = text.upper().replace('J', 'I').replace(" ", "")

    # 1. Prepare Pairs
    pairs = []
    if encrypt:
        i = 0
        while i < len(text):
            a = text[i]
            if i + 1 < len(text):
                b = text[i+1]
                if a == b:
                    pairs.append(a + 'X')
                    i += 1
                else:
                    pairs.append(a + b)
                    i += 2
            else:
                pairs.append(a + 'X')
                i += 1
    else:
        pairs = [text[i:i+2] for i in range(0, len(text), 2)]

    # 2. Process Pairs
    processed_text = ""
    shift = 1 if encrypt else 4

    for p in pairs:
        r1, c1 = find_position(matrix, p[0])
        r2, c2 = find_position(matrix, p[1])

        if r1 == r2:
            processed_text += matrix[r1][(c1 + shift) % 5] + matrix[r2][(c2 + shift) % 5]
        elif c1 == c2:
            processed_text += matrix[(r1 + shift) % 5][c1] + matrix[(r2 + shift) % 5][c2]
        else:
            processed_text += matrix[r1][c2] + matrix[r2][c1]

    # 3. Post-Process Decryption (Remove 'X' fillers)
    if not encrypt:
        final_out = ""
        i = 0
        while i < len(processed_text):
            char = processed_text[i]
            # Check if 'X' is between two identical letters (e.g., L X L)
            if i + 2 < len(processed_text) and char == processed_text[i+2] and processed_text[i+1] == 'X':
                final_out += char
                i += 2 # Skip the X
            else:
                final_out += char
                i += 1

        # Remove trailing 'X' if it exists
        if final_out.endswith('X'):
            final_out = final_out[:-1]
        return final_out

    return processed_text

def main():
    while True:
        print("\n--- PLAYFAIR TOOL ---")
        choice = input("1. Playfair Cipher\n0. Exit\nSelect: ")
        if choice == '0': break
        if choice != '1': continue

        mode = input("Action (E/D): ").upper()
        msg = input("Message: ")
        key = input("Keyword: ")

        result = playfair_cipher(msg, key, mode == 'E')
        print(f"RESULT: {result}")

if __name__ == "__main__":
    main()

[23bcs096@mepcolinux ex2]$python3 play1.py

--- PLAYFAIR TOOL ---
1. Playfair Cipher
0. Exit
Select: 1
Action (E/D): e
Message: ballon
Keyword: cryptography
RESULT: OHQUUDQW

--- PLAYFAIR TOOL ---
1. Playfair Cipher
0. Exit
Select: 1
Action (E/D): d
Message: ohquudqw
Keyword: cryptography
RESULT: BALLON

--- PLAYFAIR TOOL ---
1. Playfair Cipher
0. Exit
Select: 1
Action (E/D): e
Message: attack
Keyword: monarchy
RESULT: RSSRDE

--- PLAYFAIR TOOL ---
1. Playfair Cipher
0. Exit
Select: 1
Action (E/D): d
Message: rssrde
Keyword: monarchy
RESULT: ATTACK

--- PLAYFAIR TOOL ---
1. Playfair Cipher
0. Exit
Select: 0
