from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    avatarUrl = Column(String)
    parentGameCategoryId = Column(Integer)
    rootGameCategoryId = Column(Integer)
    gameId = Column(Integer)


class Mod(Base):
    __tablename__ = 'mods'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    websiteUrl = Column(String)
    summary = Column(String)
    defaultFileId = Column(Integer)
    downloadCount = Column(Integer)
    gameId = Column(Integer)
    status = Column(Integer)
    primaryCategoryId = Column(Integer)
    slug = Column(String)
    isFeatured = Column(Boolean)
    popularityScore = Column(Float)
    gamePopularityRank = Column(Integer)
    primaryLanguage = Column(String)
    gameSlug = Column(String)
    gameName = Column(String)
    portalName = Column(String)
    dateModified = Column(TIMESTAMP)
    dateCreated = Column(TIMESTAMP)
    dateReleased = Column(TIMESTAMP)
    isAvailable = Column(Boolean)
    # TODO(dmauldin): curse has this as "isExperiemental", so take care
    isExperimental = Column(Boolean)
    # ARRAYS
    authors = relationship("ModAuthor", backref="mod")
    # authors
    # attachments
    # latestFiles
    # categories
    # categorySection
    # gameVersionLatestFiles


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    mods = relationship("ModAuthor", backref="user")


class ModAuthor(Base):
    __tablename__ = 'author_mod'
    # TODO(dmauldin): figure out best practice for class member casing (userId vs user_id) in python
    userId = Column(Integer(), ForeignKey("users.id")),
    mod_id = Column(Integer(), ForeignKey("mods.id"))
    twitch_id = Column(Integer)
