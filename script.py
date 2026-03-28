import requests
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Configuration
URL = "https://hotstarlive.nebula-core.workers.dev?token=154dc5-7a9126-56996d-1fa267"
KEY_HEX = "fe3fd1b7dc91f363348da0cba1efcd0d0b571fc9f6a3e38c5084d47f7dbb5c49"
IV_HEX = "18b7e28e236b68119731470a85dfb3c9"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache, no-store'
}

def decrypt_data(encrypted_text):
    key = binascii.unhexlify(KEY_HEX)
    iv = binascii.unhexlify(IV_HEX)
    # Assuming the response is Base64 or raw hex, adjust if it's different
    # Most common is raw bytes or base64. If it's hex, use unhexlify.
    try:
        raw_data = binascii.unhexlify(encrypted_text.strip())
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(raw_data), AES.block_size)
        return decrypted.decode('utf-8')
    except Exception as e:
        return f"Decryption failed: {e}"

def main():
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        # If response is already plain text, use response.text
        # If encrypted, call decrypt_data(response.text)
        decrypted_content = decrypt_data(response.text)
        
        with open("emax.m3u8", "w", encoding="utf-8") as f:
            f.write(decrypted_content)
        print("File emax.m3u8 updated successfully.")
    else:
        print(f"Failed to fetch. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
      
