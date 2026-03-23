from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


"""variable name: type hint = Field() is the validation rules"""
"""... means the field is required, if not provided, validation error"""
"""min and max length are for string length"""
"""ge and le are for int, and they mean greater or equal, less or equal"""
"""notes is an optional field here, it can be string or none"""
"""is_operational is by default True if not set"""
"""datetime converts a string into a datetime"""
"""datetime takes year,month,day, and others can be empty"""


def main() -> None:
    print("Space Station Data Validation")
    # you can do print("=" * 40)
    print("========================================")
    valid_station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2026-03-15T10:00:00"
    )
    print("Valid station created:")
    print(f"ID: {valid_station.station_id}")
    print(f"Name: {valid_station.name}")
    print(f"Crew: {valid_station.crew_size} people")
    print(f"Power: {valid_station.power_level}%")
    print(f"Oxygen: {valid_station.oxygen_level}%")
    print(f"Status: {'Operational' if valid_station.is_operational else
                     'Not Operational'}"
          )
    print()
    print("========================================")
    try:
        SpaceStation(
            station_id="Abc",
            name="test station",
            crew_size=25,
            power_level=10,
            oxygen_level=50,
            last_maintenance="2026-03-15"
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e)


if __name__ == "__main__":
    main()
