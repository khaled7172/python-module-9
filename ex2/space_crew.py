from enum import Enum
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from pydantic import model_validator
from pydantic import ValidationError

"""Using Enum ensures only valid ranks are accepted"""
"""Any string not in this Enum automatically rejected"""


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


"""crew is a list of CrewMember models"""
"""Pydantic validates nested models automatically, If one CrewMember fails
validation, then the whole SpaceMission fails"""


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)  # max 10 years
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_mission_rules(self):
        # Mission ID must start with "M"
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        # Must have at least one Commander or Captain
        if not any(
            member.rank in {
                Rank.commander,
                Rank.captain} for member in self.crew):
            raise ValueError(
                "Mission must have at least one Commander or Captain")

        # Long missions (> 365 days) require 50% experienced crew (5+ years)
        if self.duration_days > 365:
            experienced = sum(member.years_experience >=
                              5 for member in self.crew)
            if experienced < len(self.crew) / 2:
                raise ValueError(
                    "Long missions (>365 days) require 50% experienced crew")

        # All crew members must be active
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main():
    print("Space Mission Crew Validation")
    print("=========================================")

    # Valid mission example
    crew = [
        CrewMember(
            member_id="CM001",
            name="Sarah Connor",
            rank=Rank.commander,
            age=35,
            specialization="Mission Command",
            years_experience=10),
        CrewMember(
            member_id="CM002",
            name="John Smith",
            rank=Rank.lieutenant,
            age=30,
            specialization="Navigation",
            years_experience=6),
        CrewMember(
            member_id="CM003",
            name="Alice Johnson",
            rank=Rank.officer,
            age=28,
            specialization="Engineering",
            years_experience=4)]
    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2024-07-01T09:00:00",
        duration_days=900,
        crew=crew,
        budget_millions=2500.0
    )
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(crew)}")
    print("Crew members:")
    for mem in crew:
        print(f"- {mem.name} ({mem.rank.value}) - {mem.specialization}")
    print()
    print("=========================================")

    # Invalid mission example (no Commander/Captain)
    try:
        SpaceMission(
            mission_id="M2024_LUNA",
            mission_name="Moon Research",
            destination="Moon",
            launch_date="2024-08-01T09:00:00",
            duration_days=200,
            crew=[
                CrewMember(
                    member_id="CM004",
                    name="Bob Lee",
                    rank=Rank.lieutenant,
                    age=32,
                    specialization="Science",
                    years_experience=3)],
            budget_millions=500.0)
    except ValidationError as e:
        print("Expected validation error:")
        print(e)


if __name__ == "__main__":
    main()
