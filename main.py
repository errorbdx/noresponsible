from curl_cffi import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import sys

# 1. Configuration & Keys
URL = "https://hotstarlive.nebula-core.workers.dev/?token=154dc5-7a9126-56996d-1fa267"
KEY_HEX = "fe3fd1b7dc91f363348da0cba1efcd0d0b571fc9f6a3e38c5084d47f7dbb5c49"
IV_HEX = "18b7e28e236b68119731470a85dfb3c9"

# We keep the exact headers you pulled from the app
HEADERS = {
    "Host": "hotstarlive.nebula-core.workers.dev",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
    "accept": "*/*",
    "cache-control": "no-cache, no-store"
}

def decrypt_aes(encrypted_hex, key_hex, iv_hex):
    try:
        encrypted_bytes = binascii.unhexlify(encrypted_hex)
        key = bytes.fromhex(key_hex)
        iv = bytes.fromhex(iv_hex)
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

def main():
    print("Fetching data using curl_cffi to spoof TLS fingerprint...")
    
    try:
        # The 'impersonate' flag perfectly mimics a real browser/app handshake
        # to stop Cloudflare from serving the YouTube redirect decoy.
        response = requests.get(URL, headers=HEADERS, impersonate="chrome110")
        
        if response.status_code == 200:
            print("Successfully connected! Bypassed the redirect.")
            encrypted_hex = response.text.strip()
            
            print("Decrypting payload...")
            decrypted_m3u8 = decrypt_aes(encrypted_hex, KEY_HEX, IV_HEX)

            if decrypted_m3u8:
                with open("emax.m3u8", "w", encoding="utf-8") as file:
                    file.write(decrypted_m3u8)
                print("Successfully saved playlist to emax.m3u8")
            else:
                print("Failed to decrypt the data. The payload might be in a different format.")
                sys.exit(1)
        else:
            print(f"Failed to connect. HTTP Status: {response.status_code}")
            print(f"Response Body: {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    
