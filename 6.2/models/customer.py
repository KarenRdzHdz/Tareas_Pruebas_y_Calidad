"""Customer model."""

from typing import Dict
from storage.file_manager import FileManager


CUSTOMER_FILE = "data/customers.json"


class Customer:
    """Represents a customer."""

    def __init__(self, customer_id: str,
                 name: str, email: str, phone: str) -> None:

        if "@" not in email:
            raise ValueError("Invalid email format.")

        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self) -> Dict:
        """Convert object to dictionary."""
        return self.__dict__

    @staticmethod
    def create_customer(customer: "Customer") -> None:
        """Create new customer."""
        customers = FileManager.load_data(CUSTOMER_FILE)

        for item in customers:
            if item["customer_id"] == customer.customer_id:
                raise ValueError("Customer ID already exists.")

        customers.append(customer.to_dict())
        FileManager.save_data(CUSTOMER_FILE, customers)

    @staticmethod
    def display_customer(customer_id: str) -> Dict:
        """Return customer info."""
        customers = FileManager.load_data(CUSTOMER_FILE)

        for customer in customers:
            if customer["customer_id"] == customer_id:
                return customer

        raise ValueError("Customer not found.")