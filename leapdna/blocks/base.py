import json
from typing import Any, Dict, IO, Optional


class Base:
    block_type = 'base'
    id: Optional[str] = None

    user: Any = None

    def __init__(self,
                 block_type: str = 'base',
                 id: str = None,
                 user=None,
                 leapdna=None,
                 *args,
                 **kwargs):
        if leapdna is not None:
            # direct arguments take precedence over those in leapdna
            block_type = block_type or leapdna.get('block_type', None)
            id = id or leapdna.get('id', None)

        self.id = id
        self.block_type = block_type

        if user is None:
            self.user = {}
        else:
            self.user = user

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
            'leapdna': {
                'block_type': self.block_type,
                'id': self.id
            },
            'user': self.user
        }