import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

# 1. Configuration & Keys
URL = "https://hotstarlive.nebula-core.workers.dev/?token=154dc5-7a9126-56996d-1fa267"
KEY_HEX = "fe3fd1b7dc91f363348da0cba1efcd0d0b571fc9f6a3e38c5084d47f7dbb5c49"
IV_HEX = "18b7e28e236b68119731470a85dfb3c9"

# Mimicking the exact request method provided
HEADERS = {
    "Host": "hotstarlive.nebula-core.workers.dev",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
    "accept": "*/*",
    "cache-control": "no-cache, no-store",
    # The requests library handles gzip automatically, so we can omit 'accept-encoding' 
    # or leave it. Leaving it out prevents raw compressed byte conflicts.
}

def decrypt_aes(encrypted_bytes, key_hex, iv_hex):
    """Decrypts AES-CBC encrypted bytes using hex keys."""
    try:
        # Convert hex strings to raw bytes
        key = bytes.fromhex(key_hex)
        iv = bytes.fromhex(iv_hex)
        
        # Initialize the Cipher
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Decrypt and remove PKCS7 padding
        decrypted_data = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted_data.decode('utf-8')
    except ValueError as e:
        print(f"Decryption failed (Padding or Key error): {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    print("Fetching encrypted data...")
    response = requests.get(URL, headers=HEADERS)
    
    if response.status_code == 200:
        # Some APIs return the payload as a hex string rather than raw binary. 
        # We will try to unhexlify it first; if it fails, we treat it as raw bytes.
        try:
            encrypted_data = binascii.unhexlify(response.text.strip())
        except binascii.Error:
            encrypted_data = response.content

        print("Decrypting payload...")
        decrypted_m3u8 = decrypt_aes(encrypted_data, KEY_HEX, IV_HEX)

        if decrypted_m3u8:
            # Save the decrypted output
            with open("emax.m3u8", "w", encoding="utf-8") as file:
                file.write(decrypted_m3u8)
            print("Successfully saved playlist to emax.m3u8")
        else:
            print("Failed to decrypt the data.")
    else:
        print(f"Failed to connect to API. HTTP Status: {response.status_code}")

if __name__ == "__main__":
    main()
  
