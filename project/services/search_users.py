from project.database import Select


class SearchUsersService:
    def __init__(self, username_start: str, start: int) -> None:
        self.username_start = username_start
        self.start = start

    # Fetch the next 10 users whose usernames start with username_start
    def fetch_next_10_users(self) -> dict:
        user_pairs = Select.select_users_with_username(
            self.username_start, self.start
        )
        res = {}
        for pair in user_pairs:
            res[pair[1]] = pair[0]

        return res
