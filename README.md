📌 Название проекта:
Restaurant-Guru 


📄 Описание
Скрипт парсит информацию о ресторанах Витебска с сайта restaurantguru.ru,
включая название, ID и ссылки. Затем по каждой ссылке извлекается номер телефона.
Результаты сохраняются в Markdown-файлы.


🚀 Технологии
Python 3.10+
Playwright (async API)
BeautifulSoup4
re (регулярные выражения)
Markdown-файлы для вывода
asyncio
webdriver_manager
(перечень всех зависимостей указан в req.txt)


⚙️ Установка и запуск
1. Клонирование проекта:
git clone https://github.com/Nick8927/Restaraunt-Guru
cd директора проекта
2. Создание и активация виртуального окружения:
python -m venv venv
venv\Scripts\activate   # для Windows
3. Установка зависимостей:
pip install -r req.txt
4. Установка браузеров для Playwright (обязательно!):
playwright install
5. Запуск парсинга:
python main.py


📁 Структура проекта
RestaurantGuru/
├── parsers/
│   ├── __init__.py
│   ├── parser.py              # Сбор ссылок на рестораны
│   └── final_parsing.py       # Итоговый парсинг 
├── pre_data/                  # Промежуточные данные
├── output_files/              # Результирующие данные
├── main.py                    # Запуск
├── req.txt
├── .gitignore
└── README.md
*не указаны файлы, которые не нужны при финальном запуске

👨‍💻 Автор
GitHub: https://github.com/Nick8927


