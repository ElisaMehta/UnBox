from config import db
from sqlalchemy.sql import func
from datetime import date, time



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(255))
    # user_address = db.relationship("Address", back_populates="users", cascade="all, delete, delete-orphan")
    password_hash=db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())

    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Address(db.Model):
    __tablename__ = "addresses" 
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(2))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    user = db.relationship('User', foreign_keys=[user_id])
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())
    
    def full_address(self):
        return self.address + ' ' + self.city

class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))
    option = db.Column(db.String(4))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    user = db.relationship('User', foreign_keys=[user_id])
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id', ondelete='cascade'))
    address = db.relationship('Address', foreign_keys=[address_id])
    phone = db.Column(db.String(11))
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())