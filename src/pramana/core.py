"""Pramana OGM base classes.

Provides the object-graph mapping foundation for the Pramana knowledge graph.
Mirrors the C# PramanaLib OGM layer.
"""

import uuid
from abc import ABC, abstractmethod


class PramanaException(Exception):
    """Raised when a Pramana OGM constraint is violated (e.g. ID reassignment)."""
    pass


class IPramanaLinkable(ABC):
    """Interface for all objects that participate in the Pramana knowledge graph."""

    @property
    @abstractmethod
    def pramana_guid(self) -> uuid.UUID:
        """UUID (v4 or v5) identifying this entity."""
        ...

    @property
    @abstractmethod
    def pramana_id(self) -> str | None:
        """Pramana identifier string (e.g. 'pra:num:3,1,2,1'), or None for regular objects."""
        ...

    @property
    def pramana_hash_url(self) -> str:
        """Pramana entity URL using the hashed UUID."""
        return f"https://pramana.dev/entity/{self.pramana_guid}"

    @property
    def pramana_url(self) -> str:
        """Pramana entity URL. Uses pramana_id if available, otherwise pramana_hash_url."""
        pid = self.pramana_id
        if pid is not None:
            return f"https://pramana.dev/entity/{pid}"
        return self.pramana_hash_url


class PramanaInterface(ABC):
    """Mixin for objects that declare ontology roles."""

    @abstractmethod
    def get_roles(self) -> list['PramanaRole']:
        """Return the PramanaRole instances this object fulfils."""
        ...


class PramanaObject(IPramanaLinkable, PramanaInterface):
    """Base class for all Pramana-mapped objects.

    IDs follow "friction by design": new objects start with no ID and only
    receive a UUID when generate_id() is explicitly called. Once assigned,
    IDs are immutable.
    """

    ROOT_ID = uuid.UUID("10000000-0000-4000-8000-000000000001")
    CLASS_ID = ROOT_ID
    CLASS_URL = f"https://pramana.dev/entity/{CLASS_ID}"

    def __init__(self, id: uuid.UUID | None = None):
        if id is not None:
            self._pramana_guid = id
        else:
            self._pramana_guid = uuid.UUID(int=0)

    @property
    def pramana_guid(self) -> uuid.UUID:
        return self._pramana_guid

    @property
    def pramana_id(self) -> str | None:
        return None

    def generate_id(self) -> uuid.UUID:
        """Assign a UUID v4 to this object. Raises PramanaException if already assigned."""
        if self._pramana_guid != uuid.UUID(int=0):
            raise PramanaException("Cannot reassign an ID that has already been generated.")
        self._pramana_guid = uuid.uuid4()
        return self._pramana_guid

    def get_roles(self) -> list['PramanaRole']:
        return []


class PramanaRole(PramanaObject):
    """Represents an ontology role/interface in the Pramana knowledge graph.

    Supports hierarchy via instance_of, subclass_of, parent_roles, and child_roles.
    """

    def __init__(self, label: str, id: uuid.UUID | None = None):
        super().__init__(id)
        self.label = label
        self.instance_of: PramanaRole | None = None
        self.subclass_of: PramanaRole | None = None
        self.parent_roles: list[PramanaRole] = []
        self.child_roles: list[PramanaRole] = []

    def get_roles(self) -> list['PramanaRole']:
        return [self]


class PramanaParticular(PramanaObject):
    """A concrete particular in the Pramana knowledge graph."""

    CLASS_ID = uuid.UUID("13000000-0000-4000-8000-000000000004")
    CLASS_URL = f"https://pramana.dev/entity/{CLASS_ID}"

    def __init__(self, id: uuid.UUID | None = None):
        super().__init__(id)
