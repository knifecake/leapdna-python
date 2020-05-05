class LeapdnaBlock():
    __block_type__ = 'block'
    def __init__(self, id = None, version = None, type = None, leapdna = None, **user):
        self.dprops = {}
        if type is not None:
            assert type == self.__block_type__, f"Leapdna block is not a {self.__block_type__}"
            self.type = type
        else:
            self.type = self.__block_type__

        self.id = id
        self.version = version
        self.leapdna = leapdna
        if len(user) > 0:
            self.user = user
        else:
            self.user = None

    def to_leapdna(self, top_level = False):
        ret = self.drop_nones(self.__dict__)
        del ret['dprops']

        if top_level:
            if self.version is not None: ret['version'] = self.version

        ret.update(self.drop_nones(self.dprops))

        return ret

    @staticmethod
    def drop_nones(dictionary):
        return { k: v for k, v in dictionary.items() if k[0] != '_' and v is not None }
