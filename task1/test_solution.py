import pytest
from .solution import strict


# --- Тестовые функции ---

@strict
def add(x: int, y: int) -> int:
    return x + y

@strict
def concat(a: str, b: str) -> str:
    return a + b

@strict
def logical(flag: bool, value: int) -> bool:
    return flag and bool(value)

@strict
def division(a: float, b: float) -> float:
    return a / b
  


# --- Тесты ---

def test_add_ok():
    assert add(1, 2) == 3

def test_add_type_error():
    with pytest.raises(TypeError):
        add(1, "2")

def test_multiple_type_errors():
    with pytest.raises(TypeError):
        add("3", "4")  


def test_concat_ok():
    assert concat("foo", "bar") == "foobar"

def test_concat_type_error():
    with pytest.raises(TypeError):
        concat("foo", 2)


def test_logical_ok():
    assert logical(True, 5) is True

def test_logical_type_error():
    with pytest.raises(TypeError):
        logical(1, 5)  


def test_division_ok():
    assert division(6.0, 3.0) == 2.0

def test_division_type_error():
    with pytest.raises(TypeError):
        division(6, 3.0)  


def test_keyword_args():
    assert add(x=3, y=4) == 7
