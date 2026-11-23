"""
Decorator pattern - refactor of the order pricing system.

Before: Order.calculate_total() took 5 boolean flags and handled every
option inside one method (adding an option = modifying that method, and
the order of operations was hidden in the code).

After:
- OrderComponent = interface with get_cost() and get_description()
- BaseOrder = the plain order
- each option is a decorator that WRAPS an order, adds its own cost and
  description, and delegates the rest to the order it wraps.
The order in which you wrap is the order of operations, so it is visible.
"""

from abc import ABC, abstractmethod


class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        self.base_price = base_price

    def get_cost(self) -> float:
        return self.base_price

    def get_description(self) -> str:
        return f"Base order ({self.base_price:.2f}€)"


class OrderDecorator(OrderComponent):
    """Parent of every option: it holds the wrapped order and delegates to it."""

    def __init__(self, order: OrderComponent):
        self._order = order

    @property
    def base_price(self) -> float:
        # lets an option such as insurance find the original price
        return self._order.base_price

    def get_cost(self) -> float:
        return self._order.get_cost()

    def get_description(self) -> str:
        return self._order.get_description()


class ExpressShippingDecorator(OrderDecorator):
    COST = 15.00

    def get_cost(self):
        return self._order.get_cost() + self.COST

    def get_description(self):
        return self._order.get_description() + f" + Express shipping (+{self.COST:.2f}€)"


class InsuranceDecorator(OrderDecorator):
    RATE = 0.05  # 5 % of the base price, like in the original code

    def get_cost(self):
        return self._order.get_cost() + self.base_price * self.RATE

    def get_description(self):
        return self._order.get_description() + f" + Insurance 5% (+{self.base_price * self.RATE:.2f}€)"


class GiftWrapDecorator(OrderDecorator):
    COST = 5.00

    def get_cost(self):
        return self._order.get_cost() + self.COST

    def get_description(self):
        return self._order.get_description() + f" + Gift wrap (+{self.COST:.2f}€)"


class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, percent: float):
        super().__init__(order)
        if not 0 <= percent <= 100:
            raise ValueError("Discount must be between 0 and 100 %")
        self.percent = percent

    def get_cost(self):
        return self._order.get_cost() * (1 - self.percent / 100)

    def get_description(self):
        return self._order.get_description() + f" - Discount {self.percent}%"


class PremiumMemberDecorator(OrderDecorator):
    RATE = 0.10

    def get_cost(self):
        return self._order.get_cost() * (1 - self.RATE)

    def get_description(self):
        return self._order.get_description() + " - Premium member 10%"


if __name__ == "__main__":
    order = BaseOrder(100.00)
    print(order.get_description())
    print(f"Total: {order.get_cost():.2f}€")

    print("\n---\n")

    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)
    print(order.get_description())
    print(f"Total: {order.get_cost():.2f}€")
