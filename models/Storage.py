import base64
from rsa_utils import *
import os

# 載入或建立密鑰
if not os.path.exists("private_key.pem") or not os.path.exists("public_key.pem"):
    private_key, public_key = generate_keys()
    save_keys(private_key, public_key)
else:
    private_key = load_private_key()
    public_key = load_public_key()

# 儲存資料的類別
class Storage:
    def __init__(self, filename):
        self.filename = filename

    def save_record(self, data_list):
        enc_parts = [base64.b64encode(encrypt_data(public_key, str(d))) for d in data_list]
        line = b":".join(enc_parts) + b"\n"
        with open(self.filename, "ab") as f:
            f.write(line)

    def load_records(self):
        results = []
        if not os.path.exists(self.filename):
            return results
        with open(self.filename, "rb") as f:
            for line in f:
                parts = line.strip().split(b":")
                try:
                    dec_parts = [decrypt_data(private_key, base64.b64decode(p)) for p in parts]
                    results.append(dec_parts)
                except Exception:
                    continue
        return results