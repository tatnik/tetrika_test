import pytest

NUM_TASKS = 3  # количество задач 

def run_pytest_for_task(task_name):
    """Запустить pytest для одной задачи.
    Возвращает:
      ('success', 0) — если тесты прошли успешно,
      ('error', код возврата) — если pytest вернул ненулевой код,
      ('error', текст ошибки) — если возникло исключение.
    """
    test_file = f"{task_name}/test_solution.py"
    try:
        result_code = pytest.main([test_file])
        if result_code == 0:
            return ("success", 0)
        else:
            return ("error", result_code)
    except Exception as e:
        return ("error", str(e))

def main():
    results = {}
    task_names = [f"task{i+1}" for i in range(NUM_TASKS)]

    for task in task_names:
        results[task] = run_pytest_for_task(task)

    print("\n--- Результаты тестирования ---")
    all_success = True
    for task, (status, info) in results.items():
        if status == "success":
            print(f"[{task}] — все тесты успешно прошли.")
        elif status == "error" and isinstance(info, int):
            print(f"[{task}] — тесты завершились с ошибкой (код возврата {info}).")
            all_success = False
        else:  # status == "error" and isinstance(info, str)
            print(f"[{task}] — возникла ошибка: {info}")
            all_success = False

    if all_success:
        print("\nВсе тесты по всем задачам успешно прошли!")
    else:
        print("\nВ некоторых задачах тесты завершились с ошибкой или не были запущены.")

if __name__ == "__main__":
    main()
