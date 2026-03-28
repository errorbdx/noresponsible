import requests
from Crypto.Cipher import AES
import binascii

# --- Configuration ---
url = "https://hotstarlive.nebula-core.workers.dev/?token=154dc5-7a9126-56996d-1fa267"

user_agent = "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"

key_hex = "fe3fd1b7dc91f363348da0cba1efcd0d0b571fc9f6a3e38c5084d47f7dbb5c49"
iv_hex = "18b7e28e236b68119731470a85dfb3c9"

output_file = "emax.m3u8"

# --- Fetch encrypted content ---
headers = {"User-Agent": user_agent, "Accept": "*/*"}
response = requests.get(url, headers=headers)
response.raise_for_status()

encrypted_data = response.content  # assuming binary content
# If the server returns hex or base64, convert accordingly:
# encrypted_data = binascii.unhexlify(response.text.strip())
# or for base64: encrypted_data = base64.b64decode(response.text.strip())

# --- AES decryption (CBC) ---
key = binascii.unhexlify(key_hex)
iv = binascii.unhexlify(iv_hex)

cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_data = cipher.decrypt(encrypted_data)

# Remove PKCS7 padding
pad_len = decrypted_data[-1]
decrypted_data = decrypted_data[:-pad_len]

# --- Write to file ---
with open(output_file, "wb") as f:
    f.write(decrypted_data)

print(f"[+] Decrypted file saved as {output_file}")
