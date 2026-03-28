import requests
import binascii
import base64
import re
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

def decrypt_data(raw_text):
    # Convert HEX keys/IV to bytes
    key = binascii.unhexlify(KEY_HEX)
    iv = binascii.unhexlify(IV_HEX)
    
    # 1. CLEANING: Remove everything that isn't a valid Base64 character
    # This removes quotes, brackets, or hidden Unicode markers (BOM)
    b64_clean = re.sub(r'[^a-zA-Z0-9+/=]', '', raw_text)
    
    try:
        # 2. Decode Base64 to raw bytes
        encrypted_bytes = base64.b64decode(b64_clean)
        
        # 3. AES Decryption (CBC)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_raw = cipher.decrypt(encrypted_bytes)
        
        # 4. Unpadding and decoding to UTF-8
        # We use 'ignore' to prevent crashes if there's a stray byte at the end
        decrypted_text = unpad(decrypted_raw, AES.block_size).decode('utf-8', errors='ignore')
        
        return decrypted_text
    except Exception as e:
        return f"# Error during Decryption: {str(e)}\n# Raw Length: {len(raw_text)}"

def main():
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Get response and handle potential JSON wrapper
        content = response.text
        
        # If the response is a JSON string like {"data": "..."}, we need the value
        # But if it's just the raw string, our regex cleaner handles it.
        result = decrypt_data(content)
        
        with open("emax.m3u8", "w", encoding="utf-8") as f:
            f.write(result)
            
        print("Update Successful: emax.m3u8 generated.")
        
    except Exception as e:
        print(f"Network/Request Error: {e}")

if __name__ == "__main__":
    main()
