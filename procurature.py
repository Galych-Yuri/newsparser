import requests
from bs4 import BeautifulSoup

# URL сайту
url = "https://od.gp.gov.ua/ua/news.html"

# Шлях до файлу для запису новин
file_path = "procurature.txt"


# Функція для перевірки, чи новина вже є в файлі
def is_duplicate(news, file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # Перевіряємо, чи є новина в файлі
            file_content = file.read()
            if news in file_content:
                return True
            return False
    except FileNotFoundError:
        # Якщо файл не знайдений, повертаємо False (файл ще не існує)
        return False


# Функція для запису новин у файл
def write_news_to_file(news, file_path):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(news + "\n")


# Виконуємо запит до сайту
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    # Знаходимо головний блок із новинами
    news_section = soup.select_one(
        "section > section:nth-of-type(2) > section")

    if news_section:
        # Обробляємо всі елементи <li> всередині блоку
        for item in news_section.select("section > section > ul > li"):
            # Посилання на новину
            link_tag = item.select_one("a")
            if link_tag and link_tag.get("href"):
                link = link_tag['href']
                full_link = f"https://od.gp.gov.ua{link}" if link.startswith(
                    "/") else link

                # Дата новини
                date_span = item.select_one("a > p > b > span")
                date = date_span.get_text(
                    strip=True) if date_span else "Без дати"

                # Текст новини
                text_node = item.select_one("a > p:nth-of-type(1)")
                text = text_node.get_text(
                    strip=True) if text_node else "Без тексту"

                # Формуємо повне повідомлення
                news = f"Дата: {date}\nТекст: {text}\nПосилання: {full_link}"

                # Перевіряємо на дублікати
                if not is_duplicate(news, file_path):
                    # Якщо новина не знайдена в файлі, записуємо її
                    write_news_to_file(news, file_path)
                    print(f"Новину додано: {news}")
                else:
                    print(f"Дублікати не додано: ")
    else:
        print("Не знайдено блок із новинами.")
else:
    print(f"Не вдалося отримати сторінку. Статус-код: {response.status_code}")
