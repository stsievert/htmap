class HTMapException(Exception):
    """Base exception for all ``htmap`` exceptions."""
    pass


class MissingSetting(HTMapException):
    """The requested setting has not been set."""
    pass


class OutputNotFound(HTMapException):
    """The requested output file does not exist."""
    pass


class NoResultYet(HTMapException):
    """The :class:`htmap.MapBuilder` does not have an associated :class:`htmap.MapResult` yet."""
    pass


class TimeoutError(TimeoutError, HTMapException):
    """An operation has timed out because it took too long."""
    pass


class MapIdAlreadyExists(HTMapException):
    """The requested ``map_id`` already exists (recover the :class:`MapResult`, then either use or delete it)."""
    pass


class InvalidMapId(HTMapException):
    """The ``map_id`` has an invalid character in it."""
    pass


class MapIdNotFound(HTMapException):
    """The requested ``map_id`` does not exist."""
    pass


class EmptyMap(HTMapException):
    """The map contains no inputs."""
    pass


class ReservedOptionKeyword(HTMapException):
    pass


class MisalignedInputData(HTMapException):
    pass


class CannotRenameMap(HTMapException):
    pass
