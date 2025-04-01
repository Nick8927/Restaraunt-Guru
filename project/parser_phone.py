import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re


async def parse_restaurant_phone_numbers(md_file_path):
    restaurant_links = read_restaurant_links_from_md(md_file_path)  # Читаем ссылки из файла

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",  # Путь к твоему Chrome
            headless=True  # Убираем headless=False, чтобы браузер работал без интерфейса
        )

        for link in restaurant_links:
            try:
                print(f"🔍 Открываю страницу: {link}")

                # Используем новый контекст для каждой страницы
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                    # Указываем User-Agent
                    extra_http_headers={
                        "Accept-Language": "en-US,en;q=0.9"
                    }
                )
                page = await context.new_page()

                if await load_page_with_retry(page, link):  # Попытка загрузки страницы
                    await page.wait_for_selector('a[href^="tel:"]',
                                                 timeout=60000)  # Ожидаем появления блока с телефоном

                    # Получаем HTML-код страницы
                    html = await page.content()
                    soup = BeautifulSoup(html, "html.parser")

                    # Ищем номер телефона в формате <a href="tel:+375447488267">
                    phone_tag = soup.find("a", href=re.compile(r"tel:\+?\d+"))

                    if phone_tag:
                        phone_number = phone_tag.get_text(strip=True)
                        print(f"📞 Найден номер: {phone_number}")
                    else:
                        print(f"⚠️ Не удалось найти телефон на странице {link}")

                    await page.close()  # Закрыть страницу после обработки
                else:
                    print(f"⚠️ Не удалось загрузить страницу {link} после нескольких попыток.")
            except Exception as e:
                print(f"❌ Ошибка при обработке {link}: {e}")

        await browser.close()


async def load_page_with_retry(page, url, retries=3):
    """Попытка загрузки страницы с повтором при ошибке"""
    for attempt in range(retries):
        try:
            print(f"Попытка {attempt + 1} для {url}")
            await page.goto(url, timeout=90000)  # Увеличиваем таймаут на 90 секунд
            await page.wait_for_selector('a[href^="tel:"]', timeout=60000)  # Увеличиваем таймаут до 60 секунд
            return True
        except Exception as e:
            print(f"Попытка {attempt + 1} не удалась для {url}: {e}")
            await asyncio.sleep(5)  # Подождать перед повтором
    return False


def read_restaurant_links_from_md(md_file_path):
    """ Читаем ссылки из markdown-файла """
    links = []
    with open(md_file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.search(r"\[(?:Ссылка|.*?)\]\((https://restaurantguru\.ru/.*?)\)", line)
            if match:
                links.append(match.group(1))
    return links


md_file_path = "restaurants_vitebsk_clean.md"
asyncio.run(parse_restaurant_phone_numbers(md_file_path))
