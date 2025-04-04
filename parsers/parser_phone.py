import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re


async def parse_restaurant_phone_numbers(md_file_path, output_file_path):
    """
    Функция для извлечения номеров телефонов с сайта restaurantguru.ru из ссылок, указанных в markdown файле.

    Аргументы:
    md_file_path (str): Путь к markdown файлу с ссылками на страницы ресторанов.
    output_file_path (str): Путь к markdown файлу для сохранения найденных номеров телефонов.
    """
    restaurant_links = read_restaurant_links_from_md(md_file_path)

    phone_numbers = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )

        for link in restaurant_links:
            try:
                print(f"🔍 Открываю страницу: {link}")

                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                    extra_http_headers={
                        "Accept-Language": "en-US,en;q=0.9"
                    }
                )
                page = await context.new_page()

                if await load_page_with_retry(page, link):
                    await page.wait_for_selector('a[href^="tel:"]', timeout=60000)

                    html = await page.content()
                    soup = BeautifulSoup(html, "html.parser")

                    phone_tag = soup.find("a", href=re.compile(r"tel:\+?\d+"))

                    if phone_tag:
                        phone_number = phone_tag.get_text(strip=True)
                        print(f"📞 Найден номер: {phone_number}")
                        phone_numbers.append(f"- {phone_number}\n")  # Добавляем номер в список
                    else:
                        print(f"⚠️ Не удалось найти телефон на странице {link}")

                    await page.close()
                else:
                    print(f"⚠️ Не удалось загрузить страницу {link} после нескольких попыток.")
            except Exception as e:
                print(f"❌ Ошибка при обработке {link}: {e}")

        await browser.close()

    save_phone_numbers_to_md(output_file_path, phone_numbers)


def save_phone_numbers_to_md(output_file_path, phone_numbers):
    """
    Сохраняет найденные номера телефонов в md файл.

    Аргументы:
    output_file_path : Путь к md файлу для сохранения номеров.
    phone_numbers : Список найденных номеров телефонов.
    """
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write("# Найденные номера телефонов ресторанов\n\n")
        file.writelines(phone_numbers)


async def load_page_with_retry(page, url, retries=3):
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
    Читает ссылки на страницы ресторанов из markdown файла.
    """

    links = []
    with open(md_file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.search(r"\[(?:Ссылка|.*?)\]\((https://restaurantguru\.ru/.*?)\)", line)
            if match:
                links.append(match.group(1))
    return links


# md_file_path = "restaurants_vitebsk_clean.md"
# output_file_path = "restaurant_phone_numbers.md"
# asyncio.run(parse_restaurant_phone_numbers(md_file_path, output_file_path))
