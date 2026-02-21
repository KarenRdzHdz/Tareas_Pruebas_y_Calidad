"""Reservation model."""

import uuid
from storage.file_manager import FileManager
from models.hotel import Hotel

RESERVATION_FILE = "data/reservations.json"


class Reservation:
    """Represents a reservation."""

    @staticmethod
    def create_reservation(customer_id: str,
                           hotel_id: str) -> None:
        """Create reservation."""
        reservation_id = str(uuid.uuid4())

        Hotel.reserve_room(hotel_id)

        reservations = FileManager.load_data(RESERVATION_FILE)

        reservations.append({
            "reservation_id": reservation_id,
            "customer_id": customer_id,
            "hotel_id": hotel_id
        })

        FileManager.save_data(RESERVATION_FILE, reservations)

    @staticmethod
    def cancel_reservation(reservation_id: str) -> None:
        """Cancel reservation."""
        reservations = FileManager.load_data(RESERVATION_FILE)

        new_reservations = [
            r for r in reservations
            if r["reservation_id"] != reservation_id
        ]

        if len(new_reservations) == len(reservations):
            raise ValueError("Reservation not found.")

        FileManager.save_data(RESERVATION_FILE, new_reservations)
