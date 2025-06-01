import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = 'https://ru.wikipedia.org'
CATEGORY_URL = BASE_URL + '/wiki/Категория:Животные_по_алфавиту'
OUTPUT_FILE = 'task2/beasts.csv'
DELAY = 0.5  # Чтобы не спамить запросы



ALPHABET = [chr(x) for x in range(ord('А'), ord('Я')+1)]  # А-Я
beasts = {letter: 0 for letter in ALPHABET}

def parse_page(url):
    try: 
        resp = requests.get(url)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, 'html.parser')

        pages_div = soup.find('div', id='mw-pages')
        if not pages_div:
            return None

        # Все div с классом mw-category-group
        groups = pages_div.find_all('div', class_='mw-category-group')

        for group in groups:
            # Ищем букву
            h3 = group.find('h3')
            if h3:
                letter = h3.text.strip()
                # Считаем элементы списка
                count = len(group.find_all('li'))
                if letter not in beasts:
                    beasts[letter] = 0
                beasts[letter] += count
        # Переход к следующей странице
        next_link = pages_div.find('a', string='Следующая страница')
        if next_link:
            return BASE_URL + next_link['href']
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса {url}: {e}")
    except Exception as e:
        print(f"Ошибка парсинга страницы {url}: {e}")
    
    return None


def save_to_file():
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for letter, count in beasts.items():
            writer.writerow([letter, count])
    

def main():
    url = CATEGORY_URL
    page_num = 1
    while url:
        print(f'Парсим страницу {page_num}: {url}')
        url = parse_page(url)
        page_num += 1
        time.sleep(DELAY)  
    save_to_file()
    print('Готово!')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Критическая ошибка:", e)
        raise
