from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationships

Base = declarative_base()


class Mod(Base):
    __tablename__ = 'mod'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gameId = Column(Integer)
    summary = Column(Text)

    authors = relationships("User", backref="mod", order_by="User.id")


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    twitchId = Column(Integer)
    """
    {
        "name": "FTB",
        "url": "https://www.curseforge.com/members/17809311-ftb?username=ftb",
        "projectId": 283861,
        "id": 182372,
        "projectTitleId": null,
        "projectTitleTitle": null,
        "userId": 17809311,
        "twitchId": 151020426
    }
    """
