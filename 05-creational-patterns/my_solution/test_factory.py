import pytest

from factory import (BankTransferProcessor, CreditCardProcessor, PaymentFactory,
                     PaymentProcessor, PayPalProcessor)


def test_factory_returns_the_right_class():
    factory = PaymentFactory()
    assert isinstance(factory.get_processor("credit_card"), CreditCardProcessor)
    assert isinstance(factory.get_processor("bank_transfer"), BankTransferProcessor)
    assert isinstance(factory.get_processor("paypal"), PayPalProcessor)


def test_unknown_type_raises():
    with pytest.raises(ValueError):
        PaymentFactory().get_processor("cheque")


def test_credit_card_fee():
    result = CreditCardProcessor().process(100.0, {"card_number": "1234567890123456", "cvv": "123"})
    assert result == {"success": True, "method": "credit_card", "amount": 102.9, "fee": 2.9}


def test_bank_transfer_fee():
    result = BankTransferProcessor().process(100.0, {"iban": "FR7630006000011234567890189"})
    assert result["amount"] == 101.5 and result["fee"] == 1.5


def test_paypal_fee():
    result = PayPalProcessor().process(100.0, {"email": "a@b.com"})
    assert result["fee"] == pytest.approx(3.7)


def test_invalid_details():
    assert CreditCardProcessor().process(100.0, {"card_number": "123", "cvv": "1"})["success"] is False
    assert PayPalProcessor().process(100.0, {"email": "no-at-sign"})["success"] is False


def test_register_new_method_without_modifying_factory():
    class ApplePayProcessor(PaymentProcessor):
        method = "apple_pay"

        def validate(self, details):
            return "token" in details

        def calculate_fee(self, amount):
            return 0.0

    factory = PaymentFactory()
    factory.register("apple_pay", ApplePayProcessor)
    assert factory.get_processor("apple_pay").process(50.0, {"token": "x"})["amount"] == 50.0


def test_abstract_class_cannot_be_instantiated():
    with pytest.raises(TypeError):
        PaymentProcessor()
