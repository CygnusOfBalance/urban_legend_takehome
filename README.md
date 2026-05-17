# TinyRouter

<!-- Fill in your own words below. Bullets and fragments are fine. -->

## Stack

- **Framework:** Django 5 + Django REST Framework
- **Database:** SQLite
- **Why these choices:** <!-- e.g. speed of setup, reviewer friction, what you'd swap in prod -->

## Setup

Requires Python 3.10+.

```bash
make setup
make run
```

Server runs at `http://localhost:8000`.

Optional: copy `.env.example` to `.env` and tweak `APP_BASE_URL` / `SECRET_KEY`.

```bash
make test    # run the 3 integration tests
```

## Endpoints

### `POST /links`

Create a tracked short link.

```bash
curl -s -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{
    "destination_url": "https://example.com/landing",
    "campaign_code": "spring2026",
    "creator_handle": "@somebody"
  }'
```

Response shape:

```json
{ "slug": "...", "short_url": "http://localhost:8000/r/..." }
```

### `GET /r/:slug`

Redirect to the destination URL. Incoming query params (e.g. UTMs) are appended to the destination.

```bash
# replace SLUG with value from POST /links
curl -sI "http://localhost:8000/r/SLUG?utm_source=twitter&utm_content=post1" \
  -H "User-Agent: Mozilla/5.0"
```

Expect `302` and a `Location` header. Bot user-agents still get `302` but do not create a click row.

### `GET /links/:slug/stats`

Click aggregates for a slug (excludes bot traffic).

```bash
curl -s "http://localhost:8000/links/SLUG/stats"
```

Response shape:

```json
{
  "slug": "...",
  "total_clicks": 0,
  "unique_ips": 0,
  "by_country": {}
}
```

## Async enrichment

ip-api.com lookups run on a background thread after the redirect returns, so the 302 never blocks on HTTP.

<!-- Your call: why threading vs Celery/ActiveJob/etc, and what you'd change at scale -->

## How I used Cursor

<!-- 3–5 specific bullets. Examples of prompts to answer:
  - What did Cursor do well?
  - What did it get wrong?
  - What did you override manually?
  - One judgment call where you ignored its suggestion
-->

-

-

-

## What I'd do next with another hour

<!-- honest list if you ran out of time; stretch ideas from TASK.md:
  - IP dedup window (5s)
  - fraud score on hosting ASN
  - HTML stats page at GET /links/:slug
-->

-

-

## Time spent

<!-- actual wall-clock time for the take-home -->

~ ___ hours
