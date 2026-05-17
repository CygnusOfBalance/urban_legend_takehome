BOT_SUBSTRINGS = [
    "facebookexternalhit",
    "twitterbot",
    "slackbot",
    "discordbot",
    "googlebot",
    "python-requests",
    "curl/",
    "wget/",
]


def is_bot(user_agent: str | None) -> bool:
    if not user_agent or not user_agent.strip():
        return True
    ua = user_agent.lower()
    return any(s in ua for s in BOT_SUBSTRINGS)
