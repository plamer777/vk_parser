"""This file contains the Group classes serves as models to store, process
and validate data"""
from pydantic import BaseModel
# --------------------------------------------------------------------------


class Group(BaseModel):
    """This class represents a VK group"""
    column_num: int | None = None
    id: str = ''
    name: str = ''
    description: str = ''
    fixed_post: str = ''
    status: str = ''
    tags: str = ''

    class Config:
        orm_mode = True
