from project.parser import parse_restaurants, save_to_csv
from project.data_cleaner import clean_restaurant_data

if __name__ == "__main__":
    print("🚀 Запуск парсинга ресторанов...")
    restaurants = parse_restaurants()

    print("\n💾 Сохранение данных...")
    save_to_csv(restaurants)

    print("\n🔄 Очистка и форматирование данных...")
    clean_restaurant_data()

    print("\n🎉 Готово! Данные сохранены в restaurants_vitebsk_clean.csv")
