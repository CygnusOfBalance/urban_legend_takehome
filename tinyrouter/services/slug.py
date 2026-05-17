import secrets
import string

from tinyrouter.models import Link

SLUG_ALPHABET = string.ascii_letters + string.digits + "_-"
SLUG_LENGTH = 8
MAX_ATTEMPTS = 10


class SlugGenerationError(Exception):
    pass


def generate_unique_slug() -> str:
    for _ in range(MAX_ATTEMPTS):
        slug = "".join(secrets.choice(SLUG_ALPHABET) for _ in range(SLUG_LENGTH))
        if not Link.objects.filter(slug=slug).exists():
            return slug
    raise SlugGenerationError("Could not generate a unique slug")
