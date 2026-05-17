HOSTING_MARKERS = (
    "amazon",
    "aws",
    "google cloud",
    "gcp",
    "microsoft azure",
    "azure",
    "digitalocean",
    "ovh",
    "hetzner",
    "linode",
    "vultr",
    "rackspace",
    "oracle cloud",
)


def compute_fraud_score(asn: str | None, isp: str | None) -> float:
    haystack = f"{asn or ''} {isp or ''}".lower()
    if any(marker in haystack for marker in HOSTING_MARKERS):
        return 1.0
    return 0.0
