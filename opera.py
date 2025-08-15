from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def get_opera_afisha(url, file_path):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)

        # Чекаємо на завантаження блоку .tickets
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.tickets'))
        )

        # Знаходимо всі новини
        news_elements = driver.find_elements(By.CSS_SELECTOR,
                                             '.tickets__day .ticket-item')
        news = []

        for element in news_elements:
            try:
                # Знаходимо дату
                day = element.find_element(By.CSS_SELECTOR,
                                           '.ticket__date .ticket__day').text.strip()
                month = element.find_element(By.CSS_SELECTOR,
                                             '.ticket__date .ticket__month').text.strip()
                date = f"{day} {month}"

                # Знаходимо назву та посилання
                title_element = element.find_element(By.CSS_SELECTOR,
                                                     '.ticket__title a')
                title = title_element.text.strip()
                link = title_element.get_attribute('href')

                event_info = f"{date}\n{title}\n{link}"
                add_to_file_if_not_duplicate(file_path, event_info)
                news.append(event_info)
            except Exception as e:
                print(f"Помилка при обробці елемента: {e}")

        return news

    finally:
        driver.quit()


def add_to_file_if_not_duplicate(file_path, data):
    """
    Записує дані у файл, якщо таких даних ще немає.

    :param file_path: шлях до файлу
    :param data: рядок, який треба записати
    """
    try:
        with open(file_path, 'r') as file:
            existing_data = set(line.strip() for line in file)
    except FileNotFoundError:
        existing_data = set()

    if data not in existing_data:
        with open(file_path, 'a') as file:
            file.write(data + '\n')
        print(f"Додано: {data}")
    else:
        print(f"Дублікат: {data}")


# Приклад виклику функції
url = "https://operahouse.od.ua/afisha"  
file_path = "opera.txt"  # Шлях до файлу для збереження даних
afisha_data = get_opera_afisha(url, file_path)

print("\n".join(afisha_data))
