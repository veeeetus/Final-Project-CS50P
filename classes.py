from hashlib import sha256
from colorama import Fore
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)

    sites = relationship("Site", back_populates = "user")

    # String representation of object
    def __str__(self):
        return f"{Fore.GREEN}\nUsername: {self.username}\nPassword hash: {self.password_hash}\n"


class Site(Base):
    __tablename__ = "Site"

    site_id = Column(Integer, primary_key=True)
    site = Column(String)
    login = Column(String)
    password = Column(String)
    user_id = Column(Integer, ForeignKey("User.user_id"))

    user = relationship("User", back_populates="sites")

    def __init__(self, site, login, password, user_id):
        self.site = site
        self.login = login
        self.password = password
        self.user_id = user_id
    
    def __str__(self):
        return f"{Fore.GREEN}\nId: {self.site_id}\nSite: {self.site}\nLogin: {self.login}\nPassword: {self.password}"
