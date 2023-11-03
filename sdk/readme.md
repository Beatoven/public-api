# Beatoven Public SDK

## Usage

If you are interested in using the SDK, please get in touch with hello@beatoven.ai. We would like to discuss your use-case(s) and issue an API key for your application.


```python
import os

os.environ["BEATOVEN_API_KEY"] = ""
```

## Install

Install the python package from git

`!python -m pip install -e "git+https://github.com/Beatoven/public-api.git/#subdirectory=sdk"`


```python
import beatoven_sdk

beatoven_sdk.get_version()
```

### List all tracks


```python
tracks = await beatoven_sdk.list_all_tracks()
```

### Compose new track


```python
track_id, track_url = await beatoven_sdk.create_new_track(
    title="my sdk track",
    track_duration=30000,
    track_genre="cinematic",
    track_tempo="medium",
    mood="happy",
)
```

### Get existing track by ID


```python
track_id, track_url = await beatoven_sdk.get_track_by_id(tracks[0]["id"])
```

### Download track


```python
import aiofiles
import aiohttp

track_file_path = os.path.join(os.getcwd(), "composed_track.mp3")
async with aiohttp.ClientSession() as session:
    async with session.get(track_url) as response:
        if response.status == 200:
            async with aiofiles.open(track_file_path, "wb+") as f:
                await f.write(await response.read())
print("Composed! you can find your track at `composed_track.mp3`")
```

    Composed! you can find your track at `composed_track.mp3`

