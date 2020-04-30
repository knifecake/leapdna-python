class LeapdnaBlock():

    __block_type__ = None
    __leapdna_version__ = 1

    def __init__(self, version = None, type = None, id = None, leapdna = None, **user):
        self.dprops = None
        if type is not None:
            if self.__block_type__ is not None:
                assert type == self.__block_type__, f"type does not match {self.__block_type__}"
            self.type = type
        else:
            self.type = self.__block_type__

        self.version = version
        self.id = id
        self.leapdna = leapdna
        if len(user) > 0:
            self.user = user
        else:
            self.user = None

    def to_leapdna(self, top_level = False):
        ret = self.drop_nones(self.__dict__)
        if top_level:
            ret['version'] = self.__leapdna_version__
        if self.dprops is not None:
            ret.update(self.drop_nones(self.dprops))

        return ret

    @staticmethod
    def drop_nones(dictionary):
        return { k: v for k, v in dictionary.items() if k[0] != '_' and v is not None }
