from .utils import drop_nones

class Allele:
    def __init__(self,
        name,
        frequency = None,
        count = None,
        repeat_units = None,
        repeating_region_bracketed = None,
        flank_features = None,
        assembly = None,
        flank5_seq = None,
        repeating_region_seq = None,
        flank3_seq = None,
        **user):

        self.name = name
        self.frequency = frequency
        self.count = count
        self.repeat_units = repeat_units
        self.repeating_region_bracketed = repeating_region_bracketed
        self.flank_features = flank_features
        self.assembly = assembly
        self.flank5_seq = flank5_seq
        self.repeating_region_seq = repeating_region_seq
        self.flank3_seq = flank3_seq
        if len(user) > 0:
            self.user = user
        else:
            self.user = None

    def to_leapdna(self):
        return drop_nones(self.__dict__)

    # pretend to be a dictionary
    def __getitem__(self, index):
        return self.__dict__[index]

    def __setitem__(self, index, value):
        self.__dict__[index] = value

def repeat_to_seq(bracketed):
    seq = ''
    in_braket = False
    in_nrepeat = False
    repeat = ''
    nrepeat = 0
    for char in bracketed:
        if char.isspace(): continue
        
        if in_nrepeat:
            if char.isdigit():
                nrepeat = 10 * nrepeat + int(char)
            else:
                seq += repeat * nrepeat
                in_nrepeat = False
                repeat = ''
    
        if char in ('[', '('):
            in_braket = True
            repeat = ''
            continue
        elif char in (']', ')'):
            in_braket = False
            in_nrepeat = True
            nrepeat = 0
            continue

        if in_braket:
            repeat += char
        elif not in_nrepeat:
            seq += char

    # return accumulated sequence plus a possible last repeat
    return seq + repeat * nrepeat
            