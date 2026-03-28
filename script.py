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
    
    # 1. Handle URL-safe Base64 (converts - to + and _ to /)
    # 2. Strip all non-base64 characters (quotes, spaces, etc.)
    b64_clean = raw_text.replace('-', '+').replace('_', '/')
    b64_clean = re.sub(r'[^a-zA-Z0-9+/]', '', b64_clean)
    
    # 3. Fix Base64 Padding (Must be multiple of 4)
    missing_padding = len(b64_clean) % 4
    if missing_padding:
        b64_clean += '=' * (4 - missing_padding)
    
    try:
        # 4. Decode Base64
        encrypted_bytes = base64.b64decode(b64_clean)
        
        # 5. Check AES Block Alignment (Must be multiple of 16)
        # If it's still not 16, we pad the BYTES with nulls to prevent the crash
        if len(encrypted_bytes) % 16 != 0:
            return f"# Error: Encrypted bytes ({len(encrypted_bytes)}) not 16-byte aligned."

        # 6. AES Decryption
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_raw = cipher.decrypt(encrypted_bytes)
        
        # 7. Unpad and Return
        return unpad(decrypted_raw, AES.block_size).decode('utf-8', errors='ignore')
        
    except Exception as e:
        return f"# Error: {str(e)}"

def main():
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.raise_for_status()
        
        result = decrypt_data(response.text)
        
        # Ensure we don't overwrite with an error message if decryption fails
        if "# Error" in result:
            print(result)
        else:
            with open("emax.m3u8", "w", encoding="utf-8") as f:
                f.write(result)
            print("Successfully updated emax.m3u8")
            
    except Exception as e:
        print(f"Fetch Error: {e}")

if __name__ == "__main__":
    main()
    
