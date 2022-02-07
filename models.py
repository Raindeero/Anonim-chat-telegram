from pydantic import BaseModel

from temp import Sexes


class UserData(BaseModel):
    # Main user data
    id: int
    sex: Sexes
    name: str
    age: int

    # User`s preferences
    sex_partner: Sexes
    age_partner_from: int
    age_partner_to: int

    # Partner id
    meeting_id: int
