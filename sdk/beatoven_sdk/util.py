import os

SDK_VERSION = "0.0.1"
DEFAULT_BASEPATH = "https://sync.beatoven.ai"


def get_version():
    return SDK_VERSION


def get_env():
    BEATOVEN_API_BASEPATH = os.getenv("BEATOVEN_API_BASEPATH", DEFAULT_BASEPATH)
    BEATOVEN_API_KEY = os.getenv("BEATOVEN_API_KEY", "")
    return BEATOVEN_API_BASEPATH, BEATOVEN_API_KEY
