import argparse
from tabulate import tabulate
from csv_tool import read_csv, parse_where_condition, filter_rows, aggregate

def main():
    parser = argparse.ArgumentParser(description="CSV фильтрация и агрегация")
    parser.add_argument("csvfile", help="Путь к CSV-файлу")
    parser.add_argument("--where", help="Условие фильтрации, например: price>200")
    parser.add_argument("--aggregate", help="Агрегация, например: avg=rating")
    args = parser.parse_args()

    # Чтение данных
    rows = read_csv(args.csvfile)

    # Фильтрация
    if args.where:
        column, op, value = parse_where_condition(args.where)
        rows = filter_rows(rows, column, op, value)

    # Аггрегация
    if args.aggregate:
        if '=' not in args.aggregate:
            raise ValueError("Параметр aggregate должен быть в формате operation=column")
        operation, column = args.aggregate.split('=', 1)
        operation = operation.strip()
        column = column.strip()
        result = aggregate(rows, operation, column)
        print(tabulate([result], headers="keys", tablefmt="grid"))
    else:
        if rows:
            print(tabulate(rows, headers="keys", tablefmt="grid"))
        else:
            print("Нет строк, удовлетворяющих условиям.")

if __name__ == "__main__":
    main()
