from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def setup_driver():
    """Настройка и запуск Selenium WebDriver."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def parse_restaurants():
    """Парсит список ресторанов и возвращает данные в виде списка словарей."""
    driver = setup_driver()
    url = 'https://restaurantguru.ru/Viciebsk'
    driver.get(url)
    time.sleep(7)

    # Прокрутка страницы
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    restaurants = []
    restaurant_cards = driver.find_elements(By.CLASS_NAME, "rest_info")

    if not restaurant_cards:
        print("❌ Ошибка: Элементы с классом 'rest_info' не найдены!")
        driver.quit()
        return []

    for card in restaurant_cards:
        try:
            name = card.find_element(By.CLASS_NAME, "title").text.strip()
            link = card.find_element(By.CLASS_NAME, "title").get_attribute("href")
            restaurant_id = link.split("/")[-1] if link else "N/A"
        except:
            continue

        restaurants.append({"Название": name, "ID": restaurant_id})

    driver.quit()
    return restaurants

def save_to_csv(data, output_file="restaurants_vitebsk.csv"):
    """Сохраняет список ресторанов в CSV-файл."""
    if not data:
        print("❌ Нет данных для сохранения!")
        return

    with open(output_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=["Название", "ID"])
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Данные успешно сохранены в {output_file}")
