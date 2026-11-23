import pytest

from operator_overloading import Circle, Complex, Matrix, Person, Point, Vector


def test_complex_add_and_sub():
    assert Complex(3, 2) + Complex(1, 7) == Complex(4, 9)
    assert Complex(3, 2) - Complex(1, 7) == Complex(2, -5)


def test_person_compared_on_age():
    assert Person("A", 30, "F") > Person("B", 20, "M")
    assert not Person("A", 20, "F") > Person("B", 30, "M")


def test_vector_dot_product():
    assert Vector(1, 2, 3) * Vector(4, 5, 6) == 32


def test_circle_all_comparisons():
    small, big = Circle(1), Circle(5)
    assert small < big and big > small
    assert small <= Circle(1) and big >= Circle(5)
    assert small == Circle(1) and small != big


def test_circle_negative_radius():
    with pytest.raises(ValueError):
        Circle(-1)


def test_point_compared_on_distance():
    assert Point(3, 4) == Point(5, 0)  # both at distance 5
    assert Point(1, 1) < Point(2, 2)
    assert Point(2, 2) >= Point(1, 1)


def test_matrix_product():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    assert a * b == Matrix([[19, 22], [43, 50]])


def test_matrix_wrong_dimensions():
    with pytest.raises(ValueError):
        Matrix([[1, 2, 3]]) * Matrix([[1, 2]])
