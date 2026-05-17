# TinyRouter

## Stack
- Framework: Django 5
- Database: SQLite
- Why I made this decision: Django because python is something I'm generally more comfortable in. It's my preferred language to do takehome assignments with. SQLite because of the one command setup ease and time budget. Is also easy to swap later on


## Setup
`make setup` should satisfy one-command setup requirement
```bash
make setup
make run
```

`make test` if you'd like to run the three tests 

Server is set to run @ `http://localhost:8000`

## curl

POST /links

Create a tracked shortlink:
```bash
curl -s -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{
    "destination_url": "https://example.com/landing",
    "campaign_code": "spring2026",
    "creator_handle": "@somebody"
  }'
```

Response example:
```json
{ "slug": "...", "short_url": "http://localhost:8000/r/..." }
```

GET /r/:slug

Redirect to the destination URL
```bash
# replace <SLUG> with value from POST /links
curl -sI "http://localhost:8000/r/<SLUG>?utm_source=twitter&utm_content=post1" \
  -H "User-Agent: Mozilla/5.0"
```

Should get `302` and `location` header. Bot user agents still get a 302 but don't create click row.

GET /links/:slug/stats

Click aggregates for a slug. Excludes all bot traffic
```bash
curl -s "http://localhost:8000/links/SLUG/stats"
```

Expected Response:
```json
{
  "slug": "...",
  "total_clicks": 0,
  "unique_ips": 0,
  "by_country": {}
}
```

## Async enrichment
ip-api.com lookups run on a background thread after the redirect returns, so the 302 never blocks on HTTP. I prefered to do it this way since it was easy, simple, and fast. Some known tradeoffs I'm include no durability, no backpressure, multiworker weirdness, and no retries. These are things I'd change if I was given more time. In regards to scale, I'd include multiple web workers for durability and decouple the enrichment from redirect to handle high click volume.


## How I used Cursor
I used cursor to entirely generate a plan in which I could do things using parallel agents to be as efficient as possible. This plan was outputted to `PLAN.md`. Made it easy for me to run through all parts of this project while fully understanding what each individual agent was accomplishing. In a perfect world, I would have likely also used subagents but I wanted to purposely throttle myself in order to really understand what I was doing and the code changes I was making. I couldn't find any issues with what Cursor did due to the way I prompted it. It did initially want to write everything in rails/postgres but I chose to use django/sqlite instead due to the reasons above. Usually I look for abnormalities in syntax/readability when I'm heavily using AI.

## What I'd do next with another hour
This is less about what I'd do with another hour since I didn't even use the entire alotted time, but more about what I'd change in regard to the project. The previously mentioned async enrichment is something I'd (obviously) change, but also would write WAY more tests. Testing is so easy using AI tools like cursor and claude and is incredibly good at hitting code coverage metrics. I'd also do something in regards to creating a github actions workflow to run all of these tests and deploying to a public endpoint for you to test. 

## Time spent
40-ish minutes on project
30-ish minutes on readme

