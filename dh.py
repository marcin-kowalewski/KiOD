import random

def generate_private_key(p):
    """Generuje klucz prywatny jako losową liczbę całkowitą mniejszą od p."""
    return random.randint(2, p-2)

def generate_public_key(g, p, private_key):
    return pow(g, private_key, p)

def generate_shared_secret(public_key, private_key, p):
    return pow(public_key, private_key, p)

# Parametry publiczne (mogą być uzgodnione publicznie)
p = 23  # duża liczba pierwsza ;)
g = 5   # baza

# Generowanie kluczy prywatnych
private_key_a = generate_private_key(p)
private_key_b = generate_private_key(p)

# Generowanie kluczy publicznych
public_key_a = generate_public_key(g, p, private_key_a)
public_key_b = generate_public_key(g, p, private_key_b)

# Wymiana kluczy publicznych i generowanie wspólnego sekretu
shared_secret_a = generate_shared_secret(public_key_b, private_key_a, p)
shared_secret_b = generate_shared_secret(public_key_a, private_key_b, p)

print("Klucz prywatny A:", private_key_a)
print("Klucz publiczny A:", public_key_a)
print("Klucz prywatny B:", private_key_b)
print("Klucz publiczny B:", public_key_b)
print("Wspólny sekret obliczony przez A:", shared_secret_a)
print("Wspólny sekret obliczony przez B:", shared_secret_b)

# Sprawdzanie, czy wspólny sekret jest taki sam
assert shared_secret_a == shared_secret_b, "Wspólne sekrety różnią się!"
