import os
import base64
from rsa_utils import encrypt_data, decrypt_data, init_keys

private_key, public_key = init_keys()

# 儲存資料的類別
class Storage:
    def __init__(self, filename):
        self.filename = filename
        self.public_key = public_key
        self.private_key = private_key
    
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
    
    def save_all_records(self, records):
        with open(self.filename, "wb") as f:
            for data_list in records:
                enc_parts = [base64.b64encode(encrypt_data(self.public_key, str(d))) for d in data_list]
                line = b":".join(enc_parts) + b"\n"
                f.write(line)