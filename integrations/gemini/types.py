from typing import List
from typing_extensions import Annotated
from pydantic import BaseModel, Field


class Input(BaseModel):
    name: Annotated[str, Field(description="User's name")]
    preferences: Annotated[List[str], Field(description="User's preferences")]
    personality: Annotated[List[str], Field(description="User's personality traits")]
    current_vibe: Annotated[
        str,
        Field(
            description="Current vibe or mood of the user, e.g., happy, sad, adventurous"
        ),
    ]


class Movie(BaseModel):
    title: Annotated[str, Field(description="Title of the movie to recommend")]
    synopsis: Annotated[str, Field(description="Short description without spoilers")]
    reason_for_recommendation: Annotated[
        str, Field(description="Reason why the movie was recommended to the user")
    ]
    tags: Annotated[List[str], Field(description="Keywords that describe the movie")]


class Output(BaseModel):
    movies: Annotated[List[Movie], Field(description="List of recommended movies")]
