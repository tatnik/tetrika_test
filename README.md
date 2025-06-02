# Тестовое задание для компании Tetrika

- Для решения используется __Python 3.12__

- Для задания 2 используются библиотеки __bs4__ и __requests__, задачи 1 и 3 реализованы встроенными средствами языка

- Решение каждой задачи находится  в папке с ее условием, в файле __solution.py__

- К каждой задаче написаны тесты

- При тестировании используется __pytest__

# Структура проекта

```
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py              - точка входа, содержит запуск тестов для всех задач
│
├── task1/
│   ├── task1.md         - описание задачи 
│   ├── solution.py      - решение
│   └── test_solution.py - тесты
│
├── task2/
...
```

# Запуск в Docker

Сборка и запуск контейнера

```docker-compose up --build```

Контейнер запустится и выполнит команду __python3 main.py__.
Результат работы должен быть таким:
```
app-1  | ============================= test session starts ==============================
app-1  | platform linux -- Python 3.12.10, pytest-8.4.0, pluggy-1.6.0
app-1  | rootdir: /code
app-1  | collected 10 items
app-1  | 
app-1  | task1/test_solution.py ..........                                        [100%]
app-1  | 
app-1  | ============================== 10 passed in 0.07s ==============================
app-1  | ============================= test session starts ==============================
app-1  | platform linux -- Python 3.12.10, pytest-8.4.0, pluggy-1.6.0
app-1  | rootdir: /code
app-1  | collected 6 items
app-1  | 
app-1  | task2/test_solution.py ......                                            [100%]
app-1  | 
app-1  | ============================== 6 passed in 0.18s ===============================
app-1  | ============================= test session starts ==============================
app-1  | platform linux -- Python 3.12.10, pytest-8.4.0, pluggy-1.6.0
app-1  | rootdir: /code
app-1  | collected 3 items
app-1  | 
app-1  | task3/test_solution.py ...                                               [100%]
app-1  | 
app-1  | ============================== 3 passed in 0.10s ===============================
app-1  | 
app-1  | --- Результаты тестирования ---
app-1  | [task1] — все тесты успешно прошли.
app-1  | [task2] — все тесты успешно прошли.
app-1  | [task3] — все тесты успешно прошли.
app-1  | 
app-1  | Все тесты по всем задачам успешно прошли!
```
