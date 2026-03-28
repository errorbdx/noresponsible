import cloudscraper
import binascii
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Configuration - Using Hex strings provided
URL = "https://hotstarlive.nebula-core.workers.dev/?token=154dc5-7a9126-56996d-1fa267"
KEY_HEX = "fe3fd1b7dc91f363348da0cba1efcd0d0b571fc9f6a3e38c5084d47f7dbb5c49"
IV_HEX = "18b7e28e236b68119731470a85dfb3c9"

def run_task():
    # 1. Initialize Scraper with custom headers
    scraper = cloudscraper.create_scraper()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "accept": "*/*",
        "cache-control": "no-cache, no-store",
    }

    print("Fetching encrypted data...")
    response = scraper.get(URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status: {response.status_code}")
        return

    # 2. Prepare Decryption
    # Convert Hex strings to raw bytes
    key = binascii.unhexlify(KEY_HEX)
    iv = binascii.unhexlify(IV_HEX)
    
    # Check if response is hex or raw; assuming hex string based on typical API outputs
    try:
        encrypted_data = binascii.unhexlify(response.text.strip())
    except binascii.Error:
        # If it's not hex, it might be raw binary
        encrypted_data = response.content

    # 3. Decrypt (AES-256-CBC)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # 4. Save Output
    with open("emax.m3u8", "wb") as f:
        f.write(decrypted_data)
    print("Successfully saved decrypted content to emax.m3u8")

if __name__ == "__main__":
    run_task()
            
