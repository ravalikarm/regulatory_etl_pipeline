import requests
from bs4 import BeautifulSoup
import json
from io import BytesIO
from pdfminer.high_level import extract_text
import re
from datetime import datetime

def extract_pdf_text(pdf_url):
    try:
        response = requests.get(pdf_url, timeout=15)
        response.raise_for_status()
        with BytesIO(response.content) as pdf_file:
            return extract_text(pdf_file).strip()
    except Exception as e:
        print(f"⚠️ Failed to extract PDF text from {pdf_url}: {e}")
        return None

def extract_date_from_text(text):
    try:
        match = re.search(r"(?:Date:\s*)?([A-Z][a-z]+ \d{1,2}, \d{4})", text)
        if match:
            dt = datetime.strptime(match.group(1), "%B %d, %Y")
            return dt.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"⚠️ Failed to parse date: {e}")
    return "unknown"

URL = "https://www.tceq.texas.gov/rules/prop.html"
response = requests.get(URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

proposed_rules = []
table = soup.find('table')
if table:
    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 3:
            identifier = cols[0].get_text(strip=True)
            title = cols[1].get_text(strip=True)
            doc_links = cols[2].find_all('a')
            source_url = None
            for link_tag in doc_links:
                if 'href' in link_tag.attrs:
                    source_url = link_tag['href']
                    if source_url.startswith('/'):
                        source_url = f"https://www.tceq.texas.gov{source_url}"
                    break
            full_text = extract_pdf_text(source_url) if source_url else None
            date_proposed = extract_date_from_text(full_text) if full_text else "unknown"
            proposed_rules.append({
                "identifier": identifier,
                "title": title,
                "date_proposed": date_proposed,
                "source_url": source_url,
                "full_text": full_text
            })

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(proposed_rules, f, indent=2)

print(f"\n✅ Done. Extracted {len(proposed_rules)} rules with real proposal dates.")
print("📁 Output written to output.json")
