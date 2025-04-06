import json
import os

from django.core.cache import cache

def set_user_session(user_id: int, cinemas: list, page: int) -> None:
    """
    Sets the user session in cache with the given cinemas and page number.
    """
    session_data = {
        "cinemas": [
            {
                "id": f["id"] if isinstance(f, dict) else f.cinema.id,
                "title": f["title"] if isinstance(f, dict) else f.cinema.title,
                "view_count": (
                    f["view_count"] if isinstance(f, dict) else f.cinema.view_count
                ),
            }
            for f in cinemas
        ],
        "page": page,
    }
    cache.set(f"user_session:{user_id}", json.dumps(session_data), timeout=3600)


def get_user_session(user_id: int):
    """
    Cache'dan foydalanuvchi sessiyasini oladi.
    """
    session = cache.get(f"user_session:{user_id}")
    if session:
        return json.loads(session)  # noqa
    return None


def delete_user_session(user_id: int):
    """
    Deletes the user session from cache if it exists.
    """
    cache.delete(f"user_session:{user_id}")
