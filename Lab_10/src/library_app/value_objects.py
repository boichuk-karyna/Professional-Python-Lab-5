from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PublicationInfo:
    year: int
    publisher: str

    def __post_init__(self) -> None:
        if self.year < 0:
            raise ValueError("Publication year cannot be negative")

        if not self.publisher.strip():
            raise ValueError("Publisher cannot be empty")

    def __str__(self) -> str:
        return f"{self.publisher}, {self.year}"