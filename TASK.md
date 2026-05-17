# TinyRouter — Backend Take-Home

## Build this with Cursor

We use [Cursor](https://cursor.com) every day and want to see how you work in it. **Use Cursor as your editor for this exercise** — agent mode, tab completions, inline edits, whatever your normal workflow looks like. We're evaluating both the code and your judgment about when to lean on the AI vs. override it. The "How I used Cursor" section in the README (described below) is where you tell us about that.

One exception: see the "README ground rule" further down. Code = Cursor encouraged. README prose = write it yourself.

## Context

At Urban Legend, creators post tracked links to their audiences. When someone clicks, our service redirects them to the campaign's destination, records the click, and enriches it with metadata so we can later compute attribution, payout, and detect fraud.

Build a small slice of this.

## Stack

Rails 7+ **or** Django 4+/DRF — your choice. Postgres or SQLite — also your choice. Whichever you pick, justify it briefly in the README.

## Time budget

**2 hours hard cap.** If you run out, ship what you have and note in the README what you'd do next. Padding past the cap to "polish" is worse signal than an honest cutoff.

## Required endpoints

### `POST /links`

- Body: `{ "destination_url": "...", "campaign_code": "spring2026", "creator_handle": "@somebody" }`
- Returns: `{ "slug": "abc123", "short_url": "http://localhost:PORT/r/abc123" }`
- Slug must be URL-safe and stable.

### `GET /r/:slug?utm_source=...&utm_content=...`

- 302 redirect to the link's `destination_url` (preserve UTM params on the redirect target).
- Record a `Click` row: `slug`, `timestamp`, `ip_address`, `user_agent`, raw query params, plus the enriched fields from the IP integration below.
- Skip recording (but still 302) when the User-Agent matches an obvious crawler — see "Bot filter" below.

### `GET /links/:slug/stats`

- Returns: `{ "slug", "total_clicks", "unique_ips", "by_country": {"US": 42, "CA": 7, ...} }`
- Excludes filtered bot hits.

## Free API integration (required)

Enrich each recorded click with **country, region, and ASN/ISP** using [ip-api.com](https://ip-api.com/) — fully free, no signup, no API key, 45 req/min per source IP. Store the enriched fields on the `Click` row.

If ip-api.com is unreachable, the redirect must still succeed and the click must still be recorded (with enrichment fields nullable). **The redirect path must not block on this call** — use a background job, a thread, `enqueue_after_response`, whatever fits your stack. Your choice; explain it briefly in the README.

## Bot filter (required)

Skip recording when `User-Agent` (case-insensitive) contains any of:

```
facebookexternalhit, twitterbot, slackbot, discordbot, googlebot,
python-requests, curl/, wget/
```

Empty UA also counts as a bot.

## Tests (required, keep it small)

At minimum:

1. Happy-path redirect records a click.
2. Bot UA hits 302 but does not record a click.
3. Stats endpoint returns correct counts.

RSpec, Minitest, or Django TestCase — your call. **Do not write more than ~3 tests.** This is not a TDD exercise.

## README must include

- One-command setup after `bundle install` / `pip install -r requirements.txt`.
- `curl` examples for each endpoint.
- A short "**How I used Cursor**" section: 3-5 specific bullets — what Cursor did well, what it got wrong, what you manually overrode, and one judgment call where you chose not to take its suggestion.
- "What I'd do next with another hour" section.

## README ground rule (read this carefully)

**Write the README yourself. Do not have Cursor (or any LLM) generate the prose for you.**

Use Cursor freely for the code; the README is where we want to hear *your* voice and judgment. Bullet points, fragments, typos — all fine. Polished, hedge-y, "as a backend engineer, I leveraged…" prose is exactly what we don't want. If we can't tell whether a human or an LLM wrote it, that's a strong negative signal.

## Stretch (only if you have time, do not exceed the 2-hour cap)

- IP-based dedup window (same IP + slug within 5s = don't double-count).
- Tiny fraud score: flag clicks where the enriched ASN/ISP looks like a hosting provider (e.g. AWS, OVH, DigitalOcean).
- Server-rendered HTML stats page at `GET /links/:slug` for human consumption.

## Don't waste time on

- Auth / users / sessions.
- A frontend (the optional stats page is server-rendered, not React).
- Docker, unless your stack genuinely needs it for someone to run the project.
- More than ~3 tests.

## Commits

Commit as you go — we want to see the shape of your work, not one giant "initial commit". Aim for ~5+ logical commits (e.g. scaffold, model + migration, redirect endpoint, ip-api enrichment, bot filter, tests). Don't squash. Messy-but-honest history beats a single polished commit.

## Submission

Push to a GitHub repo with:

- The code.
- Your hand-written README.
- A short note on how long it actually took you.

Public repo or private repo is fine — if private, share it with **@interestinall** on GitHub.