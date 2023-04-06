# Beatoven.ai Track Composition API

## Authentication

Beatoven.ai API uses an API token based authentication. With each request, you need to include your API token in the `Authorization` request header. For example, if your API token is `qIN5iSz0CrGcFi0Ic8pGH3k9_iq6BSpC`, then include the following header in each API request -

`Authorization: api_key qIN5iSz0CrGcFi0Ic8pGH3k9_iq6BSpC`

## Creating a new track

Before composing a track, you'll need to create/initialize a track.

### Request

**Endpoint**

`POST /api/v1/tracks`

**Payload Example**

This example request body will create a `1 minute` long track with the `Indie` genre and `happy` mood.

```json
{
    "duration_ms": 60000,
    "tempo": "medium",
    "title": "demo",
    "genre": "indie",
    "sections": [
        {
            "emotion": "happy",
            "length": 60000,
            "start": 0
        }
    ]
}
```

**Payload**

`genre`: Genre of a track can be specified here. Refer to this API to get the supported genres.

`duration_ms`: The duration of the track in milliseconds. 

`tempo`: Speed of the track. It can be changed to one of these values - `slow`, `medium`, `fast`.

`title`: Title of the track

`sections`: A track created on beatoven.ai can have one or more moods. To allow multiple moods, we divide a track into sections. By default, a track will have one section. For defining multiple moods, you'd need to define multiple sections. For example, to have two moods (`happy` and `angry`) in your track, the sections array would look like this -

```json
[
   {
      "emotion": "happy",
      "start": "0",
      "length": "30000"
   },
   {
      "emotion": "angry",
      "start": "30000",
      "length": "60000"
   }
]
```
Each section object requires the following fields - 

`emotion`: The mood/emotion of the resulting music for that section.  Refer to this API to get the supported emotions.

`start`: Duration in ms where you want that section the begin

`length`: Duration in ms for how long you want the section to continue

***Note***: When creating multiple sections, please ensure you cover the entire track duration with non-overlapping sections. That is, the second section should start where the first ends, and so on.

### Response

On successful creation, you'll get a track object in response.

**Example**
```json
{
   "status" : "Created successfully",
   "uuid" : "bd517be6-ce63-43f1-b0ad-475230fcd2b4",
   "track" : {
      "created_at" : "Tue, 04 Apr 2023 09:49:33 GMT",
      "duration_ms" : 60000,
      "genre" : "Ambient",     
      "sections" : [
         {
            "emotion" : "motivational",
            "length" : 60000,
            "start" : 0,
         }
      ],
      "tempo" : "medium",
      "title" : "Talented Anger created by API",
      "version" : 0
   }
}
```

**Description**

`uuid`: This is the unique ID of the track that has been created. For further, operations on track, you'll need to save this on your end and pass it along with other requests.

## Composing a track

Once a track has been created, you can get new compositions, either with the already set parameters of the track or with new ones.

## Request

**Endpoint**

`POST /api/v1/tracks/<track_id>`

**Arguments**
- `track_id`: Track ID returned in the response of the track creation request.

**Payload**

Same as track creation payload. You can omit this if you want to compose with the existing parameters.

### Response

If the composition request succeeds, an asynchronous process will begin and you'll be delivered a task ID in the success response.

**Example**:
```json
{"task_id": "abcd442-baus4394-ajos4834-mvn7bffd"}
```

## Checking composition status

Once a composition task has started, you can query the progress of the task using the status request.

## Request

**Endpoint**

`GET /api/v1/status/<task_id>`

**Arguments**
- `task_id`: Task ID returned in the response of the composition request.

## Response

**Example**

```json
{
   "meta" : {
      "message" : "Spicing up your composition",
      "percentage" : 64
   },
   "state" : "PROGRESS"
}
```

**Description**

`state`: The value can be one of the following -

- `pending`: The task has not started yet
- `failure`: The task has failed
- `progress`:  The task is in progress. The response object has additional metadata regarding how much the task has progressed. The value is stored in `generationProgress` field.
- `success`: The task has succeeded. The response object has additional metadata of the composed track assets which you'll need to extract to listen to the track. See below for details.

### Successful Composition

Once a composition task finishes successfully, the status request along with reporting `success` as `state`, will also return information about composed track assets. This is basically a list of four tracks composed by Beatoven.ai, each item is further a list (an item per section) containing the URLs to the composed track file for that section and a shorter preview of the same.

**Example**

```json
{
   "meta" : [
      [
         {
            "instruments" : [
               "percussion-tabla",
               "drone-tanpura",
               "melody-sarangi",
               "melody-sarod"
            ],
            "object_name" : "",
            "preview_url" : "",
            "section_duration" : 64000,
            "track_url" : "/some/url/to/an/mp3/file.mp3"
         },
         {},
         {}
      ]
    ]
}
```

**Description**

`meta`: List of composed track options. Each option is further a list containing an item per section. So if you have two sections in your track, each item will have two objects. Each of the objects will contain the following fields:

`instruments`: List of instruments that appear in the composed tracks

`track_url`: URL to the composed track for that section. This is in .mp3 format

`preview_url`: URL to the short preview of the composed track for that section. This is in .mp3 format

## Supported Options

You can use this API, to get the supported values for track parameters like genre, moods and tempo. In this API, you'll also get a list of combinations that may lead to errors. You can use pick the parameters and hardcode them into your application but it'd be recommended that your application fetches these parameters dynamically on launch.

**Endpoint**

`GET /api/v1/composition_params`

**Payload Example**

```json
{
   "genre": ["indian", "pop", "ambient", "indie", "rnb", "cinematic", "hiphop", "electronic"],
   "emotion": ["sad", "calm", "motivational", "happy", "scary", "cheerful", "angry", "triumphant", "relaxing", "depressing", "dreamy", "inspirational", "energetic", "joyful", "tense", "fearful"],
   "tempo": ["slow", "medium", "fast"],
   "blockedParams": [
      {
            "genre": "rnb",
            "moods": ["tense", "angry", "scary", "fearful", "sad", "inspirational", "depressing", "motivational", "triumphant"],
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
