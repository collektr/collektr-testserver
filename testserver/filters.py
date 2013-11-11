
def uuid_filter(config):
    """
    Matches a valid UUID.
    """
    regexp = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    def to_python(match):
        return match
    def to_url(uri):
        return uri
    return regexp, to_python, to_url

