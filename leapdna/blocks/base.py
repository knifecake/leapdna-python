from leapdna.errors import LeapdnaError
from typing import Any, Dict, Optional


class Base:
    block_type = 'base'
    id: Optional[str] = None

    user: Dict[str, Any]

    def __init__(self,
                 id: Optional[str] = None,
                 user: Optional[Dict[str, Any]] = None,
                 *args,
                 **kwargs):
        self.id = id

        if user:
            self.user = user
        else:
            self.user = {}

    def __str__(self):
        return f'<leapdna block {self.block_type}: {self.id}>'

    def __repr__(self) -> str:
        return str(self)

    def resolve_deps_from_blob(self, blob):
        pass

    def block_deps(self):
        """Returns a flat dictionary of (block id, block) pairs containing every block dependency
        of this block or of any of its dependencies."""
        return {}

    def asdict(self, without_deps=False):
        return {
            'block_type': self.block_type,
            'id': self.id,
            'user': self.user
        }

    def __eq__(self, o: object) -> bool:
        if isinstance(o, type(self)):
            return o.id == self.id

        return False

    def __hash__(self) -> int:
        return hash(self.id)