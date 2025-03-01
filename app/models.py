from sqlalchemy import Column, Integer, String, ARRAY, JSON, Boolean
from .database import Base
from typing import List
import json
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    email = Column(String, unique=True, index=True)
    city = Column(String)
    interests = Column(JSON)

    def set_interests(self, interests):
        self.interests = json.dumps(interests)

    def get_interests(self):
        return json.loads(self.interests)