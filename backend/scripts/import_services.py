import re

import requests
from bs4 import BeautifulSoup

from app.database import SessionLocal
from app.models import Service


URL = "https://tamirat.info/تعمیرگاه-خودرو-در-تهران/"


def clean_text(text: str) -> str:
    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def parse_price(price_text: str):
    """
    تبدیل:

    ۱٬۲۰۰٬۰۰۰ تا ۱٬۸۰۰٬۰۰۰

    به:

    1200000
    1800000
    """

    numbers = re.findall(
        r"\d[\d٬,]*",
        price_text
    )

    numbers = [
        number
        .replace("٬", "")
        .replace(",", "")
        for number in numbers
    ]

    numbers = [
        int(number)
        for number in numbers
    ]

    if len(numbers) >= 2:
        return numbers[0], numbers[1]

    if len(numbers) == 1:
        return numbers[0], numbers[0]

    return None, None


def scrape_services():

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

    if len(tables) < 2:
        raise Exception(
            "Services table not found"
        )

    service_table = tables[1]

    rows = service_table.find_all("tr")

    services = []

    for row in rows[1:]:

        columns = row.find_all("td")

        if len(columns) < 4:
            continue

        name = clean_text(
            columns[0].get_text(
                " ",
                strip=True
            )
        )

        description = clean_text(
            columns[1].get_text(
                " ",
                strip=True
            )
        )

        price = clean_text(
            columns[2].get_text(
                " ",
                strip=True
            )
        )

        duration = clean_text(
            columns[3].get_text(
                " ",
                strip=True
            )
        )

        price_min, price_max = parse_price(
            price
        )

        services.append({
            "name": name,
            "description": description,
            "price_min": price_min,
            "price_max": price_max,
            "duration": duration,
        })

    return services


def service_exists(db, service_data):

    service = db.query(Service).filter(
        Service.name == service_data["name"]
    ).first()

    return service is not None


def save_services(services):

    db = SessionLocal()

    added_count = 0
    skipped_count = 0

    try:

        for service_data in services:

            if service_exists(
                db,
                service_data
            ):

                print(
                    f"Already exists: "
                    f"{service_data['name']}"
                )

                skipped_count += 1

                continue

            service = Service(
                name=service_data["name"],
                description=service_data["description"],
                price_min=service_data["price_min"],
                price_max=service_data["price_max"],
                duration=service_data["duration"],
            )

            db.add(service)

            added_count += 1

            print(
                f"Added: {service_data['name']}"
            )

        db.commit()

        print()
        print("-" * 50)
        print(
            f"New services added: {added_count}"
        )
        print(
            f"Existing services skipped: "
            f"{skipped_count}"
        )

    except Exception as e:

        db.rollback()

        print(
            f"Error while saving services: {e}"
        )

    finally:

        db.close()


def main():

    print("Starting service scraper...")

    services = scrape_services()

    print(
        f"Found {len(services)} services"
    )

    print("-" * 50)

    save_services(services)


if __name__ == "__main__":
    main()