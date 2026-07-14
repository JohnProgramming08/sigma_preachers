from flask_socketio import SocketIO, send, emit, join_room, leave_room


class WebsocketService:
    # Handle a user joining a room
    @staticmethod
    def join(username: str, room_name: str) -> None:
        join_room(room_name)
        message = {"sender": "SERVER", "message": f"{username} joined the chat"}

        emit("message", message, room=room_name)

    # Handle a user sending a message
    @staticmethod
    def message(
        username: str, room_name: str, data: str, colour: str = "Blue"
    ) -> None:
        message = {"sender": username, "message": data, "colour": colour}

        emit("message", message, room=room_name)

    # Handle a user leaving a room
    @staticmethod
    def leave(username: str, room_name: str) -> None:
        message = {
            "sender": "SERVER",
            "message": f"{username} has left the chat",
        }

        emit(
            "message",
            message,
            room=room_name,
            include_self=False,
        )
