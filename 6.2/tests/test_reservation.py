"""Unit tests for Reservation model."""

import unittest
from models.hotel import Hotel
from models.customer import Customer
from models.reservation import Reservation
from storage.file_manager import FileManager


HOTEL_FILE = "data/hotels.json"
CUSTOMER_FILE = "data/customers.json"
RESERVATION_FILE = "data/reservations.json"


class TestReservation(unittest.TestCase):
    """Test cases for Reservation class."""

    def setUp(self):
        """Reset all files."""
        FileManager.save_data(HOTEL_FILE, [])
        FileManager.save_data(CUSTOMER_FILE, [])
        FileManager.save_data(RESERVATION_FILE, [])

        hotel = Hotel("H1", "Hotel1", "MX", 2)
        Hotel.create_hotel(hotel)

        customer = Customer("C1", "John",
                            "john@mail.com", "123")
        Customer.create_customer(customer)

    def test_create_reservation_valid(self):
        """Test valid reservation."""
        Reservation.create_reservation("C1", "H1")

        data = FileManager.load_data(RESERVATION_FILE)
        self.assertEqual(len(data), 1)

    def test_cancel_reservation_valid(self):
        """Test cancel reservation."""
        Reservation.create_reservation("C1", "H1")
        reservations = FileManager.load_data(RESERVATION_FILE)

        reservation_id = reservations[0]["reservation_id"]
        Reservation.cancel_reservation(reservation_id)

        data = FileManager.load_data(RESERVATION_FILE)
        self.assertEqual(len(data), 0)

    def test_cancel_reservation_not_found(self):
        """Negative test: reservation not found."""
        with self.assertRaises(ValueError):
            Reservation.cancel_reservation("INVALID")

    def test_reservation_no_rooms(self):
        """Negative test: no availability."""
        Reservation.create_reservation("C1", "H1")
        Reservation.create_reservation("C1", "H1")

        with self.assertRaises(ValueError):
            Reservation.create_reservation("C1", "H1")