"""
OOP Problems - Operator overloading.

Each class redefines one or more "magic methods" (__add__, __gt__, __mul__...)
so that Python's operators (+, >, *...) work directly on our own objects.
"""

import math
from functools import total_ordering


# ---------------------------------------------------------------------------
# Problem 1 - Complex numbers: overload + and -
# ---------------------------------------------------------------------------
class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        # (a + bi) + (c + di) = (a + c) + (b + d)i
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        # (a + bi) - (c + di) = (a - c) + (b - d)i
        return Complex(self.real - other.real, self.imag - other.imag)

    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    def __repr__(self):
        sign = "+" if self.imag >= 0 else "-"
        return f"{self.real} {sign} {abs(self.imag)}i"


# ---------------------------------------------------------------------------
# Problem 2 - Person: compare two persons on their age with >
# ---------------------------------------------------------------------------
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other):
        return self.age > other.age

    def __repr__(self):
        return f"Person({self.name}, {self.age})"


# ---------------------------------------------------------------------------
# Problem 4 - Vector in space: * returns the dot product
# ---------------------------------------------------------------------------
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        # dot product: x1*x2 + y1*y2 + z1*z2
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"


# ---------------------------------------------------------------------------
# Problem 5 - Circle: all six comparison operators, based on the radius
# ---------------------------------------------------------------------------
class Circle:
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("A radius cannot be negative")
        self.radius = radius

    def __lt__(self, other):
        return self.radius < other.radius

    def __gt__(self, other):
        return self.radius > other.radius

    def __eq__(self, other):
        return self.radius == other.radius

    def __ne__(self, other):
        return self.radius != other.radius

    def __le__(self, other):
        return self.radius <= other.radius

    def __ge__(self, other):
        return self.radius >= other.radius

    def __repr__(self):
        return f"Circle(r={self.radius})"


# ---------------------------------------------------------------------------
# Problem 6 - 2D point: compare on the Euclidean distance from the origin
# Here I only write == and <, and @total_ordering generates <=, >, >=
# for me (a shortcut, compared with writing all six like in Circle).
# ---------------------------------------------------------------------------
@total_ordering
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __eq__(self, other):
        return self.distance() == other.distance()

    def __lt__(self, other):
        return self.distance() < other.distance()

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


# ---------------------------------------------------------------------------
# Problem 7 - Matrix: * is the matrix product
# ---------------------------------------------------------------------------
class Matrix:
    def __init__(self, rows):
        # rows is a list of lists, e.g. [[1, 2], [3, 4]]
        if not rows or any(len(row) != len(rows[0]) for row in rows):
            raise ValueError("All rows must have the same length")
        self.rows = rows
        self.n_rows = len(rows)
        self.n_cols = len(rows[0])

    def __mul__(self, other):
        # (n x m) * (m x p) -> (n x p): columns of A must equal rows of B
        if self.n_cols != other.n_rows:
            raise ValueError(
                f"Cannot multiply a {self.n_rows}x{self.n_cols} matrix "
                f"by a {other.n_rows}x{other.n_cols} matrix"
            )
        result = []
        for i in range(self.n_rows):
            new_row = []
            for j in range(other.n_cols):
                total = 0
                for k in range(self.n_cols):
                    total += self.rows[i][k] * other.rows[k][j]
                new_row.append(total)
            result.append(new_row)
        return Matrix(result)

    def __eq__(self, other):
        return self.rows == other.rows

    def __repr__(self):
        return "\n".join(str(row) for row in self.rows)


if __name__ == "__main__":
    print("Complex:", Complex(3, 2) + Complex(1, 7), "|", Complex(3, 2) - Complex(1, 7))
    print("Person:", Person("Amaury", 19, "M") > Person("Leo", 17, "M"))
    print("Vector:", Vector(1, 2, 3) * Vector(4, 5, 6))
    print("Circle:", Circle(2) < Circle(5), Circle(3) == Circle(3))
    print("Point:", Point(3, 4) == Point(5, 0), Point(1, 1) < Point(2, 2))
    print("Matrix:")
    print(Matrix([[1, 2], [3, 4]]) * Matrix([[5, 6], [7, 8]]))
