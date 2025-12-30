from __future__ import annotations

from typing import Any

from airflow.api_fastapi.auth.managers.base_auth_manager import BaseAuthManager
from airflow.api_fastapi.auth.managers.models.base_user import BaseUser


class LocalAuthUser(BaseUser):
    def __init__(self, username: str = "dev", role: str | None = "ADMIN") -> None:
        self.username = username
        self.role = role

    def get_id(self) -> str:
        return self.username

    def get_name(self) -> str:
        return self.username

    def get_role(self) -> str | None:
        return self.role


class LocalAuthManager(BaseAuthManager[LocalAuthUser]):
    """Very small permissive auth manager for local Windows development only.

    This avoids importing `fcntl` (used by the default simple auth manager)
    which is unavailable on native Windows. Do NOT use in production.
    """

    def deserialize_user(self, token: dict[str, Any]) -> LocalAuthUser:
        username = token.get("sub", "dev")
        role = token.get("role", "ADMIN")
        return LocalAuthUser(username=username, role=role)

    def serialize_user(self, user: LocalAuthUser) -> dict[str, Any]:
        return {"sub": user.get_id(), "role": user.get_role()}

    def get_url_login(self, **kwargs) -> str:
        return "/login"

    def get_url_logout(self) -> str | None:
        return None

    def is_authorized_configuration(self, *, method: str, user: LocalAuthUser, details: Any | None = None) -> bool:
        return True

    def is_authorized_connection(self, *, method: str, user: LocalAuthUser, details: Any | None = None) -> bool:
        return True

    def is_authorized_dag(self, *, method: str, user: LocalAuthUser, access_entity: Any | None = None, details: Any | None = None) -> bool:
        return True

    def is_authorized_backfill(self, *, method: str, user: LocalAuthUser, details: Any | None = None) -> bool:
        return True

    def is_authorized_asset(self, *, method: str, user: LocalAuthUser, details: Any | None = None) -> bool:
        return True

    def is_authorized_asset_alias(self, *, method: str, user: LocalAuthUser, details: Any | None = None) -> bool:
        return True

    def is_authorized_pool(self, *, method: str, user: LocalAuthUser, details: Any | None = None) -> bool:
        return True

    def is_authorized_variable(self, *, method: str, user: LocalAuthUser, details: Any | None = None) -> bool:
        return True

    def is_authorized_view(self, *, access_view: Any, user: LocalAuthUser) -> bool:
        return True

    def is_authorized_custom_view(self, *, method: str | Any, resource_name: str, user: LocalAuthUser) -> bool:
        return True

    def filter_authorized_menu_items(self, menu_items: list[Any], *, user: LocalAuthUser) -> list[Any]:
        return menu_items
