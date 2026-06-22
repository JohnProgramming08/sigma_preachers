import hashlib


class HashService:
    # Return the hash value of the given string
    @staticmethod
    def hash(password: str) -> int:
        full_hashed_password = int(
            hashlib.sha256(password.encode("utf-8")).hexdigest(), 16
        )
        password_hash = full_hashed_password % (10**8)

        return password_hash
