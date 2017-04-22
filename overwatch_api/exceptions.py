class RatelimitError(ConnectionError):
    """Raised when an api call is ratelimited."""
    pass


class ProfileNotFoundError(ValueError):
    """Raised when a battletag isn't found with specified region and platform"""
    pass
