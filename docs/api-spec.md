# Beatoven.ai Track Composition API

Base URL: https://sync.beatoven.ai

## Authentication

Beatoven.ai API uses an API token based authentication. With each request, you need to include your API token in the `Authorization` request header. For example, if your API token is `qIN5iSz0CrGcFi0Ic8pGH3k9_iq6BSpC`, then include the following header in each API request -

`Authorization: api_key qIN5iSz0CrGcFi0Ic8pGH3k9_iq6BSpC`

## Endpoints

- [Creating a track](https://github.com/Beatoven/public-api/blob/main/docs/api-spec.md#creating-a-new-track)
- [Composing a track](https://github.com/Beatoven/public-api/blob/main/docs/api-spec.md#composing-a-track)
- [Fetching Instruments](https://github.com/Beatoven/public-api/blob/main/docs/api-spec.md#fetching-instruments)
- [Checking composition status](https://github.com/Beatoven/public-api/blob/main/docs/api-spec.md#checking-composition-status)
- [Fetching a track](https://github.com/Beatoven/public-api/blob/main/docs/api-spec.md#get-composed-track)
- [Fetching supported options](https://github.com/Beatoven/public-api/blob/main/docs/api-spec.md#supported-options)

## Creating a new track

Before composing a track, you'll need to create/initialize a track.

### Request

**Endpoint**

`POST /api/v2/tracks`

**Payload Example**

`prompt`: Text instruction used to compose music.

```json
{
  "prompt": "Make a 30 second upbeat EDM track for a party"
}
```

### Response

On successful creation, you'll get a track object in response.

**Example**

```json
{
  "status": "Created successfully",
  "track": {...},
  "uuid": "81b38b35-6535-4230-9e34-7c123e7d1348"
}
```

**Description**

`uuid`: This is the unique ID of the track that has been created. For further, operations on track, you'll need to save this on your end and pass it along with other requests.

## Composing a track

Once a track has been created, you can get new compositions, either with the already set parameters of the track or with new ones.

### Request

**Endpoint**

`POST /api/v2/tracks/<track_id>/compose`

**Arguments**

- `track_id`: Track ID returned in the response of the track creation request.

**Payload**

Same as track creation payload.

### Response

If the composition request succeeds, an asynchronous process will begin and you'll be delivered a task ID in the success response.

**Example**:

```json
{ "task_id": "abcd442-baus4394-ajos4834-mvn7bffd" }
```

## Checking composition status

Once a composition task has started, you can query the progress of the task using the status request.

### Request

**Endpoint**

`GET /api/v2/status/<task_id>`

**Arguments**

- `task_id`: Task ID returned in the response of the composition request.

### Response

**Example**

```json
{
  "meta": {
    "message": "Mixing your track",
    "payload": {...},
    "percentage": 70
  },
  "state": "PROGRESS"
}
```

**Description**

`state`: The value can be one of the following -

- `pending`: The task has not started yet
- `failure`: The task has failed
- `progress`: The task is in progress. The response object has additional metadata regarding how much the task has progressed. The value is stored in `generationProgress` field.
- `success`: The task has succeeded. The response object has additional metadata of the composed track assets which you'll need to extract to listen to the track. See below for details.

### Successful Composition

Once a composition task finishes successfully, the status request along with reporting `success` as `state`, will also return information about composed track assets. This is basically a list of four tracks composed by Beatoven.ai, each item is further a list (an item per section) containing the URLs to the composed track file for that section and a shorter preview of the same.

**Example**

```json
{
  "meta": {
    "download_url": "<signed_s3_url>",
    "section_options": [
      [
        {
          "instruments": [
            "bass-bass",
            "percussion-percussion",
            "chords-chords",
            "melody-melody"
          ],
          "option_number": 0,
          "preview_url": "<signed_s3_url>",
          "section_bar_boundary": [0, 15.0],
          "section_duration": 30000.0,
          "tempo": 120.0,
          "track_url": "<signed_s3_url>"
        }
      ]
    ]
  },
  "state": "SUCCESS"
}
```

**Description**

`download_url`: Complete composed track in mp3 format

`section_options`: List of sections of the composed track and each section is further a list with track information. The list is sorted at a section level which means the first list is the first section and so on. So if you have two sections in your track, each item will have two objects and each of the objects will contain the following fields:

`instruments`: List of instruments that appear in the composed tracks

`track_url`: URL to the composed track for that section. This is in .mp3 format

`preview_url`: URL to the short preview of the composed track for that section. This is in .mp3 format

`section_duration`: Duration of the section in milliseconds

## Fetching Instruments

To fetch individual instrument stems for a given track you would need to call this API, By default stems are not generated for a composed track

### Request

**Endpoint**

`POST /api/v2/tracks/<track_id>/instrument_urls`

**Arguments**

- `track_id`: Track ID returned in the response of the track creation request.
- `version`: (Optional) Track ID version

**Payload**

Empty JSON

```
{}
```

### Response

If the composition request succeeds, an asynchronous process will begin and you'll be delivered a task ID in the success response.

**Example**:

```json
{ "task_id": "d5b63125-2cea-4709-8e46-1fc040116a9d" }
```

Check the composition status through the status API similar as mentioned [here](https://github.com/Beatoven/public-api/blob/main/docs/api-spec.md#checking-composition-status)

### Successful Instrument Fetch

Once a composition task finishes successfully, the status request along with reporting success as state, will also return individual stems for the composed track

**Example**

```json
{
  "meta": [
    [
      {
        "<instrument_name>": {
          "preview_url": "",
          "track_url": "/some/url/stem/melody.mp3"
        }
      }
    ],
    [],
    []
  ]
}
```

**Description**

`meta`: Similar to compose API response instrument fetch also returns stem urls at a section level. Each section is a list with a dictionary containing the following fields

`instrument`: Name of the stem eg: chords,melody,bass,percussion and each stem contains these two url that can be used to download them:

`track_url`: URL to the composed section for that instrument. This is in .mp3 format

`preview_url`: URL to the short preview of the composed section for that instrument. This is in .mp3 format

## GET composed track

To fetch all the track urls for an already composed track. This API requires that the [fetching instruments API](https://github.com/Beatoven/public-api/blob/main/docs/api-spec.md#fetching-instruments) call has already been made

### Request

**Endpoint**

`GET /api/v2/tracks/<track_id>`

**Arguments**

- `track_id`: Track ID returned in the response of the track creation request.
- `version`: (Optional) Track ID version

### Response

Response returns the downloadable url, section level urls and instrument level urls (if they exists)

**Example**:

```json
{
  "download_url": "<signed_s3_url>",
  "section_options": "<section_options>",
  "instrument_urls": "<instrument_urls>",
  "prompts": ["<prompt>"]
}
```

`download_url`: Complete composed track in mp3 format

`section_options`: Same as meta [here](https://github.com/Beatoven/public-api/blob/main/docs/api-spec.md#successful-composition)

`instrument_urls`: Same as meta [here](https://github.com/Beatoven/public-api/blob/main/docs/api-spec.md#successful-instrument-fetch)

## Supported Options

You can use this API, to get the supported values for track parameters like genre, moods and tempo. In this API, you'll also get a list of combinations that may lead to errors. You can use pick the parameters and hardcode them into your application but it'd be recommended that your application fetches these parameters dynamically on launch.

**Endpoint**

`GET /api/v2/composition_params`

**Payload Example**

```json
{
  "genre": [
    "indian",
    "pop",
    "ambient",
    "indie",
    "rnb",
    "cinematic",
    "hiphop",
    "electronic"
  ],
  "emotion": [
    "sad",
    "calm",
    "motivational",
    "happy",
    "scary",
    "cheerful",
    "angry",
    "triumphant",
    "relaxing",
    "depressing",
    "dreamy",
    "inspirational",
    "energetic",
    "joyful",
    "tense",
    "fearful"
  ],
  "tempo": ["slow", "medium", "fast"],
  "blockedParams": [
    {
      "genre": "rnb",
      "moods": [
        "tense",
        "angry",
        "scary",
        "fearful",
        "sad",
        "inspirational",
        "depressing",
        "motivational",
        "triumphant"
      ],
      "tempo": "slow"
    },
    {
      "genre": "rnb",
      "moods": ["inspirational", "motivational", "triumphant"],
      "tempo": "fast"
    },
    {
      "genre": "indie",
      "moods": ["energetic"],
      "tempo": "slow"
    },
    {
      "genre": "indie",
      "mood": ["energetic"],
      "tempo": "medium"
    },
    {
      "genre": "cinematic",
      "moods": ["energetic"],
      "tempo": "slow"
    },
    {
      "genre": "hiphop",
      "moods": ["energetic"],
      "tempo": "slow"
    }
  ]
}
```

**Payload Description**

Fields like `genre`, `mood` and `tempo` might be self-explainatory.

`blockedParameters`: While most of the options in genre, mood and tempo can be combined to create a track. Some combinations might lead to errors due to limitations in our composition system. The list in the value of `blockedParameters` is a list of those combinations.
