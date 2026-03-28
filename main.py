import cloudscraper
import os

# 1. Target URL
url = "https://hotstarlive.nebula-core.workers.dev/?token=u003d154dc5-7a9126-56996d-1fa267"

# 2. Exact Headers from your logs
# We use the 'okhttp' User-Agent and the 'Sportzfy' package name
headers = {
    "Host": "hotstarlive.nebula-core.workers.dev",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
    "X-Requested-With": "com.cricfytv.sports",
    "Accept-Encoding": "gzip"
}

def fetch_playlist():
    try:
        print("1. Initializing Cloudscraper...")
        # create_scraper tries to mimic a real browser to bypass Cloudflare
        scraper = cloudscraper.create_scraper() 

        print("2. Requesting playlist...")
        response = scraper.get(url, headers=headers)
        
        print(f"3. Server Status: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            if "#EXTM3U" in content:
                with open("iptv.m3u", "w", encoding="utf-8") as f:
                    f.write(content)
                print("✅ Success! Playlist saved to iptv.m3u")
            else:
                print("⚠️ Server sent 200 OK, but content is not M3U.")
                print("Preview:", content[:100])
        else:
            print(f"❌ Failed. Code: {response.status_code}")
            print("Response:", response.text)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":

    fetch_playlist()
