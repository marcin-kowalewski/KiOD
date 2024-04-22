import random
from sympy import isprime, gcd
import os

def text_to_int_blocks(text):
    # Dopełnienie tekstu, aby jego długość była wielokrotnością 8
    while len(text) % 8 != 0:
        text += '\0'  # Dodanie znaku o wartości 0 w ASCII
    
    # Podział tekstu na bloki 8-znakowe
    blocks = [text[i:i+8] for i in range(0, len(text), 8)]
    
    # Konwersja bloków na liczby całkowite
    int_blocks = []
    for block in blocks:
        block_value = 0
        for char in block:
            block_value = block_value * 256 + ord(char)  # Przesunięcie wartości i dodanie nowej wartości ASCII
        int_blocks.append(block_value)
    
    return int_blocks

def int_blocks_to_text(int_blocks):
    text = ""
    for value in int_blocks:
        block = ""
        for _ in range(8):
            char = chr(value % 256)  # Pobranie wartości ostatniego bajtu
            block = char + block  # Dodajemy znak na początek bloku (odwracamy kolejność)
            value //= 256  # Przygotowanie liczby do pobrania kolejnego bajtu
        text += block
    return text.rstrip('\x00')  # Usunięcie znaków dopełnienia


def generate_keys(bit_length=1024):
    def get_prime(n):
        p = random.getrandbits(n)
        while not isprime(p):
            p = random.getrandbits(n)
        return p
    
    p = get_prime(bit_length // 2)
    q = get_prime(bit_length // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    #e = 65537  # Często używany publiczny eksponent
    e = random.getrandbits(bit_length // 2)
    while not isprime(e) and gcd(e, phi) != 1:
            e = random.getrandbits(bit_length // 2)

    # Znajdowanie d, inwersja modularna e mod phi
    d = pow(e, -1, phi)
    
    # Klucz publiczny (e, n), klucz prywatny (d, n)
    return (e, n), (d, n)

def rsa_encrypt(int_blocks, public_key):
    e, n = public_key
    return [pow(block, e, n) for block in int_blocks]

def rsa_decrypt(int_blocks, private_key):
    d, n = private_key
    return [pow(block, d, n) for block in int_blocks]


# Funkcje rsa_encrypt, rsa_decrypt, text_to_int_blocks, int_blocks_to_text oraz generate_keys
# powinny być zaimplementowane zgodnie z wcześniejszymi opisami

def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        for value in data:
            file.write(f"{value}\n")

def load_data_from_file(filename):
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file]

text = "To jest scisle tajna informacja"
int_blocks = text_to_int_blocks(text)
print(int_blocks)

text = int_blocks_to_text(int_blocks)
print(text)

# Przykładowe użycie funkcji
public_key, private_key = generate_keys()
print('public_key:', public_key, 'private_key:', private_key)

text = "To jest scisle tajna informacja"
int_blocks = text_to_int_blocks(text)
encrypted_blocks = rsa_encrypt(int_blocks, public_key)
decrypted_blocks = rsa_decrypt(encrypted_blocks, private_key)
decrypted_text = int_blocks_to_text(decrypted_blocks)
print("Encrypted:", encrypted_blocks)
print("Decrypted:", decrypted_text)

