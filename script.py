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
    key = binascii.unhexlify(KEY_HEX)
    iv = binascii.unhexlify(IV_HEX)
    
    # 1. Strip EVERYTHING except valid Base64 chars (A-Z, a-z, 0-9, +, /)
    # This removes quotes, curly braces, and newlines automatically.
    b64_clean = re.sub(r'[^a-zA-Z0-9+/]', '', raw_text.replace('-', '+').replace('_', '/'))
    
    # 2. FIX: "1 more than a multiple of 4"
    # If the length is 4n + 1, that 1 extra char is usually a trailing quote or noise.
    # We strip it to make the string decodable.
    if len(b64_clean) % 4 == 1:
        b64_clean = b64_clean[:-1]
    
    # 3. Add necessary padding (=) to reach a multiple of 4
    while len(b64_clean) % 4 != 0:
        b64_clean += '='

    try:
        # 4. Decode to Bytes
        encrypted_bytes = base64.b64decode(b64_clean)
        
        # 5. AES Block alignment check
        # If it's not a multiple of 16, it's not valid AES-CBC. 
        # We trim it to the nearest 16 to try and force a partial recovery.
        if len(encrypted_bytes) % 16 != 0:
            encrypted_bytes = encrypted_bytes[:-(len(encrypted_bytes) % 16)]
            
        if not encrypted_bytes:
            return "# Error: Cleaned data was empty or too short."

        # 6. Decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_raw = cipher.decrypt(encrypted_bytes)
        
        # 7. Unpad (using custom unpad to handle potential corruption)
        try:
            return unpad(decrypted_raw, AES.block_size).decode('utf-8')
        except:
            # If unpadding fails, return the raw decode as a fallback
            return decrypted_raw.decode('utf-8', errors='ignore')
            
    except Exception as e:
        return f"# Decryption Crash: {str(e)}"

def main():
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.raise_for_status()
        
        result = decrypt_data(response.text)
        
        # Save results
        with open("emax.m3u8", "w", encoding="utf-8") as f:
            f.write(result)
        print("Done. Check emax.m3u8")
            
    except Exception as e:
        print(f"Network Error: {e}")

if __name__ == "__main__":
    main()
    
