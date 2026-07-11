from project.database import Select, Update


class AdminMessagesService:
    # Fetch all non-dismissed admin messages
    @staticmethod
    def fetch_all_messages() -> list:
        return Select.select_all_admin_messages()

    # Mark an admin message as dismissed, return if successful
    @staticmethod
    def dismiss_message(message_id: int) -> bool:
        return Update.dismiss_admin_message(message_id)

    # Fetch the data of a specific admin message
    @staticmethod
    def fetch_message_data(message_id: int) -> dict | None:
        return Select.select_admin_message(message_id)
