from playwright.async_api import async_playwright


async def open_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Открываем браузер
        page = await browser.new_page()

        url = "https://restaurantguru.ru/Pushkin-Times-Viciebsk"
        print(f"🔍 Открываю страницу: {url}")
        await page.goto(url)

        input("⏳ Проверь страницу вручную. Если номер есть — нажми Enter...")
        await browser.close()


import asyncio

asyncio.run(open_page())
