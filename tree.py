class Tree:
    """
    An instance of a Tree Object stores the id of a genome or the 
    genomes stored within a certain tree. Its primary method is 
    is_leaf(self), which checks whether an instance of a Tree is
    a leaf node or not. 
    """
    def __init__(self, id):
        self._id = id
        self._left = None
        self._right = None
        self._genome_list = []

    def is_leaf(self):
        """
        Checks if the two children of the tree are empty or not. Returns 
        true if they are, false otherwis. 
        """
        return self._left == None and self._right == None

    def __str__(self):
        if self.is_leaf():
            return self._id
        else:
            return "({}, {})".format(str(self._left), str(self._right))