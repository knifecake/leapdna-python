from .block import LeapdnaBlock

class Sequence(LeapdnaBlock):
    __block_type__ = 'sequence'

    def __init__(self,
                 name = None,
                 refseq_name = None,
                 refseq_start = None,
                 refseq_end = None,
                 repeat_units = [],
                 repeating_seq = None,
                 flank5_seq = None,
                 flank3_seq = None,
                 repeating_bracketed = None,
                 flank5_bracketed = None,
                 flank3_bracketed = None,
                 **rest):

        super().__init__(**rest)

        self._name = name
        self.refseq_name = refseq_name
        self.refseq_start = refseq_start
        self.refseq_end = refseq_end
        self.repeat_units = repeat_units

        self.dprops = {
            'repeating_seq': repeating_seq,
            'flank5_seq': flank5_seq,
            'flank3_seq': flank3_seq,
            'repeating_bracketed': repeating_bracketed,
            'flank5_bracketed': flank5_bracketed,
            'flank3_bracketed': flank3_bracketed
        }

    @property
    def name(self):
        if self._name is not None:
            return self._name

        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def repeating_seq(self):
        return self._seq_or_bracketed('repeating')

    @repeating_seq.setter
    def repeating_seq(self, value):
        self.dprops['repeating_seq'] = value
        
    @property
    def flank5_seq(self):
        return self._seq_or_bracketed('flank5')

    @flank5_seq.setter
    def flank5_seq(self, value):
        self.dprops['flank5_seq'] = value
        
    @property
    def flank3_seq(self):
        return self._seq_or_bracketed('flank3')

    @flank3_seq.setter
    def flank3_seq(self, value):
        self.dprops['flank3_seq'] = value
        
    @property
    def repeating_region_bracketed(self):
        # TODO: calculate bracketed if not present
        return self.dprops['repeating_region_bracketed']

    @repeating_region_bracketed.setter
    def repeating_region_bracketed(self, value):
        self.dprops['repeating_region_bracketed'] = value
        
    @property
    def flank5_bracketed(self):
        # TODO: calculate bracketed if not present
        return self.dprops['flank5_bracketed']

    @repeating_region_bracketed.setter
    def flank5_bracketed(self, value):
        self.dprops['flank5_bracketed'] = value

    @property
    def flank3_bracketed(self):
        # TODO: calculate bracketed if not present
        return self.dprops['flank3_bracketed']

    @repeating_region_bracketed.setter
    def flank3_bracketed(self, value):
        self.dprops['flank3_bracketed'] = value
        
    def _seq_or_bracketed(self, index):
        '''Returns a sequence from the derived property dictionary. If the
        sequence is not found it attempts to calculate it from its bracketed
        counterpart. Otherwise it returns None.'''
        if self.dprops[f'{index}_seq'] is None and self.dprops[f'{index}_bracketed'] is not None:
            self.dprops[f'{index}_seq'] = self.bracketed_to_seq(self.dprops[f'{index}_bracketed'])

        return self.dprops[f'{index}_seq']

    @staticmethod
    def bracketed_to_seq(bracketed):
        '''Converts a sequence from bracketed format to explicit (FASTA) format.'''
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
