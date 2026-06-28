from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(67), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)  # Only store password hash
    status = db.Column(db.String(20), default="Believer")

    room_access = db.relationship("RoomAccess", backref="user")


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_name = db.Column(db.String(67), unique=True, nullable=False)

    room_access = db.relationship("RoomAccess", backref="room")


class RoomAccess(db.Model):
    __tablename__ = "room_access"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
