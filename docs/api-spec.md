# Beatoven.ai Track Composition API

Base URL: https://public-api.beatoven.ai

## Authentication

Beatoven.ai API uses an API token based authentication (using Bearer authentication method). With each request, you need to include your API token as a bearer token in the `Authorization` request header. For example, if your API token is `qIN5iSz0CrGcFi0Ic8pGH3k9_iq6BSpC`, then include the following header in each API request -

`Authorization: Bearer qIN5iSz0CrGcFi0Ic8pGH3k9_iq6BSpC`

### Other headers

All `POST` endpoints accept a json body, so please include `content-type: application/json` in your requests.

> You can find our older/ soon to be deprecated API spec [here](https://raw.githubusercontent.com/Beatoven/public-api/refs/heads/main/docs/api-spec-old.md).

## Composing a track

You can use the compose API with `prompt` to compose the track.

## Request

**Endpoint**

`POST /api/v1/tracks/compose`

**Payload**

```json
{
   "prompt": {
      "text": "30 seconds peaceful lo-fi chill hop track"
   },
   "format": "wav", // optional
   "looping": false // optional
}
```

**Description**

- `prompt`: The prompt for the track.
- `format`: format of the generated assets. Can be chosen as `mp3`, `aac` and `wav`. Default is `wav`
- `looping`: control the extent of looping in the track. Set `true` for higher amount of looping. The default value is `false`

### Response

If the composition request succeeds, an asynchronous process will begin and you'll be delivered a task ID in the success response.

**Example**:
```json
{
   "status": "started",
   "task_id": "ccb84650-7b4a-4d00-9f80-8a6427ca21aa_1"
}
```

## Checking composition status

Once a composition task has started, you can query the progress of the task using the status request.

## Request

**Endpoint**

`GET /api/v1/tasks/<task_id>`

**Arguments**
- `task_id`: Task ID returned in the response of the composition request.

## Response

**Example**

```json
{
   "status": "composed",
   "meta": {
      "project_id": "3ade3151-372d-4ac8-b1ef-866a67ef0875",
      "track_id": "ccb84650-7b4a-4d00-9f80-8a6427ca21aa",
      "prompt": {
         "text": "30 seconds peaceful lo-fi chill hop track"
      },
      "version": 1,
      "track_url":"<url-of-the-composed-track",
      "stems_url": {
         "bass": "<url-of-the-bass-track>",
         "chords": "<url-of-the-chords-track>",
         "melody": "<url-of-the-melody-track>",
         "percussion": "<url-of-the-percussion-track>"
      }
   }
}
```

**Description**

`status`: The value can be one of the following -

- `composing`: The task has been put in the queue
- `running`: The task has started running
- `composed`:  The composition task has finished and the generated assets are available
