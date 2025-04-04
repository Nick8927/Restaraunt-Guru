from playwright.async_api import async_playwright
import asyncio


async def open_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        url = "https://restaurantguru.ru/Pushkin-Times-Viciebsk"
        print(f"🔍 Открываю страницу: {url}")
        await page.goto(url)

        input("⏳ Проверка страницы. Если номер есть — жми Enter...")
        await browser.close()


# asyncio.run(open_page())
