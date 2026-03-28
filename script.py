import requests
import binascii
import json
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

def decrypt_data(raw_response):
    key = binascii.unhexlify(KEY_HEX)
    iv = binascii.unhexlify(IV_HEX)
    
    # 1. Clean the input: Remove quotes or handle JSON if the response is wrapped
    encrypted_text = raw_response.strip().replace('"', '')
    
    try:
        # 2. Convert Hex string to Bytes
        encrypted_bytes = binascii.unhexlify(encrypted_text)
        
        # 3. AES Decryption (CBC Mode)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        
        return decrypted.decode('utf-8')
    except Exception as e:
        return f"# Error: Decryption failed - {str(e)}"

def main():
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Get the raw text from response
        encrypted_data = response.text
        
        # Decrypt
        result = decrypt_data(encrypted_data)
        
        # Save to file
        with open("emax.m3u8", "w", encoding="utf-8") as f:
            f.write(result)
            
        print("Success: emax.m3u8 has been updated.")
        
    except Exception as e:
        print(f"Fetch Error: {e}")

if __name__ == "__main__":
    main()
        
