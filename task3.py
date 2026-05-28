import sys
from pathlib import Path
def parse_log_line(line: str) -> dict:
    """
    Розбирає один рядок логу на компоненти.

    :param line: рядок з логу
    :return: словник з ключами date, time, level, message
    """
    # Розділяємо рядок на частини: дата, час, рівень, повідомлення
    parts = line.split(" ", 3)
    return {
        "date": parts[0],       # 2024-01-22
        "time": parts[1],       # 08:30:01
        "level": parts[2],      # INFO
        "message": parts[3].strip()  # текст повідомлення
    }
def load_logs(file_path: str) -> list:
    """
    Завантажує всі рядки з лог-файлу.

    :param file_path: шлях до файлу
    :return: список словників з розібраними рядками
    """
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Застосовуємо parse_log_line до кожного рядка
            logs = [parse_log_line(line) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Помилка: файл '{file_path}' не знайдено")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)
    return logs
def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Фільтрує логи за рівнем логування.

    :param logs: список всіх логів
    :param level: рівень логування (INFO, ERROR, DEBUG, WARNING)
    :return: відфільтрований список
    """
    # Використовуємо filter з lambda — елемент функціонального програмування
    return list(filter(lambda log: log["level"] == level.upper(), logs))
def count_logs_by_level(logs: list) -> dict:
    """
    Підраховує кількість записів для кожного рівня.

    :param logs: список всіх логів
    :return: словник {рівень: кількість}
    """
    counts = {}
    for log in logs:
        level = log["level"]
        # Збільшуємо лічильник для цього рівня
        counts[level] = counts.get(level, 0) + 1
    return counts
def display_log_counts(counts: dict):
    """Виводить таблицю зі статистикою рівнів логування."""
    print(f"{'Рівень логування':<17}| Кількість")
    print(f"{'-' * 17}|{'-' * 10}")
    # Виводимо кожен рівень і його кількість
    for level, count in counts.items():
        print(f"{level:<17}| {count}")
def main():
    """Основна логіка скрипту."""
    # Перевіряємо чи переданий шлях до файлу
    if len(sys.argv) < 2:
        print("Використання: python task3.py /шлях/до/logfile.log [рівень]")
        sys.exit(1)

    file_path = sys.argv[1]

    # Завантажуємо всі логи з файлу
    logs = load_logs(file_path)

    # Підраховуємо і виводимо статистику
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    # Якщо переданий другий аргумент — виводимо деталі для цього рівня
    if len(sys.argv) > 2:
        level = sys.argv[2].upper()
        filtered = filter_logs_by_level(logs, level)
        print(f"\nДеталі логів для рівня '{level}':")
        for log in filtered:
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()