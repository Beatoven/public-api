from .api import get_track, list_tracks, create_track, compose_track, get_task_status
import asyncio


def extract_track_info(track):
    track_info = {}
    track_info["title"] = track["title"]
    track_info["id"] = track["project_id"]
    return track_info


async def list_all_tracks():
    tracks_data = await list_tracks()
    return list(map(extract_track_info, tracks_data["tracks"]))


async def get_track_by_id(track_id):
    track_data = await get_track(track_id)
    track_url = track_data["download_url"]
    return track_id, track_url


async def create_new_track(
    title=None,
    track_duration=30000,
    track_genre="cinematic",
    track_tempo="medium",
    mood="happy",
):
    if title == None:
        return None, None

    tracks = await list_all_tracks()
    for track in tracks:
        if track["title"] == title:
            return await get_track_by_id(track_id=track["id"])

    track_metadata = {
        "title": title,
        "duration_ms": track_duration,
        "genre": track_genre,
        "tempo": track_tempo,
        "sections": [
            {
                "start": 0,
                "length": track_duration,
                "emotion": mood,
            }
        ],
    }

    track_result = await create_track(track_data=track_metadata)
    track_id = track_result["uuid"]

    compose_result = await compose_track(track_id, track_metadata)
    task_id = compose_result["task_id"]

    generation_meta = await watch_task_status(task_id)
    track_url = generation_meta["meta"]["download_url"]

    return track_id, track_url


async def watch_task_status(task_id, interval=2):
    while True:
        track_status = await get_task_status(task_id)

        if "error" in track_status:
            raise Exception(track_status)
        elif track_status["state"] == "PENDING":
            await asyncio.sleep(interval)
        elif track_status["state"] == "FAILURE":
            raise Exception({"error": "task failed"})
        elif track_status["state"] == "PROGRESS":
            progress_info = track_status["meta"]
            progress_percentage = int(progress_info["percentage"])
            print(f"Composition progress: {progress_percentage}%")
            await asyncio.sleep(interval)
        else:
            return track_status
