"""Authentication helpers for the Student Management System."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path


@dataclass(frozen=True)
class AdminCredentials:
    """Simple container for admin credential details."""

    username: str
    password_hash: str


class Authenticator:
    """Validates administrator login credentials."""

    def __init__(self, credentials_file: Path) -> None:
        self.credentials_file = credentials_file
        self.credentials = self._load_credentials()

    def _load_credentials(self) -> AdminCredentials:
        """Load admin credentials from the configured file."""
        default_credentials = AdminCredentials(
            username="admin",
            password_hash=self._hash_password("admin123"),
        )

        if not self.credentials_file.exists():
            self.credentials_file.parent.mkdir(parents=True, exist_ok=True)
            self.credentials_file.write_text(
                "username=admin\npassword_hash="
                f"{default_credentials.password_hash}\n",
                encoding="utf-8",
            )
            return default_credentials

        entries: dict[str, str] = {}
        for line in self.credentials_file.read_text(encoding="utf-8").splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", maxsplit=1)
            entries[key.strip()] = value.strip()

        username = entries.get("username", default_credentials.username)
        password_hash = entries.get("password_hash", default_credentials.password_hash)
        return AdminCredentials(username=username, password_hash=password_hash)

    @staticmethod
    def _hash_password(password: str) -> str:
        """Return the SHA-256 hash for a password."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def authenticate(self, username: str, password: str) -> bool:
        """Return True when the provided credentials are valid."""
        return (
            username == self.credentials.username
            and self._hash_password(password) == self.credentials.password_hash
        )
