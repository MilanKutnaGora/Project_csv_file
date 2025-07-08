from typing import List, Dict, Any, Tuple
import csv

def parse_where_condition(cond: str) -> Tuple[str, str, str]:
    """
    Разбирает строку условия фильтрации, например "price>200" -> ("price", ">", "200")
    """
    for op in ['>', '<', '=']:
        if op in cond:
            col, val = cond.split(op, 1)
            return col.strip(), op, val.strip()
    raise ValueError("Invalid where condition format. Expected format: column>value, column<value or column=value")

def filter_rows(rows: List[Dict[str, str]], column: str, op: str, value: str) -> List[Dict[str, str]]:
    """
    Фильтрует строки по одной колонке и одному оператору.
    """
    def cmp(v1: str, v2: str) -> bool:
        try:
            v1f = float(v1)
            v2f = float(v2)
            if op == '>': return v1f > v2f
            if op == '<': return v1f < v2f
            if op == '=': return v1f == v2f
        except ValueError:
            if op == '=': return v1 == v2
            else:
                raise ValueError("Operator > or < not supported for non-numeric values")
        return False
    return [row for row in rows if cmp(row[column], value)]

def aggregate(rows: List[Dict[str, str]], operation: str, column: str) -> Dict[str, Any]:
    """
    Выполняет агрегацию (avg, min, max) по одной числовой колонке.
    """
    values = [float(row[column]) for row in rows]
    if not values:
        raise ValueError("No data to aggregate")
    if operation == 'avg':
        result = sum(values) / len(values)
    elif operation == 'min':
        result = min(values)
    elif operation == 'max':
        result = max(values)
    else:
        raise ValueError(f"Unsupported aggregation operation: {operation}")
    return {f"{operation}({column})": result}

def read_csv(filepath: str) -> List[Dict[str, str]]:
    """
    Читает CSV-файл и возвращает список словарей.
    """
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)
