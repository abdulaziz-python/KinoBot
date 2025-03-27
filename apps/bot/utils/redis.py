import json
import os

import redis

redis_instance = redis.StrictRedis.from_url(os.getenv("REDIS_CACHE_URL"))


def set_user_session(user_id: int, cinemas: list, page: int) -> None:
    """
    Sets the user session in Redis with the given cinemas and page number.
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
    redis_instance.set(f"user_session:{user_id}", json.dumps(session_data))


def get_user_session(user_id: int):
    """
    Redis'dan foydalanuvchi sessiyasini oladi.
    """
    session = redis_instance.get(f"user_session:{user_id}")
    if session:
        return json.loads(session)  # noqa
    return None


def delete_user_session(user_id: int):
    """
    Deletes the user session from Redis if it exists.
    """
    if redis_instance.exists(f"user_session:{user_id}"):
        redis_instance.delete(f"user_session:{user_id}")
