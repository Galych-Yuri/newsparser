from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


# Функція для збору новин з сайту
def get_ssu_news_from_page(url):
    # Налаштування для Selenium
    options = webdriver.ChromeOptions()
    options.headless = True  # Без відкриття вікна браузера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)

    driver.get(url)
    sleep(3)  # Чекаємо, поки завантажиться сторінка

    # Збираємо всі новини з таблиці
    news_items = driver.find_elements(By.XPATH,
                                      "//article")  # Шукаємо всі теги article
    news_data = []

    for item in news_items:
        try:
            # Отримуємо дату новини
            date = item.find_element(By.XPATH, ".//span").text
            # Отримуємо посилання на новину
            link = item.find_element(By.XPATH, ".//a[2]").get_attribute("href")
            # Отримуємо текст новини
            title = item.find_element(By.XPATH, ".//a[2]").text

            # Якщо всі елементи знайдені, додаємо новину в список
            if date and link and title:
                news_data.append((date, link, title))
        except Exception as e:
            print(f"Помилка при обробці елемента: {e}")

    driver.quit()
    return news_data


# Функція для запису новин у файл, перевіряючи на дублікати
def save_ssu_news_to_file(news_data, filename="ssu.txt"):
    # Завантажуємо вже існуючі новини з файлу
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            existing_news = set(line.strip() for line in file)
    except FileNotFoundError:
        existing_news = set()

    # Записуємо нові новини, якщо їх ще немає
    with open(filename, 'a', encoding='utf-8') as file:
        for date, link, title in news_data:
            news_entry = f"{date} - {title} - {link}"
            if news_entry not in existing_news:
                file.write(f"{news_entry}\n")
                existing_news.add(news_entry)


# Збираємо новини зі сторінки
url = "https://ssu.gov.ua/novyny?regions%5B%5D=odesa-region"
news_data = get_ssu_news_from_page(url)
save_ssu_news_to_file(news_data)
