import pytest
import requests
from bs4 import BeautifulSoup
import builtins
import os

import sys
sys.path.append('task2')  

import solution  

# Мок для requests.get
class MockResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code
    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(f"HTTP {self.status_code}")

# Тестовый HTML с одной буквой (Ю)
HTML_ONE_GROUP = '''
<div id="mw-pages">
    <div class="mw-category-group">
        <h3>Ю</h3>
        <ul>
            <li>Животное1</li>
            <li>Животное2</li>
        </ul>
    </div>
    <a href="/wiki/Категория:Животные_по_алфавиту?from=B" >Следующая страница</a>
</div>
'''

# Тестовый HTML без нужных селекторов
HTML_EMPTY = '''
<div id="something-else"></div>
'''

def test_safe_find_one(monkeypatch):
    soup = BeautifulSoup('<div id="mw-pages"></div>', 'html.parser')
    found = solution.safe_find(soup, 'div', id='mw-pages')
    assert found is not None
    not_found = solution.safe_find(soup, 'div', id='not-exist')
    assert not_found is None

def test_parse_page_success(monkeypatch):
    """Тестируем парсинг страницы с одной буквой"""
    # Сбросить глобальный словарь
    solution.beasts.clear()
    monkeypatch.setattr(requests, "get", lambda url: MockResponse(HTML_ONE_GROUP))
    url = "fake_url"
    next_url = solution.parse_page(url)
    # Проверим, что beasts пополнился на 2 по букве А
    print(solution.beasts)
    assert 'Ю' in solution.beasts
    assert solution.beasts['Ю'] == 2
    # Проверим, что next_url корректен
    assert next_url.startswith('https://')

def test_parse_page_empty(monkeypatch):
    """Тестируем страницу без нужных div (ничего не должно упасть)"""
    solution.beasts.clear()
    monkeypatch.setattr(requests, "get", lambda url: MockResponse(HTML_EMPTY))
    url = "fake_url"
    next_url = solution.parse_page(url)
    assert next_url is None
    assert solution.beasts == {}

def test_save_to_file(tmp_path):
    """Тестируем сохранение в файл"""
    test_file = tmp_path / "beasts.csv"
    # Подменяем OUTPUT_FILE на временный
    orig_output_file = solution.OUTPUT_FILE
    solution.OUTPUT_FILE = str(test_file)
    # Заполним тестовые данные
    solution.beasts.clear()
    solution.beasts['А'] = 3
    solution.beasts['Б'] = 1
    solution.save_to_file()
    with open(test_file, encoding='utf-8') as f:
        lines = f.readlines()
        assert "А,3" in lines[0]
        assert "Б,1" in lines[1] or "Б,1" in lines[0]
    solution.OUTPUT_FILE = orig_output_file

def test_parse_page_bad_request(monkeypatch, capsys):
    """Тестируем обработку ошибок сети"""
    def raise_exc(url): raise requests.exceptions.RequestException("fail")
    monkeypatch.setattr(requests, "get", raise_exc)
    solution.beasts.clear()
    result = solution.parse_page("any_url")
    captured = capsys.readouterr()
    assert "Ошибка запроса" in captured.out
    assert result is None

def test_parse_page_exception(monkeypatch, capsys):
    """Тестируем обработку любых других ошибок"""
    def broken_get(url): raise Exception("some fail")
    monkeypatch.setattr(requests, "get", broken_get)
    solution.beasts.clear()
    result = solution.parse_page("any_url")
    captured = capsys.readouterr()
    assert "Ошибка парсинга" in captured.out
    assert result is None
