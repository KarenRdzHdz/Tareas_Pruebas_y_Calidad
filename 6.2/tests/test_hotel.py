"""Unit tests for Hotel model."""

import os
import unittest
from models.hotel import Hotel
from storage.file_manager import FileManager


HOTEL_FILE = "data/hotels.json"


class TestHotel(unittest.TestCase):
    """Test cases for Hotel class."""

    def setUp(self):
        """Reset hotel file before each test."""
        FileManager.save_data(HOTEL_FILE, [])

    def test_create_hotel_valid(self):
        """Test valid hotel creation."""
        hotel = Hotel("H1", "TestHotel", "MX", 10)
        Hotel.create_hotel(hotel)

        data = FileManager.load_data(HOTEL_FILE)
        self.assertEqual(len(data), 1)

    def test_create_hotel_negative_rooms(self):
        """Negative test: invalid room number."""
        with self.assertRaises(ValueError):
            Hotel("H2", "BadHotel", "MX", -5)

    def test_duplicate_hotel_id(self):
        """Negative test: duplicate ID."""
        hotel = Hotel("H1", "Hotel1", "MX", 5)
        Hotel.create_hotel(hotel)

        with self.assertRaises(ValueError):
            Hotel.create_hotel(hotel)

    def test_display_hotel_not_found(self):
        """Negative test: hotel does not exist."""
        with self.assertRaises(ValueError):
            Hotel.display_hotel("INVALID")

    def test_reserve_room_success(self):
        """Test reserving a room."""
        hotel = Hotel("H1", "Hotel1", "MX", 2)
        Hotel.create_hotel(hotel)

        Hotel.reserve_room("H1")

        data = FileManager.load_data(HOTEL_FILE)
        self.assertEqual(data[0]["available_rooms"], 1)

    def test_reserve_room_no_availability(self):
        """Negative test: no rooms available."""
        hotel = Hotel("H1", "Hotel1", "MX", 1)
        Hotel.create_hotel(hotel)
        Hotel.reserve_room("H1")

        with self.assertRaises(ValueError):
            Hotel.reserve_room("H1")

    def test_delete_hotel(self):
        """Test deleting hotel."""
        hotel = Hotel("H1", "Hotel1", "MX", 5)
        Hotel.create_hotel(hotel)

        Hotel.delete_hotel("H1")

        data = FileManager.load_data(HOTEL_FILE)
        self.assertEqual(len(data), 0)

    def test_corrupted_json_file(self):
        """Negative test: corrupted JSON."""
        with open(HOTEL_FILE, "w", encoding="utf-8") as file:
            file.write("INVALID JSON")

        data = FileManager.load_data(HOTEL_FILE)
        self.assertEqual(data, [])