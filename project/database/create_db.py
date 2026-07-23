from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(67), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)  # Only store password hash
    status = db.Column(db.String(20), default="STANDARD USER", nullable=False)
    gender = db.Column(db.String(67), default="sigma/male", nullable=False)
    age = db.Column(db.Integer, default=-1, nullable=False)
    location = db.Column(db.String(67), default="private", nullable=False)
    bio = db.Column(
        db.String(255),
        default="This person is too busy chatting to write a bio!",
        nullable=False,
    )
    banned = db.Column(db.Boolean, default=False, nullable=False)
    # Default for ban end should really be 0
    ban_end = db.Column(db.Integer, default=int(datetime.now().timestamp()))
    colour = db.Column(db.String(255), default="Blue", nullable=False)
    email = db.Column(db.String(255))
    email_verification_code = db.Column(db.Integer)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)

    room_access = db.relationship("RoomAccess", backref="user")
    admin_messages = db.relationship("AdminMessage", backref="user")
    room_message = db.relationship("RoomMessage", backref="user")


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_name = db.Column(db.String(67), unique=True, nullable=False)
    public = db.Column(db.Boolean, default=True)

    room_access = db.relationship("RoomAccess", backref="room")
    room_message = db.relationship("RoomMessage", backref="room")


class RoomAccess(db.Model):
    __tablename__ = "room_access"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)


class AdminMessageType(db.Model):
    __tablename__ = "admin_message_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)

    admin_messages = db.relationship("AdminMessage", backref="message_type")


class AdminMessage(db.Model):
    __tablename__ = "admin_messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(1670), nullable=False)
    dismissed = db.Column(db.Boolean, default=False, nullable=False)

    type_id = db.Column(
        db.Integer, db.ForeignKey("admin_message_types.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class RoomMessage(db.Model):
    __tablename__ = "room_messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
