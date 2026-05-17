from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def append_query_params(destination_url: str, extra_params: dict[str, str]) -> str:
    """Append incoming query params onto the destination URL."""
    if not extra_params:
        return destination_url

    parsed = urlparse(destination_url)
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    pairs.extend((key, value) for key, value in extra_params.items())
    return urlunparse(parsed._replace(query=urlencode(pairs)))
