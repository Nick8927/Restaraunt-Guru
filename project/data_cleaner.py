import csv

def clean_restaurant_data(input_file="restaurants_vitebsk.csv", output_file="restaurants_vitebsk_clean.csv"):
    with open(input_file, "r", encoding="utf-8-sig") as infile, open(output_file, "w", newline="", encoding="utf-8-sig") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        headers.insert(0, "ID")
        writer.writerow(headers)

        for idx, row in enumerate(reader, start=1):
            if len(row) < 2 or not row[0].strip():
                continue
            writer.writerow([idx] + row)

    print(f" Данные структурированы и сохранены в {output_file}")
