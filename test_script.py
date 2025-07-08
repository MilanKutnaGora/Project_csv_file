import pytest
from csv_tool import parse_where_condition, filter_rows, aggregate

# Пример тестовых данных
rows = [
    {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
    {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
    {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
    {"name": "poco x5 pro", "brand": "xiaomi", "price": "299", "rating": "4.4"},
]

def test_parse_where_condition():
    assert parse_where_condition("price>200") == ("price", ">", "200")
    assert parse_where_condition("brand=apple") == ("brand", "=", "apple")
    assert parse_where_condition("rating<4.8") == ("rating", "<", "4.8")
    with pytest.raises(ValueError):
        parse_where_condition("price!200")

def test_filter_rows_numeric():
    filtered = filter_rows(rows, "price", ">", "500")
    assert len(filtered) == 2
    assert all(float(row["price"]) > 500 for row in filtered)

def test_filter_rows_string():
    filtered = filter_rows(rows, "brand", "=", "xiaomi")
    assert len(filtered) == 2
    assert all(row["brand"] == "xiaomi" for row in filtered)

def test_aggregate_avg():
    filtered = filter_rows(rows, "brand", "=", "xiaomi")
    result = aggregate(filtered, "avg", "price")
    assert result == {"avg(price)": (199 + 299) / 2}

def test_aggregate_min_max():
    result_min = aggregate(rows, "min", "rating")
    result_max = aggregate(rows, "max", "rating")
    assert result_min == {"min(rating)": 4.4}
    assert result_max == {"max(rating)": 4.9}

def test_aggregate_empty():
    empty = []
    with pytest.raises(ValueError):
        aggregate(empty, "avg", "price")
