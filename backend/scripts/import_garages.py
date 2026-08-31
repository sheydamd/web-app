import re

import requests
from bs4 import BeautifulSoup

from app.database import SessionLocal
from app.models import Garage


URL = "https://tamirat.info/تعمیرگاه-خودرو-در-تهران/"


def clean_name(name: str) -> str:
    name = name.strip()

    name = re.sub(
        r"^\d+\.\s*",
        "",
        name
    )

    return name


def clean_text(text: str) -> str:
    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def clean_address(address: str) -> str:
    address = clean_text(address)

    words = address.split()

    if len(words) % 2 == 0:
        middle = len(words) // 2

        first_half = words[:middle]
        second_half = words[middle:]

        if first_half == second_half:
            return " ".join(first_half)

    return address


def scrape_garages():
    response = requests.get(
        URL,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    tables = soup.find_all("table")

    if not tables:
        raise Exception("No tables found on the page")

    garage_table = tables[0]

    rows = garage_table.find_all("tr")

    garages = []

    for row in rows[1:]:

        columns = row.find_all("td")

        if len(columns) < 3:
            continue

        name = columns[0].get_text(
            " ",
            strip=True
        )

        address = columns[1].get_text(
            " ",
            strip=True
        )

        phone = columns[2].get_text(
            " ",
            strip=True
        )

        garages.append({
            "name": clean_name(name),
            "address": clean_address(address),
            "phone": clean_text(phone),
        })

    return garages


def garage_exists(db, garage_data):
    """
    بررسی می‌کند آیا تعمیرگاه قبلاً
    در دیتابیس وجود دارد یا نه.
    """

    garage = db.query(Garage).filter(
        Garage.name == garage_data["name"],
        Garage.phone == garage_data["phone"]
    ).first()

    return garage is not None


def save_garages(garages):

    db = SessionLocal()

    added_count = 0
    skipped_count = 0

    try:

        for garage_data in garages:

            if garage_exists(db, garage_data):

                print(
                    f"Already exists: {garage_data['name']}"
                )

                skipped_count += 1

                continue

            garage = Garage(
                name=garage_data["name"],
                address=garage_data["address"],
                phone=garage_data["phone"],
                city="تهران",
                rating=0,
                review_count=0,
                source="tamirat.info"
            )

            db.add(garage)

            added_count += 1

            print(
                f"Added: {garage_data['name']}"
            )

        db.commit()

        print()
        print("-" * 50)
        print(f"New garages added: {added_count}")
        print(f"Existing garages skipped: {skipped_count}")

    except Exception as e:

        db.rollback()

        print(
            f"Error while saving garages: {e}"
        )

    finally:

        db.close()


def main():

    print("Starting scraper...")

    garages = scrape_garages()

    print(
        f"Found {len(garages)} garages"
    )

    print("-" * 50)

    save_garages(garages)


if __name__ == "__main__":
    main()