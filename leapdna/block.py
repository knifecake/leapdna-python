class LeapdnaBlock():

    __leapdna_version__ = 1

    def __init__(self, version = None, type = 'object', id = None, leapdna = None, **user):
        self.version = version
        self.type = type
        self.id = id
        self.leapdna = leapdna
        self.dprops = None
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
