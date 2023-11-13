from beatoven_sdk.client import list_all_tracks, compose_new_track, get_track_by_id
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def track_info():
    return "test track", 30000, "cinematic", "medium", "happy"


@pytest.mark.asyncio
async def test_compose_track(track_info):
    existing_tracks = await list_all_tracks()

    track_id, track_url = await compose_new_track(track_info)

    assert track_id != None
    assert track_url != None

    new_tracks = await list_all_tracks()
    assert len(new_tracks) == len(existing_tracks) + 1

    new_track_id, new_track_url = await get_track_by_id(track_id)

    assert new_track_id != None
    assert new_track_url != None
    assert new_track_url[: new_track_url.find("?")] == track_url[: track_url.find("?")]
