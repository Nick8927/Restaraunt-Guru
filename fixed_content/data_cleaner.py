import re


def clean_restaurant_md(input_file="restaurants_vitebsk.md", output_file="restaurants_vitebsk_clean.md"):
    """Чистит Markdown-файл, оставляя только ID, название и ссылку без дублирования."""

    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        lines = infile.readlines()

        outfile.write("# 📌 Список ресторанов Витебска\n\n")
        outfile.write("| №  | Название | ID | Ссылка |\n")
        outfile.write("|----|----------|----|--------|\n")

        for line in lines:
            parts = line.strip().split("|")
            if len(parts) < 5 or not parts[1].strip().isdigit():
                continue

            idx = parts[1].strip()
            raw_name = parts[2].strip()
            restaurant_id = parts[3].strip()
            raw_link = parts[4].strip()

            name_match = re.search(r'\(\("([^"]+)",\s*"([^"]+)"\)\)', raw_name)
            link_match = re.search(r'https?://[^\s)"]+', raw_link)

            if name_match:
                url, name = name_match.groups()
            else:
                name = raw_name if raw_name else "Неизвестно"
                url = link_match.group(0) if link_match else "#"

            url = url.strip().strip('",')

            markdown_link = f"[{name}]({url})"
            outfile.write(f"| {idx} | {markdown_link} | {restaurant_id} | [Ссылка]({url}) |\n")

    print(f"✅ Данные очищены и сохранены в {output_file}")

# clean_restaurant_md()
