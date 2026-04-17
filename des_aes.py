S0 = [[1, 0, 3, 2], [3, 2, 1, 0],[0, 2, 1, 3], [3, 1, 3, 2]
]
S1 = [
    [0, 1, 2, 3],[2, 0, 1, 3], [3, 0, 1, 0],[2, 1, 0, 3]
]
P10 =[3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8  =[6, 3, 7, 4, 8, 5, 10, 9]
P4  = [2, 4, 3, 1]
IP  =[2, 6, 3, 1, 4, 8, 5, 7]
IP_INV =[4, 1, 3, 5, 7, 2, 8, 6]
EP  =[4, 1, 2, 3, 2, 3, 4, 1]
def permute(bits, table):
    return "".join(bits[i - 1] for i in table)
def xor(a, b):
    return "".join("0" if x == y else "1" for x, y in zip(a, b))
def left_shift(bits, n):
    return bits[n:] + bits[:n]
def s_box(bits, box):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return format(box[row][col], '02b')
def round_func(bits, key, round_num):
    L = bits[:4]
    R = bits[4:]
    print(f"\nRound {round_num}:")
    print(f"L = {L}, R = {R}")
    ep = permute(R, EP)
    print(f"EP(R) = {ep}")
    x = xor(ep, key)
    print(f"XOR with subkey = {x}")
    s0 = s_box(x[:4], S0)
    s1 = s_box(x[4:], S1)
    print(f"S-Box outputs -> S0={s0}, S1={s1}")
    p4 = permute(s0 + s1, P4)
    print(f"P4 = {p4}")
    new_L = xor(L, p4)
    print(f"New Left = L XOR P4 = {new_L}")
    return new_L + R
def run_sdes(pt, key):
    print("\n==============")
    print("S-DES ENCRYPTION ")
    print("================")
    print("\n--- KEY GENERATION ---")
    print(f"Original 10-bit Key: {key}")
    p10_key = permute(key, P10)
    print(f"After applying P10: {p10_key}")
    L, R = p10_key[:5], p10_key[5:]
    print(f"Split into halves -> L={L}, R={R}")
    L, R = left_shift(L, 1), left_shift(R, 1)
    print(f"Left shift by 1 -> L={L}, R={R}")
    k1 = permute(L + R, P8)
    print(f"Apply P8 -> Subkey K1 = {k1}")
    L, R = left_shift(L, 2), left_shift(R, 2)
    k2 = permute(L + R, P8)
    print(f"Left shift by 2 and apply P8 -> Subkey K2 = {k2}")
    print("\n--- ENCRYPTION ---")
    ipt = permute(pt, IP)
    print(f"Initial Permutation IP(PT) = {ipt}")
    r1 = round_func(ipt, k1, 1)
    sw = r1[4:] + r1[:4]
    print(f"\nSwap halves -> {sw}")
    r2 = round_func(sw, k2, 2)
    cipher = permute(r2, IP_INV)
    print("\nApply IP")
    print(f"Final Ciphertext = {cipher}\n")
if __name__ == "__main__":
    print("=== S-DES Encryption ===")
    while True:
        plaintext = input("Enter 8-bit Plaintext: ").strip()
        if len(plaintext) == 8 and all(c in '01' for c in plaintext):
            break
        print("Error: Plaintext must be exactly 8 characters of 0s and 1s. Try again.\n")
    while True:
        key_input = input("Enter 10-bit Key: ").strip()
        if len(key_input) == 10 and all(c in '01' for c in key_input):
            break
        print("Error: Key must be exactly 10 characters of 0s and 1s. Try again.\n")
    print("\nStarting Encryption...")
    run_sdes(plaintext, key_input)
[23bcs070@mepcolinux ex4]$python3 des.py
=== S-DES Encryption ===
Enter 8-bit Plaintext: 10101010
Enter 10-bit Key:  0000000000

Starting Encryption...

==============
S-DES ENCRYPTION
================

--- KEY GENERATION ---
Original 10-bit Key: 0000000000
After applying P10: 0000000000
Split into halves -> L=00000, R=00000
Left shift by 1 -> L=00000, R=00000
Apply P8 -> Subkey K1 = 00000000
Left shift by 2 and apply P8 -> Subkey K2 = 00000000

--- ENCRYPTION ---
Initial Permutation IP(PT) = 00110011

Round 1:
L = 0011, R = 0011
EP(R) = 10010110
XOR with subkey = 10010110
S-Box outputs -> S0=11, S1=11
P4 = 1111
New Left = L XOR P4 = 1100

Swap halves -> 00111100

Round 2:
L = 0011, R = 1100
EP(R) = 01101001
XOR with subkey = 01101001
S-Box outputs -> S0=10, S1=10
P4 = 0011
New Left = L XOR P4 = 0000

Apply IP
Final Ciphertext = 00010001

[23bcs070@mepcolinux ex4]$cat aes.py
SBOX =[
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

RCON =[0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
def aes_xor(a, b):
    return[x ^ y for x, y in zip(a, b)]
def gmul(a, b):
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        hi_bit = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit:
            a ^= 0x1B
        b >>= 1
    return p

def state_matrix(state):
    lines =[]
    for row in range(4):
        row_str = "  "
        for col in range(4):
            row_str += f"{state[col * 4 + row]:02x} "
        lines.append(row_str)
    return "\n".join(lines)
def run_aes(pt_raw, key_raw):
    state = [ord(c) for c in pt_raw]
    key_bytes =[ord(c) for c in key_raw]

    print("=" * 60)
    print("AES-128 ENCRYPTION")
    print("=" * 60)
    print(f"\nPlaintext  (hex): {' '.join(f'{b:02x}' for b in state)}")
    print(f"Key        (hex): {' '.join(f'{b:02x}' for b in key_bytes)}")
    print("\n" + "=" * 60)
    print("KEY EXPANSION (W0 to W43)")
    print("=" * 60)
    w =[]
    for i in range(4):
        w.append(key_bytes[4 * i : 4 * i + 4])
    for i in range(4, 44):
        temp = w[i - 1][:]
        if i % 4 == 0:
            temp = temp[1:] + temp[:1]
            temp = [SBOX[b] for b in temp]
            temp[0] ^= RCON[(i // 4) - 1]
        w.append(aes_xor(w[i - 4], temp))
    for i in range(44):
        label = f"W{i}".ljust(4)
        if i % 4 == 0:
            rk = "Round Key 0 (Initial)" if i == 0 else f"Round Key {i // 4}"
            print(f"\n  -- {rk} --")

        hex_space = " ".join(f"{b:02x}" for b in w[i])
        hex_joined = "".join(f"{b:02x}" for b in w[i])
        print(f"  {label} = {hex_space}   [{hex_joined}]")
    print("\n" + "=" * 60)
    print("INITIAL AddRoundKey (Round Key 0: W0-W3)")
    print("=" * 60)
    print("State before:\n" + state_matrix(state))
    round_key_0 = w[0] + w[1] + w[2] + w[3]
    state = aes_xor(state, round_key_0)
    print(f"\nRound Key 0: {' '.join(f'{b:02x}' for b in round_key_0)}")
    print("State after AddRoundKey:\n" + state_matrix(state))
    for r in range(1, 11):
        print("\n" + "=" * 60)
        print(f"ROUND {r}{' (Final Round no MixColumns)' if r == 10 else ''}")
        print("=" * 60)
        state = [SBOX[b] for b in state]
        print("\n  [SubBytes]\n" + state_matrix(state))
        sr = [0] * 16
        for row in range(4):
            for col in range(4):
                sr[col * 4 + row] = state[((col + row) % 4) * 4 + row]
        state = sr
        print("\n  [ShiftRows]\n" + state_matrix(state))
        if r < 10:
            mc = [0] * 16
            for col in range(4):
                s0, s1, s2, s3 = state[col * 4 + 0], state[col * 4 + 1], state[col * 4 + 2], state[col * 4 + 3]
                mc[col * 4 + 0] = gmul(0x02, s0) ^ gmul(0x03, s1) ^ s2 ^ s3
                mc[col * 4 + 1] = s0 ^ gmul(0x02, s1) ^ gmul(0x03, s2) ^ s3
                mc[col * 4 + 2] = s0 ^ s1 ^ gmul(0x02, s2) ^ gmul(0x03, s3)
                mc[col * 4 + 3] = gmul(0x03, s0) ^ s1 ^ s2 ^ gmul(0x02, s3)
            state = mc
            print("\n  [MixColumns]\n" + state_matrix(state))
        rk = w[r * 4] + w[r * 4 + 1] + w[r * 4 + 2] + w[r * 4 + 3]
        print(f"\n[AddRoundKey  W{r * 4} W{r * 4 + 3}]")
        print(f"  Round Key: {' '.join(f'{b:02x}' for b in rk)}")
        state = aes_xor(state, rk)
        print(state_matrix(state))
    print("\n" + "=" * 60)
    print("FINAL CIPHERTEXT")
    print("=" * 60)
    print("Hex: " + "".join(f"{b:02x}" for b in state) + "\n")
if __name__ == "__main__":
    print("=== AES-128 Encryption ===")
    while True:
        plaintext = input("Enter 16-character Plaintext: ")
        if len(plaintext) == 16:
            break
        print(f"Error: Plaintext must be exactly 16 characters long. You entered {len(plaintext)}. Try again.\n")
    while True:
        key_input = input("Enter 16-character Key: ")
        if len(key_input) == 16:
            break
        print(f"Error: Key must be exactly 16 characters long. You entered {len(key_input)}. Try again.\n")
    print("\nStarting Encryption...\n")
    run_aes(plaintext, key_input)
[23bcs070@mepcolinux ex4]$python3 aes.py
=== AES-128 Encryption ===
Enter 16-character Plaintext: HELLOAESWORLD!!!
Enter 16-character Key: SUPERSECRETKEY!!

Starting Encryption...

============================================================
AES-128 ENCRYPTION
============================================================

Plaintext  (hex): 48 45 4c 4c 4f 41 45 53 57 4f 52 4c 44 21 21 21
Key        (hex): 53 55 50 45 52 53 45 43 52 45 54 4b 45 59 21 21

============================================================
KEY EXPANSION (W0 to W43)
============================================================

  -- Round Key 0 (Initial) --
  W0   = 53 55 50 45   [53555045]
  W1   = 52 53 45 43   [52534543]
  W2   = 52 45 54 4b   [5245544b]
  W3   = 45 59 21 21   [45592121]

  -- Round Key 1 --
  W4   = 99 a8 ad 2b   [99a8ad2b]
  W5   = cb fb e8 68   [cbfbe868]
  W6   = 99 be bc 23   [99bebc23]
  W7   = dc e7 9d 02   [dce79d02]

  -- Round Key 2 --
  W8   = 0f f6 da ad   [0ff6daad]
  W9   = c4 0d 32 c5   [c40d32c5]
  W10  = 5d b3 8e e6   [5db38ee6]
  W11  = 81 54 13 e4   [815413e4]

  -- Round Key 3 --
  W12  = 2b 8b b3 a1   [2b8bb3a1]
  W13  = ef 86 81 64   [ef868164]
  W14  = b2 35 0f 82   [b2350f82]
  W15  = 33 61 1c 66   [33611c66]

  -- Round Key 4 --
  W16  = cc 17 80 62   [cc178062]
  W17  = 23 91 01 06   [23910106]
  W18  = 91 a4 0e 84   [91a40e84]
  W19  = a2 c5 12 e2   [a2c512e2]

  -- Round Key 5 --
  W20  = 7a de 18 58   [7ade1858]
  W21  = 59 4f 19 5e   [594f195e]
  W22  = c8 eb 17 da   [c8eb17da]
  W23  = 6a 2e 05 38   [6a2e0538]

  -- Round Key 6 --
  W24  = 6b b5 1f 5a   [6bb51f5a]
  W25  = 32 fa 06 04   [32fa0604]
  W26  = fa 11 11 de   [fa1111de]
  W27  = 90 3f 14 e6   [903f14e6]

  -- Round Key 7 --
  W28  = 5e 4f 91 3a   [5e4f913a]
  W29  = 6c b5 97 3e   [6cb5973e]
  W30  = 96 a4 86 e0   [96a486e0]
  W31  = 06 9b 92 06   [069b9206]

  -- Round Key 8 --
  W32  = ca 00 fe 55   [ca00fe55]
  W33  = a6 b5 69 6b   [a6b5696b]
  W34  = 30 11 ef 8b   [3011ef8b]
  W35  = 36 8a 7d 8d   [368a7d8d]

  -- Round Key 9 --
  W36  = af ff a3 50   [afffa350]
  W37  = 09 4a ca 3b   [094aca3b]
  W38  = 39 5b 25 b0   [395b25b0]
  W39  = 0f d1 58 3d   [0fd1583d]

  -- Round Key 10 --
  W40  = a7 95 84 26   [a7958426]
  W41  = ae df 4e 1d   [aedf4e1d]
  W42  = 97 84 6b ad   [97846bad]
  W43  = 98 55 33 90   [98553390]

============================================================
INITIAL AddRoundKey (Round Key 0: W0-W3)
============================================================
State before:
  48 4f 57 44
  45 41 4f 21
  4c 45 52 21
  4c 53 4c 21

Round Key 0: 53 55 50 45 52 53 45 43 52 45 54 4b 45 59 21 21
State after AddRoundKey:
  1b 1d 05 01
  10 12 0a 78
  1c 00 06 00
  09 10 07 00

============================================================
ROUND 1
============================================================

  [SubBytes]
  af a4 6b 7c
  ca c9 67 bc
  9c 63 6f 63
  01 ca c5 63

  [ShiftRows]
  af a4 6b 7c
  c9 67 bc ca
  6f 63 9c 63
  63 01 ca c5

  [MixColumns]
  09 98 5f 1b
  f4 ce 7d 93
  1d 06 b1 24
  8a f1 12 bc

[AddRoundKey  W4 W7]
  Round Key: 99 a8 ad 2b cb fb e8 68 99 be bc 23 dc e7 9d 02
  90 53 c6 c7
  5c 35 c3 74
  b0 ee 0d b9
  a1 99 31 be

============================================================
ROUND 2
============================================================

  [SubBytes]
  60 ed b4 c6
  4a 96 2e 92
  e7 28 d7 56
  32 ee c7 ae

  [ShiftRows]
  60 ed b4 c6
  96 2e 92 4a
  d7 56 e7 28
  ae 32 ee c7

  [MixColumns]
  18 d7 d7 a6
  9b 79 57 ed
  aa 39 da 8e
  a6 30 75 a6

[AddRoundKey  W8 W11]
  Round Key: 0f f6 da ad c4 0d 32 c5 5d b3 8e e6 81 54 13 e4
  17 13 8a 27
  6d 74 e4 b9
  70 0b 54 9d
  0b f5 93 42

============================================================
ROUND 3
============================================================

  [SubBytes]
  f0 7d 7e cc
  3c 92 69 56
  51 2b 20 5e
  2b e6 dc 2c

  [ShiftRows]
  f0 7d 7e cc
  92 69 56 3c
  20 5e 51 2b
  2c 2b e6 dc

  [MixColumns]
  5a 34 b1 30
  83 66 c7 15
  56 d5 bb d9
  e1 e6 52 fb

[AddRoundKey  W12 W15]
  Round Key: 2b 8b b3 a1 ef 86 81 64 b2 35 0f 82 33 61 1c 66
  71 db 03 03
  08 e0 f2 74
  e5 54 b4 c5
  40 82 d0 9d

============================================================
ROUND 4
============================================================

  [SubBytes]
  a3 b9 7b 7b
  30 e1 89 92
  d9 20 8d a6
  09 13 70 5e

  [ShiftRows]
  a3 b9 7b 7b
  e1 89 92 30
  8d a6 d9 20
  5e 09 13 70

  [MixColumns]
  b6 46 91 f6
  a8 48 27 0b
  a1 7c 75 9b
  2e ed e0 7d

[AddRoundKey  W16 W19]
  Round Key: cc 17 80 62 23 91 01 06 91 a4 0e 84 a2 c5 12 e2
  7a 65 00 54
  bf d9 83 ce
  21 7d 7b 89
  4c eb 64 9f

============================================================
ROUND 5
============================================================

  [SubBytes]
  da 4d 63 20
  08 35 ec 8b
  fd ff 21 a7
  29 e9 43 db

  [ShiftRows]
  da 4d 63 20
  35 ec 8b 08
  21 a7 fd ff
  db 29 e9 43

  [MixColumns]
  0a 3b 54 e4
  08 55 9b 69
  db 8f 29 08
  cc ce 1a 11

[AddRoundKey  W20 W23]
  Round Key: 7a de 18 58 59 4f 19 5e c8 eb 17 da 6a 2e 05 38
  70 62 9c 8e
  d6 1a 70 47
  c3 96 3e 0d
  94 90 c0 29

============================================================
ROUND 6
============================================================

  [SubBytes]
  51 aa de 19
  f6 a2 51 a0
  2e 90 b2 d7
  22 60 ba a5

  [ShiftRows]
  51 aa de 19
  a2 51 a0 f6
  b2 d7 2e 90
  a5 22 60 ba

  [MixColumns]
  48 49 12 19
  66 48 97 ff
  78 28 82 01
  b2 27 37 22

[AddRoundKey  W24 W27]
  Round Key: 6b b5 1f 5a 32 fa 06 04 fa 11 11 de 90 3f 14 e6
  23 7b e8 89
  d3 b2 86 c0
  67 2e 93 15
  e8 23 e9 c4

============================================================
ROUND 7
============================================================

  [SubBytes]
  26 21 9b a7
  66 37 44 ba
  85 31 dc 59
  9b 26 1e 1c

  [ShiftRows]
  26 21 9b a7
  37 44 ba 66
  dc 59 85 31
  1c 9b 26 1e

  [MixColumns]
  d5 4c 5b d0
  2b d9 46 26
  96 61 5a 81
  b9 53 c5 99

[AddRoundKey  W28 W31]
  Round Key: 5e 4f 91 3a 6c b5 97 3e 96 a4 86 e0 06 9b 92 06
  8b 20 cd d6
  64 6c e2 bd
  07 f6 dc 13
  83 6d 25 9f

============================================================
ROUND 8
============================================================

  [SubBytes]
  3d b7 bd f6
  43 50 98 7a
  c5 42 86 7d
  ec 3c 3f db

  [ShiftRows]
  3d b7 bd f6
  50 98 7a 43
  86 7d c5 42
  db ec 3c 3f

  [MixColumns]
  d7 57 16 4f
  d7 f7 21 89
  0c fa 12 70
  3c e4 1b 7e

[AddRoundKey  W32 W35]
  Round Key: ca 00 fe 55 a6 b5 69 6b 30 11 ef 8b 36 8a 7d 8d
  1d f1 26 79
  d7 42 30 03
  f2 93 fd 0d
  69 8f 90 f3

============================================================
ROUND 9
============================================================

  [SubBytes]
  a4 a1 f7 b6
  0e 2c 04 7b
  89 dc 54 d7
  f9 73 60 0d

  [ShiftRows]
  a4 a1 f7 b6
  2c 04 7b 0e
  54 d7 89 dc
  0d f9 73 60

  [MixColumns]
  7e 7b 82 d9
  0d 32 f2 b5
  37 00 10 bb
  95 c2 16 d3

[AddRoundKey  W36 W39]
  Round Key: af ff a3 50 09 4a ca 3b 39 5b 25 b0 0f d1 58 3d
  d1 72 bb d6
  f2 78 a9 64
  94 ca 35 e3
  c5 f9 a6 ee

============================================================
ROUND 10 (Final Round no MixColumns)
============================================================

  [SubBytes]
  3e 40 ea f6
  89 bc d3 43
  22 74 96 11
  a6 99 24 28

  [ShiftRows]
  3e 40 ea f6
  bc d3 43 89
  96 11 22 74
  28 a6 99 24

[AddRoundKey  W40 W43]
  Round Key: a7 95 84 26 ae df 4e 1d 97 84 6b ad 98 55 33 90
  99 ee 7d 6e
  29 0c c7 dc
  12 5f 49 47
  0e bb 34 b4

============================================================
FINAL CIPHERTEXT
============================================================
Hex: 9929120eee0c5fbb7dc749346edc47b4
