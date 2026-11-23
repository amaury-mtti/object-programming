"""
Factory pattern - refactor of the payment system.

Before: one process_payment() function with an if/elif per payment type.
Adding Apple Pay meant opening and modifying that function (breaks the
Open/Closed principle).

After:
- PaymentProcessor (abstract class) = the "contract" every processor follows
- one class per payment method, holding its own validation and fee logic
- PaymentFactory maps a string ("paypal") to the right class with a dict
Adding a new method = writing one new class + one register() call.
"""

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Interface: every payment processor must implement these methods."""

    method = "unknown"
    error_message = "Invalid payment details"

    @abstractmethod
    def validate(self, details: dict) -> bool:
        """Return True if the payment details are valid."""

    @abstractmethod
    def calculate_fee(self, amount: float) -> float:
        """Return the fee charged for this payment method."""

    def process(self, amount: float, details: dict) -> dict:
        # The steps are the same for every method, only validate() and
        # calculate_fee() change, so process() is written once here.
        if not self.validate(details):
            return {"success": False, "error": self.error_message}
        fee = round(self.calculate_fee(amount), 2)
        return {
            "success": True,
            "method": self.method,
            "amount": round(amount + fee, 2),
            "fee": fee,
        }


class CreditCardProcessor(PaymentProcessor):
    method = "credit_card"
    error_message = "Invalid card number or CVV"

    def validate(self, details: dict) -> bool:
        card_number = details.get("card_number") or ""
        cvv = details.get("cvv") or ""
        return len(card_number) == 16 and len(cvv) == 3

    def calculate_fee(self, amount: float) -> float:
        return amount * 0.029  # 2.9 %


class BankTransferProcessor(PaymentProcessor):
    method = "bank_transfer"
    error_message = "Invalid IBAN"

    def validate(self, details: dict) -> bool:
        iban = details.get("iban") or ""
        return len(iban) >= 15

    def calculate_fee(self, amount: float) -> float:
        return 1.50  # flat fee


class PayPalProcessor(PaymentProcessor):
    method = "paypal"
    error_message = "Invalid PayPal email"

    def validate(self, details: dict) -> bool:
        email = details.get("email") or ""
        return "@" in email

    def calculate_fee(self, amount: float) -> float:
        return amount * 0.034 + 0.30  # 3.4 % + 0.30 EUR


class PaymentFactory:
    """Creates the right processor from a string, without any if/elif."""

    def __init__(self):
        self._processors = {
            "credit_card": CreditCardProcessor,
            "bank_transfer": BankTransferProcessor,
            "paypal": PayPalProcessor,
        }

    def register(self, payment_type: str, processor_class: type) -> None:
        """Add a new payment method without touching the existing code."""
        self._processors[payment_type] = processor_class

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        processor_class = self._processors.get(payment_type)
        if processor_class is None:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return processor_class()


if __name__ == "__main__":
    factory = PaymentFactory()

    processor = factory.get_processor("credit_card")
    print(processor.process(100.0, {"card_number": "1234567890123456", "cvv": "123"}))

    processor = factory.get_processor("bank_transfer")
    print(processor.process(100.0, {"iban": "FR7630006000011234567890189", "bic": "BNPAFRPP"}))

    processor = factory.get_processor("paypal")
    print(processor.process(100.0, {"email": "amaury@example.com"}))
