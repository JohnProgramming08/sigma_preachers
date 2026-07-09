from project.database import Insert


class ContactUsService:
    def __init__(self, title: str, content: str, user_id: int, type_id: int):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.type_id = type_id

    # Send the message to the admins, returning if successful
    def send_admin_message(self) -> bool:
        return Insert.insert_admin_message(
            self.title, self.content, self.type_id, self.user_id
        )
