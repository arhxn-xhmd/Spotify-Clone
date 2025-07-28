import requests, os, time

API_KEY = "AHqYlFVpJdTM0QNtxp8fx4POX2S8RcatenG5Fw2I"
headers = {"Authorization": f"Token {API_KEY}"}
query = "angry"
per_page = 20
page = 1
count = 0
target = 100

os.makedirs("angry mood", exist_ok=True)

while count < target:
    url = f"https://freesound.org/apiv2/search/text/?query={query}&fields=id,name,previews&filter=duration:[5 TO 120]&page={page}&page_size={per_page}"
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print("Error:", res.status_code, res.text)
        break

    data = res.json()
    results = data.get("results", [])

    if not results:
        print("No more results found.")
        break

    for sound in results:
        if count >= target:
            break
        try:
            mp3_url = sound["previews"]["preview-hq-mp3"]
            filename = f"{str(count + 1).zfill(3)} - {sound['name'].replace('/', '_')}.mp3"
            print(f"Downloading {filename} ...")
            mp3_data = requests.get(mp3_url).content
            with open(os.path.join("songs", filename), "wb") as f:
                f.write(mp3_data)
            count += 1
            time.sleep(0.5)  
        except Exception as e:
            print("Skipping one due to error:", e)

    page += 1

print(f"✅ Downloaded {count} 'angry' songs into './songs'")
