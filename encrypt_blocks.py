def xor_bytes(a, b):
    """XOR dwóch ciągów bajtów."""
    return #...

def cfb_encrypt(key, iv, plaintext, block_size, encrypt_block):
    """
    Szyfrowanie w trybie CFB.
    
    Args:
    key: Klucz używany w funkcji szyfrującej blok.
    iv: Wektor inicjalizacyjny (Initialization Vector), o długości block_size.
    plaintext: Tekst jawny do zaszyfrowania.
    block_size: Rozmiar bloku używany przez kryptosystem.
    encrypt_block: Funkcja szyfrująca blok danych.
    
    Returns:
    Zaszyfrowany tekst (ciphertext).
    """
    ciphertext = []
    prev_block = iv
    
    for i in range(0, len(plaintext), block_size):
        # Pobranie bloku tekstu jawnego
        block = plaintext[i:i+block_size]
        # Dopasowanie rozmiaru bloku tekstu jawnego do rozmiaru bloku
        if len(block) < block_size:
            block = block + b'\x00' * (block_size - len(block))
        
        # Szyfrowanie poprzedniego bloku
        encrypted_block = encrypt_block(key, prev_block)
        # XOR bloku szyfrowanego z blokiem tekstu jawnego
        cipher_block = xor_bytes(encrypted_block, block)
        # Przygotowanie do kolejnej iteracji
        prev_block = cipher_block
        
        # Dodanie zaszyfrowanego bloku do wyniku
        ciphertext.append(cipher_block)
    
    return b''.join(ciphertext)

def cfb_decrypt(key, iv, ciphertext, block_size, decrypt_block):
    """
    Deszyfrowanie w trybie CFB.
    
    Args:
    key: Klucz używany w funkcji szyfrującej blok.
    iv: Wektor inicjalizacyjny (Initialization Vector), o długości block_size.
    ciphertext: Tekst zaszyfrowany do odszyfrowania.
    block_size: Rozmiar bloku używany przez kryptosystem.
    decrypt_block: Funkcja deszyfrująca blok danych (nieużywana w CFB).
    
    Returns:
    Odszyfrowany tekst (plaintext).
    """
    plaintext = []
    prev_block = iv
    
    for i in range(0, len(ciphertext), block_size):
        # Pobranie bloku zaszyfrowanego tekstu
        block = ciphertext[i:i+block_size]
        # Szyfrowanie poprzedniego bloku
        encrypted_block = encrypt_block(key, prev_block)
        # XOR zaszyfrowanego bloku z aktualnym blokiem tekstu zaszyfrowanego
        plain_block = xor_bytes(encrypted_block, block)
        # Przygotowanie do kolejnej iteracji
        prev_block = block
        
        # Dodanie odszyfrowanego bloku do wyniku
        plaintext.append(plain_block)
    
    return b''.join(plaintext)