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

def safe_find(parent, name=None, many=False, error_prefix=None, **kwargs):
    """
    Универсальный поиск по BeautifulSoup с авто-логированием ошибок.
    Если many=True — работает как find_all, иначе как find.
    """
    finder = parent.find_all if many else parent.find
    result = finder(name, **kwargs)
    need_log = (not result if many else result is None)
    if need_log:
        attrs_desc = ', '.join(f"{k}={v!r}" for k, v in kwargs.items())
        msg = f"Не найдено элементов" if many else f"Не найден элемент"
        details = f"<{name or ''} {attrs_desc}>".strip()
        prefix = f"{error_prefix} " if error_prefix else ""
        print(f"{prefix}{msg}: {details}")
    return result


def parse_page(url):
    try: 
        resp = requests.get(url)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, 'html.parser')

        # Вся информация о животных находится внутри этого div
        pages_div = safe_find(soup, 'div', id='mw-pages')
        if not pages_div:
            return None

        # Животные на одну букву объединены в группы, на странице может быть одна или несколько групп 
        groups = safe_find(pages_div, 'div', class_='mw-category-group', many=True)

        for group in groups:
            # В начале группы находится заголовок с буквой
            h3 = safe_find(group, 'h3')
            if not h3:
                continue
            letter = h3.text.strip()
            
            # Каждое название животного является элементом списка
            items = safe_find(group, 'li', many=True)
            if not items:
                continue
            count = len(items)
            
            if letter not in beasts:
                beasts[letter] = 0
            beasts[letter] += count

        # Переход к следующей странице
        next_link = safe_find(pages_div, 'a', string='Следующая страница')
        if next_link:
            return BASE_URL + next_link['href']
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса {url}: {e}")
    except Exception as e:
        print(f"Ошибка парсинга страницы {url}: {e}")
    
    return None


def save_to_file():
    try: 
        with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for letter, count in beasts.items():
                writer.writerow([letter, count])
    except Exception as e:
        print("Не удалось сохранить файл {OUTPUT_FILE}:", e)
    

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
