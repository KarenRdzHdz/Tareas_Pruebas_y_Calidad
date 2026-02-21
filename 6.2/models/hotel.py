"""Hotel model."""

from typing import Dict, List
from storage.file_manager import FileManager


HOTEL_FILE = "data/hotels.json"


class Hotel:
    """Represents a hotel entity."""

    def __init__(self, hotel_id: str, name: str,
                 location: str, total_rooms: int) -> None:

        if total_rooms <= 0:
            raise ValueError("Total rooms must be positive.")

        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.available_rooms = total_rooms

    def to_dict(self) -> Dict:
        """Convert object to dictionary."""
        return self.__dict__

    @staticmethod
    def create_hotel(hotel: "Hotel") -> None:
        """Create new hotel."""
        hotels = FileManager.load_data(HOTEL_FILE)

        for item in hotels:
            if item["hotel_id"] == hotel.hotel_id:
                raise ValueError("Hotel ID already exists.")

        hotels.append(hotel.to_dict())
        FileManager.save_data(HOTEL_FILE, hotels)

    @staticmethod
    def delete_hotel(hotel_id: str) -> None:
        """Delete hotel."""
        hotels = FileManager.load_data(HOTEL_FILE)
        hotels = [h for h in hotels if h["hotel_id"] != hotel_id]
        FileManager.save_data(HOTEL_FILE, hotels)

    @staticmethod
    def display_hotel(hotel_id: str) -> Dict:
        """Return hotel information."""
        hotels = FileManager.load_data(HOTEL_FILE)

        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                return hotel

        raise ValueError("Hotel not found.")

    @staticmethod
    def reserve_room(hotel_id: str) -> None:
        """Reserve a room if available."""
        hotels = FileManager.load_data(HOTEL_FILE)

        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if hotel["available_rooms"] <= 0:
                    raise ValueError("No rooms available.")
                hotel["available_rooms"] -= 1
                FileManager.save_data(HOTEL_FILE, hotels)
                return

        raise ValueError("Hotel not found.")