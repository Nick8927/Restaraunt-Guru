import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
import os


"""
Модуль для асинхронного парсинга номеров телефонов ресторанов из списка ссылок.

Основной функционал:
- Чтение списка ресторанов из файла restaraunt_vitebsk_clean (результат работы модуля parser).
- Использование Playwright для загрузки страниц.
- Извлечение номеров телефонов и названий ресторанов.
- Обработка ошибок и повторные попытки загрузки.
- Сохранение результатов в markdown-файл.

Запуск:
```python
asyncio.run(parse_restaurant_phone_numbers("restaurants_vitebsk_clean.md", "restaurant_phones.md"))"""


output_dir = "output_files"
os.makedirs(output_dir, exist_ok=True)

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output_files"))


async def parse_restaurant_phone_numbers(md_file_path, output_file):
    """
    Асинхронно парсит номера телефонов ресторанов из списка ссылок в restaraunts_vitebsk_clean файле
     и сохраняет результат.
    """
    restaurant_links = read_restaurant_links_from_md(md_file_path)

    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )

        for index, (name, link) in enumerate(restaurant_links, start=1):
            try:
                print(f"🔍 [{index}] Открываю страницу: {name} ({link})")
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                    extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
                )
                page = await context.new_page()

                if await load_page_with_retry(page, link):
                    html = await page.content()
                    soup = BeautifulSoup(html, "html.parser")
                    phone_tag = soup.find("a", href=re.compile(r"tel:\+?\d+"))

                    if phone_tag:
                        phone_number = phone_tag.get_text(strip=True)
                        print(f"📞 [{index}] Найден номер: {phone_number}")
                        clean_name = name.strip("[]")  # убираем скобки из исх.файла
                        results.append(f"{index}. **{clean_name}**: {phone_number}")
                    else:
                        print(f"⚠️ [{index}] Номер телефона не найден")
                        results.append(f"{index}. **{clean_name}**: ❌ Номер телефона не найден")

                    await page.close()
                else:
                    print(f"⚠️ [{index}] Не удалось загрузить страницу {name}")
                    results.append(f"{index}. **{clean_name}**: ❌ Страница недоступна")

            except Exception as e:
                print(f"❌ [{index}] Ошибка при обработке {name}: {e}")
                results.append(f"{index}. **{clean_name}**: ❌ Ошибка при обработке")

        await browser.close()

    save_results_to_md(output_file, results)
    print(f"✅ Результаты сохранены в {output_file}")


async def load_page_with_retry(page, url, retries=2):
    """
    Попытка загрузки страницы с повтором при ошибке.
    """
    for attempt in range(retries):
        try:
            print(f"Попытка {attempt + 1} для {url}")
            await page.goto(url, timeout=90000)
            await page.wait_for_selector('a[href^="tel:"]', timeout=60000)
            return True
        except Exception as e:
            print(f"Попытка {attempt + 1} не удалась для {url}: {e}")
            await asyncio.sleep(5)
    return False


def read_restaurant_links_from_md(md_file_path):
    """
    Читает ссылки на рестораны из markdown-файла.
    """
    links = []
    with open(md_file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.search(r"\[(.*?)\]\((https://restaurantguru\.ru/.*?)\)", line)
            if match:
                links.append((match.group(1), match.group(2)))
    return links


def save_results_to_md(output_file, results):
    """
    Сохраняет результаты парсинга в parsed_phone_numbers.md файл.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("# Найденные номера телефонов ресторанов\n\n")
        file.write("\n".join(results))


def main():
    md_file_path = "restaurants_vitebsk_clean.md"
    output_file = os.path.join(output_dir, "parsed_phone_numbers.md")
    asyncio.run(parse_restaurant_phone_numbers(md_file_path, output_file))



if __name__ == "__main__":
    main()
