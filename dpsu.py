from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

status = 'не використано'
status_done = 'використано'

# Функція для збору новин з сайту
def get_dpsu_news_from_page(url):
    # Налаштування для Selenium
    options = webdriver.ChromeOptions()
    options.headless = True  # Без відкриття вікна браузера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)

    driver.get(url)
    sleep(10)  # Чекаємо, поки завантажиться сторінка

    # Збираємо всі новини
    news_items = driver.find_elements(By.XPATH, '//*[@id="col-lg-8"]/div/a')
    news_data = []

    for item in news_items:
        try:
            # Отримуємо текст новини
            title = item.find_element(By.XPATH, './div[2]/div[2]').text.strip()
            # Отримуємо дату новини
            date = item.find_element(By.XPATH,
                                     './div[2]/div[1]/div').text.strip()
            # Отримуємо посилання на новину
            link = item.get_attribute("href")

            # Додаємо новину до списку
            if title and date and link:
                news_data.append((date, title, link))
        except Exception as e:
            print(f"Помилка при обробці елемента: {e}")

    driver.quit()
    return news_data


# Функція для запису новин у файл, перевіряючи на дублікати
def save_dpsu_news_to_file(news_data, filename="dpsu.txt"):
    # Завантажуємо вже існуючі новини з файлу
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            existing_news = set(line.strip() for line in file)
    except FileNotFoundError:
        existing_news = set()

    # Записуємо нові новини, якщо їх ще немає
    with open(filename, 'a', encoding='utf-8') as file:
        for date, title, link in news_data:
            news_entry = f"{date}\n{title}\n{link}\n{status}\n{'_'*50}"
            if news_entry not in existing_news:
                file.write(f"{news_entry}\n")
                existing_news.add(news_entry)


# Збираємо новини зі сторінки
url = "https://dpsu.gov.ua/ua/events?page=1"
news_data = get_dpsu_news_from_page(url)
save_dpsu_news_to_file(news_data)

