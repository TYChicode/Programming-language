# rsa_utils.py
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

PRIVATE_PATH = "private_key.pem"
PUBLIC_PATH = "public_key.pem"



# 生成公鑰和私鑰
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def save_keys(private_key, public_key):
    with open(PRIVATE_PATH, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(PUBLIC_PATH, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))



# 初始化/載入密鑰
def init_keys():
    if not os.path.exists(PRIVATE_PATH) or not os.path.exists(PUBLIC_PATH):
        private_key, public_key = generate_keys()
        save_keys(private_key, public_key)
    else:
        private_key = load_private_key()
        public_key = load_public_key()
    return private_key, public_key



# 載入公鑰和私鑰
def load_public_key():
    with open(PUBLIC_PATH, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def load_private_key():
    with open(PRIVATE_PATH, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)



# 加密和解密資料
def encrypt_data(public_key, plaintext: str):
    return public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

def decrypt_data(private_key, ciphertext: bytes):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    ).decode()
