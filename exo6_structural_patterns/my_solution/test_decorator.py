import pytest

from decorator import (BaseOrder, DiscountDecorator, ExpressShippingDecorator,
                       GiftWrapDecorator, InsuranceDecorator, OrderComponent,
                       PremiumMemberDecorator)


def test_base_order():
    assert BaseOrder(100).get_cost() == 100


def test_single_options():
    assert ExpressShippingDecorator(BaseOrder(100)).get_cost() == 115
    assert InsuranceDecorator(BaseOrder(100)).get_cost() == 105
    assert GiftWrapDecorator(BaseOrder(100)).get_cost() == 105
    assert DiscountDecorator(BaseOrder(100), percent=15).get_cost() == pytest.approx(85)
    assert PremiumMemberDecorator(BaseOrder(100)).get_cost() == pytest.approx(90)


def test_same_total_as_the_original_code():
    # original calculate_total with every flag on: 100 + 15 + 5 + 5 = 125,
    # -15 % -> 106.25, -10 % -> 95.625
    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)
    assert order.get_cost() == pytest.approx(95.625)
    assert isinstance(order, OrderComponent)


def test_insurance_uses_base_price_even_when_wrapped():
    order = InsuranceDecorator(ExpressShippingDecorator(BaseOrder(100)))
    assert order.get_cost() == pytest.approx(120)  # 100 + 15 + 5 % of 100


def test_description_lists_every_option():
    order = GiftWrapDecorator(ExpressShippingDecorator(BaseOrder(50)))
    description = order.get_description()
    assert "Base order" in description and "Express shipping" in description and "Gift wrap" in description


def test_invalid_discount():
    with pytest.raises(ValueError):
        DiscountDecorator(BaseOrder(100), percent=150)
