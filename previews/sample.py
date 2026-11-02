"""Open in an editor to compare syntax colors and selections."""
from dataclasses import dataclass


@dataclass
class Palette:
    name: str
    day: bool = True

    def describe(self, count: int = 10) -> str:
        # Comments should remain readable beside ordinary text.
        if count < 1:
            raise ValueError("Expected at least one palette")
        return f"{self.name}: {count} coordinated palettes"


print(Palette("manna").describe())
