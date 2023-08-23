from this import d
from typing import List
import asyncio
import os
import aiohttp
import aiofiles

BACKEND_V1_API_URL = "https://sync.beatoven.ai/api/v1"
BACKEND_API_HEADER_KEY = os.getenv("BEATOVEN_API_KEY", "")

async def create_track(request_data):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{BACKEND_V1_API_URL}/tracks",
                json=request_data,
                headers={"Authorization": f"api_key {BACKEND_API_HEADER_KEY}"},
            ) as response:
                print(response)
                data = await response.json()
                return data
        except aiohttp.ClientConnectionError as e:
            return {"error": "Could not connect to beatoven.ai"}
        except:
            return {"error": "Failed to make a request to beatoven.ai"}


async def compose_track(request_data, track_id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{BACKEND_V1_API_URL}/tracks/{track_id}/compose",
                json=request_data,
                headers={"Authorization": f"api_key {BACKEND_API_HEADER_KEY}"},
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return {"error": "Failed to compose a track"}
        except aiohttp.ClientConnectionError:
            return {"error": "Could not connect to beatoven.ai"}
        except:
            return {"error": "Failed to make a request to beatoven.ai"}


async def get_track_status(task_id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{BACKEND_V1_API_URL}/status/{task_id}",
                headers={"Authorization": f"api_key {BACKEND_API_HEADER_KEY}"},
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return {"error": "Composition failed"}
        except aiohttp.ClientConnectionError as e:
            return {"error": "Could not connect"}
        except:
            return {"error": "Failed to make a request"}


async def handle_track_file(track_path: str, track_url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(track_url) as response:
                if response.status == 200:
                    async with aiofiles.open(track_path, "wb+") as f:
                        await f.write(await response.read())
                        return {}
        except aiohttp.ClientConnectionError as e:
            return {"error": "Could not download file"}
        except:
            return {"error": "Failed to make a request to get track file"}


async def watch_task_status(task_id, interval=5):
    while True:
        track_status = await get_track_status(task_id)
        if "error" in track_status:
            return track_status

        if track_status["state"] == "PENDING":
            await asyncio.sleep(interval)
        elif track_status["state"] == "FAILURE":
            return {"error": "task failed"}
        elif track_status["state"] == "PROGRESS":
            progress_info = track_status["meta"]
            progress_percentage = int(progress_info["percentage"])
            print(f"Composition progress: {progress_percentage}%")
            await asyncio.sleep(interval)
        else:
            return track_status


async def create_and_compose(duration=30000, genre="cinematic", mood="happy", tempo="medium"):
    track_meta = {
        "title": "my track",
        "duration_ms": duration,
        "genre": genre,
        "tempo": tempo,
        "sections": [
            {
                "start": 0,
                "length": 30000,
                "emotion": mood,
            }
        ]
    }

    track_obj = await create_track(track_meta)
    track_id = track_obj["uuid"]
    print(f"Created track with ID: {track_id}")

    compose_res = await compose_track(track_meta, track_id)
    task_id = compose_res["task_id"]
    print(f"Started composition task with ID: {task_id}")

    generation_meta = await watch_task_status(task_id)
    track_url =  generation_meta["meta"][0][0]["track_url"]
    print(f"Downloading track file")
    await handle_track_file(os.path.join(os.getcwd(), "composed_track.mp3"), track_url)


if __name__ == '__main__':
    asyncio.run(create_and_compose())
