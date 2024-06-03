from sage.crypto.block_cipher.des import DES
des = DES()
P = 0x7420656c73696353
K = 0x7CA110454A1A6E57
C = des.encrypt(plaintext=P, key=K); 
print (C)
C.hex()



