
import requests
from bs4 import BeautifulSoup

url = "https://www.neoseeker.com/rune-factory-5/Cooking_Recipe_List"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    url,
    headers=headers,
    timeout=20
)

print("Status:", response.status_code)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    print(soup.title.get_text())
    
    tables = soup.find_all("table")
    print("Jumlah tabel:", len(tables))
