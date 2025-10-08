from typing import List,Dict
from typing_extensions import Annotated,Optional
from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: Annotated[str, Field(description="Title of the movie to recommend")]
    synopsis: Annotated[str, Field(description="Short description without spoilers")]
    reason_for_recommendation: Annotated[
        str, Field(description="Reason why the movie was recommended to the user")
    ]
    emotions: Annotated[List[str], Field(description="Emotions the movie is link to")]




class Input(BaseModel):
    preferences: Annotated[List[str], Field(description="User's preferences")]
    score: Annotated[Dict[str, int], Field(description="User's personality traits")]
    blacklist: Annotated[List[str], Field(description="Movies to avoid")]

    





class Output(BaseModel):
    movies: Annotated[List[Movie], Field(description="List of recommended movies")]
