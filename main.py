import cloudscraper
import binascii
import os
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Configuration
URL = "https://hotstarlive.nebula-core.workers.dev/?token=154dc5-7a9126-56996d-1fa267"
KEY_HEX = "fe3fd1b7dc91f363348da0cba1efcd0d0b571fc9f6a3e38c5084d47f7dbb5c49"
IV_HEX = "18b7e28e236b68119731470a85dfb3c9"

def run_task():
    # 1. Initialize Scraper
    scraper = cloudscraper.create_scraper()
    
    # Matching your provided request method exactly
    headers = {
        "Host": "hotstarlive.nebula-core.workers.dev",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "accept": "*/*",
        "cache-control": "no-cache, no-store",
        "accept-encoding": "gzip"
    }

    print(f"Connecting to: {URL}")
    
    try:
        # Use .content to get raw bytes instead of .text to avoid ASCII errors
        response = scraper.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
        raw_payload = response.content
        print(f"Received {len(raw_payload)} bytes of data.")

    except Exception as e:
        print(f"Network Error: {e}")
        sys.exit(1)

    # 2. Prepare Keys
    try:
        key = binascii.unhexlify(KEY_HEX)
        iv = binascii.unhexlify(IV_HEX)
    except binascii.Error as e:
        print(f"Key/IV Hex Error: {e}")
        sys.exit(1)

    # 3. Decrypt Data
    print("Attempting AES-256-CBC Decryption...")
    try:
        # Initialize AES Cipher
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Decrypt the raw content
        decrypted_raw = cipher.decrypt(raw_payload)
        
        # Remove PKCS7 Padding
        # Note: If this fails, the data might not be padded or key is wrong
        try:
            final_output = unpad(decrypted_raw, AES.block_size)
        except ValueError:
            print("Warning: Standard padding not found. Saving raw decryption.")
            final_output = decrypted_raw

        # 4. Save to file
        with open("emax.m3u8", "wb") as f:
            f.write(final_output)
            
        print("Success! File saved as emax.m3u8")
        
        # Preview the first few lines to console for logs
        preview = final_output[:100].decode('utf-8', errors='ignore')
        print(f"Content Preview: {preview}...")

    except Exception as e:
        print(f"Decryption Process Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_task()
        
