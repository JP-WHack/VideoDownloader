import requests
from tqdm import tqdm
import os
import urllib.parse

# 🎯 ユーザーにURLを入力してもらう
url = input("🎯 動画のURLを入力: ").strip()

# 📂 ファイル名をURLから取得（ファイル名がなければデフォルト）
filename = os.path.basename(urllib.parse.urlparse(url).path) or "download.mp4"
start_byte = os.path.getsize(filename) if os.path.exists(filename) else 0
mode = "ab" if start_byte > 0 else "wb"

# 🔧 ヘッダー設定（レジューム対応）
headers = {
    "Range": f"bytes={start_byte}-",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 📡 リクエスト送信
response = requests.get(url, headers=headers, stream=True)
if response.status_code not in [200, 206]:
    print(f"❌ ダウンロード失敗！ステータス: {response.status_code}")
    exit()

# 📊 総ファイルサイズ（プログレスバー用）
total_size = int(response.headers.get("content-length", 0)) + start_byte

# 💾 ダウンロード＆保存
with open(filename, mode) as f:
    with tqdm(total=total_size, initial=start_byte, unit="B", unit_scale=True, desc=f"📥 {filename}") as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))

print("🎉 ダウンロード完了")
