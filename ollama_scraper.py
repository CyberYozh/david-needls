#part 1
# sudo apt update
# curl -fsSL https://ollama.com/install.sh | sh
# ollama run phi3

# python3 -m venv env
# pip install requests beautifulsoup4


import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "phi3",
        "prompt": "Say hello",
        "stream": False
    }
)


data = response.json()

print(data)
print("\n")
print(data["response"])


#part 2

import requests
from bs4 import BeautifulSoup

url = "https://example.com"

headers = {
    "User-Agent": "Mozilla/5.0"
}



html = requests.get(url, headers=headers).text


soup = BeautifulSoup(html, "html.parser")

for tag in soup(["script", "style", "noscript"]):
    tag.decompose()

text = soup.get_text(separator="\n")

text = "\n".join(
    line.strip()
    for line in text.splitlines()
    if line.strip()
)

text = text[:5000]


prompt = f"""
Extract useful information from this webpage.

Return JSON only.

Example:
{{
  "title": "",
  "products": [],
  "prices": []
}}

WEBPAGE:

{text}
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }
)

result = response.json()["response"]

print(result)
