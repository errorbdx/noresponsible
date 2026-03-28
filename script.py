import requests
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 1. Configuration - THE KEYS MUST BE CONVERTED FROM HEX TO BYTES
URL = "https://hotstarlive.nebula-core.workers.dev?token=154dc5-7a9126-56996d-1fa267"
KEY_HEX = "fe3fd1b7dc91f363348da0cba1efcd0d0b571fc9f6a3e38c5084d47f7dbb5c49"
IV_HEX = "18b7e28e236b68119731470a85dfb3c9"

# Convert Hex strings to actual Byte objects
key = binascii.unhexlify(KEY_HEX)
iv = binascii.unhexlify(IV_HEX)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache, no-store'
}

def decrypt_hex_data(raw_response):
    # Clean the response: remove quotes, spaces, and newlines
    # This ensures only 0-9 and a-f remain
    clean_hex = "".join(c for c in raw_response if c in "0123456789abcdefABCDEF")
    
    try:
        # Convert the encrypted Hex string from the server into bytes
        encrypted_bytes = binascii.unhexlify(clean_hex)
        
        # Initialize AES in CBC mode with the byte-version of your keys
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Decrypt and remove PKCS7 padding
        decrypted_raw = cipher.decrypt(encrypted_bytes)
        return unpad(decrypted_raw, AES.block_size).decode('utf-8')
        
    except Exception as e:
        return f"# Decryption failed: {str(e)}\n# Cleaned Hex Length: {len(clean_hex)}"

def main():
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Run the decryption
        result = decrypt_hex_data(response.text)
        
        # Save to file
        with open("emax.m3u8", "w", encoding="utf-8") as f:
            f.write(result)
        
        print("Process complete. Check emax.m3u8")
        
    except Exception as e:
        print(f"Network Error: {e}")

if __name__ == "__main__":
    main()
    
