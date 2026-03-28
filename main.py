import httpx
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

# 1. Configuration & Keys
URL = "https://hotstarlive.nebula-core.workers.dev/?token=154dc5-7a9126-56996d-1fa267"
KEY_HEX = "fe3fd1b7dc91f363348da0cba1efcd0d0b571fc9f6a3e38c5084d47f7dbb5c49"
IV_HEX = "18b7e28e236b68119731470a85dfb3c9"

# Restoring the exact headers, including accept-encoding
HEADERS = {
    "Host": "hotstarlive.nebula-core.workers.dev",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
    "accept": "*/*",
    "cache-control": "no-cache, no-store",
    "accept-encoding": "gzip"
}

def decrypt_aes(encrypted_hex, key_hex, iv_hex):
    """Decrypts AES-CBC encrypted hex string using hex keys."""
    try:
        # The data is likely coming as a hex string, so we unhexlify it first
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
    print("Fetching encrypted data using HTTP/2...")
    
    # Initialize an HTTP/2 client to match the app's protocol
    try:
        with httpx.Client(http2=True) as client:
            response = client.get(URL, headers=HEADERS)
            
            if response.status_code == 200:
                print("Successfully connected to API.")
                
                # Assuming the response text is the encrypted hex string
                encrypted_hex = response.text.strip()
                
                print("Decrypting payload...")
                decrypted_m3u8 = decrypt_aes(encrypted_hex, KEY_HEX, IV_HEX)

                if decrypted_m3u8:
                    with open("emax.m3u8", "w", encoding="utf-8") as file:
                        file.write(decrypted_m3u8)
                    print("Successfully saved playlist to emax.m3u8")
                else:
                    print("Failed to decrypt the data.")
            else:
                print(f"Failed to connect. HTTP Status: {response.status_code}")
                print(f"Response Body: {response.text}")
                
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    main()
    
