class GenomeData:
    """
    An instance of the GenomeData object stores 
    the id of a genome, its sequence, and the ngrams
    of the sequence. 
    Its primary methods are:
    add_sequence(self, sequence)- Adds to the sequence 
    of the genome
    get_sequence(self)- Returns the sequence of the genome
    get_id(self)- Returns the id of the genome. 
    """

    def __init__(self, id):
        self._id = id
        self._sequence = ''
        self._ngrams = set()
        
    def add_sequence(self, sequence):
        """
        Adds the parameter 'sequence' to the 
        sequence of the genome. 
        Parameters: sequence(str)- A string that is part 
        of a genome's sequence. 
        Returns: none
        """
        self._sequence = sequence

    def get_sequence(self):
        return self._sequence
    
    def get_id(self):
        return self._id
    

    def __str__(self):
        return 'ID is:' + self._id + ' ' 