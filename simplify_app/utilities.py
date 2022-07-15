import uuid

from simplify_app.models import SimpleUrl


def create_simple_url(original_url, user):
    url = SimpleUrl.objects.filter(original_url=original_url)
    if url:
        return url[0].simple_url_id

    simple_url_id = str(uuid.uuid4())[:5]
    simple_url = SimpleUrl(original_url=original_url, user=user,
                           simple_url_id=simple_url_id)
    simple_url.save()
    return simple_url_id
