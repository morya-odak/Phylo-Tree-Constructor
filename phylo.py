"""
File: phylo.py
Author: Morya Odak
Purpose: Construct phylogenetic trees starting from 
the genome sequences of a set of organisms. This is done 
by extracting information from a data file, reading its 
information, finding the n-grams, and creating the data
structure, and printing it as an output. 
Course: CSC 120 SP23 001-2
"""

from genome import *
from tree import *

def main():
    organism_list, n = read_file()
    similarity_data = create_similarity_data(organism_list, n)
    tree_list = create_tree_list(organism_list)
    tree = create_tree(tree_list, similarity_data)
    print(str(tree))

def read_file():
    """
    Opens a file specified by the user and iterates through the
    file to get the id of each genome and its sequence. These 
    are stored as objects and appended to a list. 
    Parameters: none
    Returns: organism_list(list)- A list containing GenomeData objects
    which store information about organisms and their sequences and id's.
    n(int)- The number given by the user that specifies the 
    size of each n-gram. 
    """
    file_name = input('FASTA file: ')
    n = int(input('n-gram size: '))
    file = open(file_name, 'r')
    organism_list = []
    sequence = ''
    prev_line = None
    for line in file:
        line = line.strip()
        if line == '' and prev_line != '':
            g.add_sequence(sequence)
            organism_list.append(g)
            sequence = ''
        elif line != '' and line[0] == '>':
            line = line.split()
            genome_id = line[0][1:]
            g = GenomeData(genome_id)
        else:
            sequence+= line
        prev_line = line

    for g in organism_list:
        [g._ngrams.add(g._sequence[i:i+n]) for i in range(len(g._sequence)-n)]

    return organism_list, n

def create_similarity_data(organism_list, n):
    """
    Creates a dictionary that stores every combination of 
    genomes in the data file paired as keys and the similarity
    value of every respective pair. 
    Parameters: organism_list(list)- A list containing GenomeData objects
    which store information about organisms and their sequences and id's.
    n(int)- The number given by the user that specifies the 
    size of each n-gram. 
    Returns: similarity_data(dictionary)- A dictionary storing pairs of 
    genomes as tuples and their similarity values. 
    """
    similarity_data = {}
    similarity_data_dup = {}
    for genome1 in organism_list:
        for genome2 in organism_list:
            key = tuple((genome1._id, genome2._id))
            if genome1._id != genome2._id and key not in similarity_data:
                g1_set = genome1._ngrams
                g2_set = genome2._ngrams
                [g1_set.add(genome1._sequence[i:i+n]) \
                 for i in range(len(genome1._sequence)-n+1)]
                [g2_set.add(genome2._sequence[i:i+n]) \
                 for i in range(len(genome2._sequence)-n+1)]
                num = len(g1_set.intersection(g2_set))
                den = len(g1_set.union(g2_set))
                similarity = float(num)/float(den)
                similarity_data[key] = similarity
                similarity_data_dup[key] = similarity
    return similarity_data

def create_tree_list(organism_list):
    """
    Iterataes through each GenomeData object in the organism 
    list and creates a new list that stores Tree objects with 
    each tree storing the id of each genome and the genome object
    that it contains.
    Paramters: organism_list(list)- A list containing GenomeData objects
    which store information about organisms and their sequences and id's.
    Returns: tree_list(list)- A list of tree objects that correspond to
    each individual genome. 
    """
    tree_list = []
    for genome in organism_list:
        t = Tree(genome._id)
        t._genome_list.append(genome)
        tree_list.append(t)
    return tree_list

def create_tree(tree_list, similarity_data):
    """
    Continuously iterates through the list of trees and combines certain 
    trees based on the highest similarity values until there is just one, 
    large tree object. 
    Parameters: tree_list(list)- A list of tree objects that correspond to
    each individual genome. 
    similarity_data(dictionary)- A dictionary storing pairs of 
    genomes as tuples and their similarity values. 
    Returns: tree(Tree)- A single tree object with all the genomes placed
    in spots that correspond to their similarity value.
    """
    while len(tree_list) != 1:
        max_similarity = None
        trees_to_be_combined = None
        for tree_one in tree_list:
            tree_one_genomes = tree_one._genome_list
            for tree_two in tree_list:
                tree_two_genomes = tree_two._genome_list
                if tree_one != tree_two:
                    curr_similarity = \
                    find_similarity(tree_one_genomes, \
                                    tree_two_genomes, \
                                    similarity_data)
                    if max_similarity == None or \
                       curr_similarity > max_similarity:
                        max_similarity = curr_similarity
                        trees_to_be_combined = [tree_one, tree_two]
        t = concat_trees(trees_to_be_combined[0], trees_to_be_combined[1])
        tree_list.remove(trees_to_be_combined[0])
        tree_list.remove(trees_to_be_combined[1])
        tree_list.append(t)
    tree = tree_list[0]
    return tree

def find_similarity(list_one, list_two, similarity_data):
    """
    Iterates through 2 lists that contain the GenomeData objects stored in a 
    tree and finds the highest similarity value between the two trees. 
    Parameters: list_one(list)- A list containing all the genomedata objects
    stored within a tree object. 
    list_two(list)- A list containing all the genomedata objects
    stored within a tree object. 
    similarity_data(dictionary)- A dictionary storing pairs of 
    genomes as tuples and their similarity values. 
    Returns:
    max_similarity(int)- The highest similarity value between all genomes 
    within two trees. 
    """
    max_similarity = None
    for genome_one in list_one:
        for genome_two in list_two:
                if genome_one != genome_two:
                    key_tuple = tuple((genome_one._id, genome_two._id))
                    curr_similarity = similarity_data[key_tuple]
                    if max_similarity == None or \
                       curr_similarity > max_similarity:
                        max_similarity = curr_similarity
    return max_similarity
    
def concat_trees(tree_one, tree_two):
    """
    Takes two trees and merges them into one, using the 
    string function to determine which side each genome goes on.
    Parameters: tree_one(Tree)- A tree object storing genomes
    tree_two(Tree)- A tree object storing genomes
    Returns: t(Tree)- A t that stores tree one and tree two combined. 
    """
    t = Tree(None)
    t._genome_list += tree_one._genome_list
    t._genome_list += tree_two._genome_list
    if str(tree_one) < str(tree_two):
        t._left, t._right = tree_one, tree_two
    else:
        t._left, t._right = tree_two, tree_one
    return t


main()