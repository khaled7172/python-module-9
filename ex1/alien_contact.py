from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import model_validator, ValidationError

"""Enums are fixed sets of values"""
"""We need enums to represent types of alien contacts in this exercise"""


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


"""ContactType.radio is now a valid type"""
"""This is better than using raw steings because Pydantic can validate
automatically that only one of the defined types is used"""


"""mode="after" validates after all fields are populated"""
"""values is a dict like object with all field values"""
"""Pydantic allows you to check the entire model at once after all individual
fields are validated"""


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_buisness_rules(self):
        #  contact id with start with "AC"
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

    #  physical contacts must be verified
        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact must be verified")

    #  telepathic contacts require at least 3 witnesses
        if (self.contact_type == ContactType.telepathic and
                self.witness_count < 3):
            raise ValueError("Telepathic contacts require "
                             "at least 3 witnesses")

    # strong signals (>7.0) must have a message
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (>7.0) must include a message")

        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)

    valid_contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp="2024-01-15T14:30:00",
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=False
    )
    print("Valid contact report:")
    print(f"ID: {valid_contact.contact_id}")
    print(f"Type: {valid_contact.contact_type.value}")
    print(f"Location: {valid_contact.location}")
    print(f"Signal: {valid_contact.signal_strength}/10")
    print(f"Duration: {valid_contact.duration_minutes} minutes")
    print(f"Witnesses: {valid_contact.witness_count}")
    print(f"Message: '{valid_contact.message_received}'")
    print()
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp="2024-01-15T14:30:00",
            location="Roswell",
            contact_type=ContactType.telepathic,
            signal_strength=6.5,
            duration_minutes=30,
            witness_count=1,
            message_received=None
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e)


if __name__ == "__main__":
    main()
