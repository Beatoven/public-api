from .util import get_env
from .errors import (
    INVALID_URL_ERROR,
    INVALID_API_KEY_ERROR,
    SERVER_ERROR,
    CLIENT_ERROR,
    CLIENT_CONNECTION_ERROR,
    BAD_REQUEST_ERROR,
)
import aiohttp

HTTP_CLIENT_TIMEOUT = aiohttp.ClientTimeout(total=10)
API_BASEPATH = "/api/v1"
AUTHORIZATION_HEADER = "Authorization"
AUTH_HEADER_PREFIX = "api_key "


async def list_tracks():
    BEATOVEN_API_BASEPATH, BEATOVEN_API_KEY = get_env()
    async with aiohttp.ClientSession(timeout=HTTP_CLIENT_TIMEOUT) as session:
        try:
            async with session.get(
                f"{BEATOVEN_API_BASEPATH}{API_BASEPATH}/tracks",
                headers={
                    AUTHORIZATION_HEADER: f"{AUTH_HEADER_PREFIX}{BEATOVEN_API_KEY}"
                },
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 400:
                    raise Exception({"error": BAD_REQUEST_ERROR})
                elif response.status == 401:
                    raise Exception({"error": INVALID_API_KEY_ERROR})
                elif response.status == 500:
                    raise Exception({"error": SERVER_ERROR})
        except aiohttp.InvalidURL as e:
            raise Exception({"error": INVALID_URL_ERROR}) from e
        except aiohttp.ClientConnectionError as e:
            raise Exception({"error": CLIENT_CONNECTION_ERROR}) from e
        except aiohttp.ClientError as e:
            raise Exception({"error": CLIENT_ERROR}) from e
        except:
            raise


async def get_track(track_id):
    BEATOVEN_API_BASEPATH, BEATOVEN_API_KEY = get_env()
    async with aiohttp.ClientSession(timeout=HTTP_CLIENT_TIMEOUT) as session:
        try:
            async with session.get(
                f"{BEATOVEN_API_BASEPATH}{API_BASEPATH}/tracks/{track_id}",
                headers={
                    AUTHORIZATION_HEADER: f"{AUTH_HEADER_PREFIX}{BEATOVEN_API_KEY}"
                },
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 400:
                    raise Exception({"error": BAD_REQUEST_ERROR})
                elif response.status == 401:
                    raise Exception({"error": INVALID_API_KEY_ERROR})
                elif response.status == 500:
                    raise Exception({"error": SERVER_ERROR})
        except aiohttp.InvalidURL as e:
            raise Exception({"error": INVALID_URL_ERROR}) from e
        except aiohttp.ClientConnectionError as e:
            raise Exception({"error": CLIENT_CONNECTION_ERROR}) from e
        except aiohttp.ClientError as e:
            raise Exception({"error": CLIENT_ERROR}) from e
        except:
            raise


async def create_track(track_data):
    BEATOVEN_API_BASEPATH, BEATOVEN_API_KEY = get_env()
    async with aiohttp.ClientSession(timeout=HTTP_CLIENT_TIMEOUT) as session:
        try:
            async with session.post(
                f"{BEATOVEN_API_BASEPATH}{API_BASEPATH}/tracks",
                json=track_data,
                headers={
                    AUTHORIZATION_HEADER: f"{AUTH_HEADER_PREFIX}{BEATOVEN_API_KEY}"
                },
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 400:
                    raise Exception({"error": BAD_REQUEST_ERROR})
                elif response.status == 401:
                    raise Exception({"error": INVALID_API_KEY_ERROR})
                elif response.status == 500:
                    raise Exception({"error": SERVER_ERROR})
        except aiohttp.InvalidURL as e:
            raise Exception({"error": INVALID_URL_ERROR}) from e
        except aiohttp.ClientConnectionError as e:
            raise Exception({"error": CLIENT_CONNECTION_ERROR}) from e
        except aiohttp.ClientError as e:
            raise Exception({"error": CLIENT_ERROR}) from e
        except:
            raise


async def compose_track(track_id, track_data):
    BEATOVEN_API_BASEPATH, BEATOVEN_API_KEY = get_env()
    async with aiohttp.ClientSession(timeout=HTTP_CLIENT_TIMEOUT) as session:
        try:
            async with session.post(
                f"{BEATOVEN_API_BASEPATH}{API_BASEPATH}/tracks/{track_id}/compose",
                json=track_data,
                headers={
                    AUTHORIZATION_HEADER: f"{AUTH_HEADER_PREFIX}{BEATOVEN_API_KEY}"
                },
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 400:
                    raise Exception({"error": BAD_REQUEST_ERROR})
                elif response.status == 401:
                    raise Exception({"error": INVALID_API_KEY_ERROR})
                elif response.status == 500:
                    raise Exception({"error": SERVER_ERROR})
        except aiohttp.InvalidURL as e:
            raise Exception({"error": INVALID_URL_ERROR}) from e
        except aiohttp.ClientConnectionError as e:
            raise Exception({"error": CLIENT_CONNECTION_ERROR}) from e
        except aiohttp.ClientError as e:
            raise Exception({"error": CLIENT_ERROR}) from e
        except:
            raise


async def get_task_status(task_id):
    BEATOVEN_API_BASEPATH, BEATOVEN_API_KEY = get_env()
    async with aiohttp.ClientSession(timeout=HTTP_CLIENT_TIMEOUT) as session:
        try:
            async with session.get(
                f"{BEATOVEN_API_BASEPATH}{API_BASEPATH}/status/{task_id}",
                headers={
                    AUTHORIZATION_HEADER: f"{AUTH_HEADER_PREFIX}{BEATOVEN_API_KEY}"
                },
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 400:
                    raise Exception({"error": BAD_REQUEST_ERROR})
                elif response.status == 401:
                    raise Exception({"error": INVALID_API_KEY_ERROR})
                elif response.status == 500:
                    raise Exception({"error": SERVER_ERROR})
        except aiohttp.InvalidURL as e:
            raise Exception({"error": INVALID_URL_ERROR}) from e
        except aiohttp.ClientConnectionError as e:
            raise Exception({"error": CLIENT_CONNECTION_ERROR}) from e
        except aiohttp.ClientError as e:
            raise Exception({"error": CLIENT_ERROR}) from e
        except:
            raise
