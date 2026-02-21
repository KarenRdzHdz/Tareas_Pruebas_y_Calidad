"""Unit tests for Customer model."""

import unittest
from models.customer import Customer
from storage.file_manager import FileManager


CUSTOMER_FILE = "data/customers.json"


class TestCustomer(unittest.TestCase):
    """Test cases for Customer class."""

    def setUp(self):
        """Reset customer file."""
        FileManager.save_data(CUSTOMER_FILE, [])

    def test_create_customer_valid(self):
        """Test valid customer."""
        customer = Customer("C1", "John", "john@mail.com", "123")
        Customer.create_customer(customer)

        data = FileManager.load_data(CUSTOMER_FILE)
        self.assertEqual(len(data), 1)

    def test_invalid_email(self):
        """Negative test: invalid email."""
        with self.assertRaises(ValueError):
            Customer("C2", "John", "invalidemail", "123")

    def test_duplicate_customer(self):
        """Negative test: duplicate ID."""
        customer = Customer("C1", "John", "john@mail.com", "123")
        Customer.create_customer(customer)

        with self.assertRaises(ValueError):
            Customer.create_customer(customer)

    def test_display_customer_not_found(self):
        """Negative test: customer not found."""
        with self.assertRaises(ValueError):
            Customer.display_customer("INVALID")
