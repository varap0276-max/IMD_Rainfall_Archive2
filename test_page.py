import requests

url = "https://mausam.imd.gov.in/responsive/rainfall_statistics.php?PAGE=4"

response = requests.get(url)

print("=" * 60)
print("STATUS CODE")
print("=" * 60)

print(response.status_code)

print()

print("=" * 60)
print("FIRST 5000 CHARACTERS")
print("=" * 60)

with open("page.html", "w", encoding="utf-8") as file:
    file.write(response.text)

print("HTML saved.")