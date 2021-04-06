from .blocks import BLOCKTYPE_MAP, Base
from .errors import LeapdnaError


class LeapdnaBlob(dict):
    id_counter: int

    def __init__(self, data=None):
        if data:
            if 'block_type' not in data or data['block_type'] != 'blob':
                raise LeapdnaError(
                    'data is not a leapdna blob. Try loading with LeapdnaBlob.parse_block instead.'
                )

            ids = set(data.keys()) - {'block_type', 'id'}
            self.update(
                {id: LeapdnaBlob.parse_block(data[id], id)
                 for id in ids})
            self.resolve_all_deps()

        self.id_counter = 1

    @staticmethod
    def parse_block(data, id=None) -> Base:
        if not ('block_type' in data):
            raise LeapdnaError('"block_type" not specified in block')
        if id:
            data['id'] = id
        try:
            block = BLOCKTYPE_MAP[data['block_type']]
            return block(**data)
        except KeyError:
            raise LeapdnaError(f'unkwon block_type "{data["block_type"]}"')

    def resolve_deps_of_type(self, type: str):
        for key in self:
            if self[key].block_type == type:
                self[key].resolve_deps_from_blob(self)

    def resolve_all_deps(self):
        self.resolve_deps_of_type('locus')
        self.resolve_deps_of_type('allele')
        self.resolve_deps_of_type('observation')
        self.resolve_deps_of_type('study')

    def generate_id(self, block: Base) -> str:
        if block.id is None or (block.id in self):
            self.id_counter += 1
            block.id = f'g.{self.id_counter}'

        return block.id

    def append(self, block: Base):
        if not isinstance(block, Base):
            raise LeapdnaError('Given object is not a leapdna block')

        if not block.id:
            block.id = self.generate_id(block)

        new_blocks = {block.id: block}
        new_blocks.update(block.block_deps())

        invalid_ids = {
            id
            for id in new_blocks if id in self and self[id] != new_blocks[id]
        }
        if len(invalid_ids) > 0:
            raise LeapdnaError(
                'Invalid ids do not match already existing blocks: ' +
                ', '.join(invalid_ids))

        self.update(new_blocks)  # type: ignore

    def asdict(self):
        ret = {id: block.asdict() for id, block in self.items()}
        ret['block_type'] = 'blob'
        return ret
