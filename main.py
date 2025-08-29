import json
import os
import re
import requests
from requests.exceptions import (
    ConnectionError,
    Timeout,
    TooManyRedirects,
    HTTPError,
    RequestException
)

from rich.console import Console
from rich.table import Table
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/'
headers = {'User-Agent': 'ObituaryBot/0.0 (ahmedalfraz30@gmail.com) (https://github.com/Alfrazgit/Obituary-Chronicle.git)'}
filename = "data/death.json"


def main():
    name = input('Whose death do you wish to know of? $>').title()
    name = name.replace(' ', '_')

    # Ensure folder exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Load existing data if available, else start empty
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r", encoding="utf-8") as f:
            try:
                loaded = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ JSON file was invalid, starting fresh.")
                loaded = {}
    else:
        loaded = {}

    if name not in loaded:
        find_death(name, loaded)
        display_data(loaded)
    else:
        print(f'{name.replace("_", " ")} is already in our database!')
        display_data(loaded)


def find_death(name, loaded):
    try:
        response = requests.get(url + name, headers=headers, timeout=10)
        response.raise_for_status()  # raises HTTPError for bad responses (4xx/5xx)

        html = response.text
        soup = BeautifulSoup(html, "lxml")

        infobox = soup.find("table", class_="infobox")

        died_cell = infobox.find("th", string="Died")
        if died_cell:
            died = died_cell.find_next_sibling("td").get_text(strip=True)
            loaded[name] = extract_data(died)
            print(died)
        else:
            loaded[name] = {"date": None, "age": None, "location": None}
            print("NOT DEAD YET THANK YOU VERY MUCH!")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(loaded, f, indent=4, ensure_ascii=False)

    except ConnectionError:
        print("❌ Network connection error. Check your internet.")
    except Timeout:
        print("⌛ Request timed out. Wikipedia is too slow or not responding.")
    except TooManyRedirects:
        print("🔁 Too many redirects. The URL might be malformed.")
    except HTTPError as e:
        print(f"⚠️ HTTP error: {e.response.status_code}")
    except RequestException as e:
        print(f"Unexpected error: {e}")


def extract_data(raw):
    parts = [p.strip() for p in raw.split("|")]
    head = parts[0] if parts else ""
    tail = " | ".join(parts[1:]).strip() or None

    # Age
    m_age = re.search(r"\(aged\s*(\d+)\)", head, flags=re.I)
    age = m_age.group(1) if m_age else None

    # Clean date
    date_clean = re.sub(r"\(aged\s*\d+\)", "", head, flags=re.I)
    date_clean = re.sub(r"\(\d{4}-\d{2}-\d{2}\)", "", date_clean)
    date_clean = date_clean.strip(" ,;")
    m_date = re.search(r"(.+?\b\d{4})", date_clean)
    date = m_date.group(1).strip() if m_date else (date_clean or None)

    # Location
    location = tail
    if not location and m_date:
        remainder = date_clean[m_date.end():].strip(" ,;")
        location = remainder or None
    if location:
        location = re.sub(r"\s*,\s*", ", ", location)

    return {"date": date or None, "age": age, "location": location or None}


def display_data(data: dict):
    console = Console()
    table = Table(title="Wikipedia Death Records", style="cyan")

    table.add_column("Name", style="bold magenta", justify="left")
    table.add_column("Date of Death", style="yellow", justify="center")
    table.add_column("Age", style="green", justify="center")
    table.add_column("Location", style="red", justify="left")

    for name, details in data.items():
        date = details.get("date", "N/A")
        age = str(details.get("age", "N/A"))
        location = details.get("location", "N/A")
        table.add_row(name, date, age, location)

    console.print(table)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error:", e)
