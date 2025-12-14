from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal, Optional


tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# Pydantic Model to validate incoming data
class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=75, description="Age of the user")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the user")]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description="Height of the user")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Income of the user in lakhs")]
    smoker: Annotated[bool, Field(..., description="Whether the user is a smoker or not")]
    city: Annotated[str, Field(..., description="City of the user")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description="Occupation of the user")]

    @field_validator('city')  # Convert the city name to title case
    @classmethod
    def normalize_city(cls, v:str) -> str:
        return v.strip().lower().title()

    @computed_field
    @property 
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field 
    @property 
    def age_group(self) -> str:
        if self.age <= 18:
            return "Child"
        elif self.age > 18 and self.age <= 40:
            return "Young Adult"
        elif self.age > 40 and self.age <= 60:
            return "Middle Aged Adult"
        else:
            return "Senior Citizen"

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "High"
        elif self.smoker and self.bmi > 25:
            return "Medium"
        else:
            return "Low"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3