import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

path_to_file = r"/parsers/restaurants_vitebsk_clean.md"
INPUT_FILE = path_to_file
OUTPUT_FILE = "restaurants_vitebsk_with_phones.md"


async def fetch_page(session, url):
    """Асинхронно загружает страницу ресторана."""
    try:
        async with session.get(url, timeout=10) as response:
            text = await response.text()
            print(f"✅ Загружена страница: {url}")  # Отладка
            return text
    except Exception as e:
        print(f"❌ Ошибка загрузки {url}: {e}")
        return None


async def get_phone(session, url):
    """Извлекает номер телефона со страницы ресторана."""
    html = await fetch_page(session, url)
    if not html:
        return "Нет данных"

    soup = BeautifulSoup(html, "html.parser")

    with open("debug_page.html", "w", encoding="utf-8") as f:
        f.write(html)

    phone_element = soup.select_one("div#call_wrap a.call span")
    if phone_element:
        return phone_element.text.strip()

    print(f"⚠️ Телефон не найден на странице: {url}")
    return "Нет данных"


async def parse_restaurant_phones():
    """Парсит номера телефонов ресторанов из файла и сохраняет в новый файл."""
    restaurants = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        with open(INPUT_FILE, "r", encoding="utf-8-sig") as file:
            for line in file:
                # Выведем строки, чтобы убедиться, что файл читается
                print(f"🔍 Читаем строку: {line.strip()}")

                match = re.match(
                    r'\|\s*(\d+)\s*\|\s*\[\[(.+?)\]\((https?://[^\s]+)\)\]\((https?://[^\s]+)\)\s*\|\s*([\w-]+)\s*\|',
                    line,
                )
                if match:
                    idx, name, display_link, real_link, rest_id = match.groups()
                    print(f"✅ Найдено: {idx}, {name}, {real_link}, {rest_id}")  # Отладка

                    tasks.append(get_phone(session, real_link))
                    restaurants.append((idx, name, real_link, rest_id))
                else:
                    print(f"⚠️ Не удалось распарсить строку: {line.strip()}")

        if not restaurants:
            print("❌ Не найдено ни одной корректной строки. Проверь формат файла!")
            return

        phones = await asyncio.gather(*tasks)

    with open(OUTPUT_FILE, "w", encoding="utf-8-sig") as file:
        file.write("# 📌 Список ресторанов Витебска с телефонами\n\n")
        file.write("| №  | Название | ID | Ссылка | Телефон |\n")
        file.write("|----|----------|----|--------|---------|\n")

        for (idx, name, link, rest_id), phone in zip(restaurants, phones):
            file.write(f"| {idx} | [{name}]({link}) | {rest_id} | {link} | {phone} |\n")

    print(f"✅ Данные с телефонами сохранены в {OUTPUT_FILE}")


# if __name__ == "__main__":
#     asyncio.run(parse_restaurant_phones())
