"""
This module defines some datastructures and exceptions
"""
import re

class OverlappingWordStemException(Exception):
    pass

class InvalidWordException(Exception):
    pass

class LetterNode:
    """
    A letter node is a node in the letter tree.
    It has
     - a value of [A-Z]
     - a dictionary of children ([A-Z] --> LetterNode)
     - a reference to a parent (can be none)
     - a flag if a word ends at this node
    """
    
    def __init__(self, parent, value, is_word=False):
        """
        Sets inital values of attributes
        """ 
        self.value = value
        self.parent = parent
        self.children_dict = {}
        self.is_word = is_word

    def add_child(self, child):
        """
        Adds a child to the node
        """
        self.children_dict[child.value] = child

    def add_children(self, children):
        """
        Convenience method to add multiple children
        """
        for child in children:
            self.add_child(child)
            
    def has_child(self, child_letter):
        """
        Boolean if the node has the given child
        """
        return child_letter in self.children_dict

    def get_child(self, child_letter):
        """
        returns the child given by child_letter, or None
        """
        return self.children_dict.get(child_letter)
        
    def children(self):
        """
        returns an iterator over this nodes children
        """
        return self.children_dict.itervalues()

    def get_distance_from_death(self, n_players):
        """
        Distance from death is the maximum number of turns,
        in the worst case, that this node is from being forced to make a word
        """
        if self.is_word:
            return 0
        else:
            return (max([child.get_distance_from_death(n_players) for child in self.children()]) + 1) % n_players
        
    def __str__(self):
        return self.value + ":" + ','.join(self.children_dict.keys())
        

class LetterTree:
    """
    Class to contain a tree of letter nodes.
    maintains a root node, and provides convenience methods
    for working with the tree
    """

    def __init__(self, words=None):
        self.root = LetterNode(None, '', False)
        
        if words is not None:
            for word in words:
                self.add_word(word)
                
    @classmethod
    def from_file(cls, filename):
        """
        Opens up a file with one word per line
        [a-zA-Z]+
        
        and creates a word list from it
        """
        file_handle = open(filename, 'r')
        
        def line_generator():
            for line in file_handle:
                line = line.strip().upper()
                if not re.match(r'[A-Z]+$', line):
                    raise ValueError("Lines in file for from_file must be only letters")
                
                yield line
        
        return cls(line_generator())

    def add_word(self, word):
        """
        Adds the word to the letter tree
        It creates nodes as necessary.
        
        If, while attempting to add a word, it comes
        across a node that is marked as being a word,
        a OverlappingWordStemException will be raised
        (this should not happen with ghost)
        """
        active_node = self.root
        for letter in word[:-1]:
            if active_node.has_child(letter):
                next_node = active_node.get_child(letter)
                if next_node.is_word:
                    raise OverlappingWordStemException
            else:
                next_node = LetterNode(active_node, letter)
                active_node.add_child(next_node)
            
            active_node = next_node

        last_letter = word[-1]
        if active_node.has_child(last_letter):
            raise OverlappingWordStemException
        else:
            active_node.add_child(LetterNode(active_node, last_letter, is_word=True))

    def get_node(self, node_string):
        """
        Finds the node at the end of the path described by
        the string of letters [A-Z]* node_string
        """
        active_node = self.root
        for letter in node_string:
            if active_node.has_child(letter):
                active_node = active_node.get_child(letter)
            else:
                return None
        return active_node

    def get_words_below(self, node_string):
        """
        returns a list of strings (words) that are below the node described
        by the given string (or empty list if the node does not exist or has no words)
        """
        active_node = self.get_node(node_string)
        if active_node is None or active_node.is_word:
            return []
        
        #now active node contains the node below which we want words
        words = []
        # DFS - keep track of node_string so we can output the whole word
        search_frontier = [(active_node, node_string)]
        while search_frontier:
            node, prefix = search_frontier.pop()
            for child in search_frontier.children():
                new_prefix = prefix + child.value
                if child.is_word:
                    words.append(new_prefix)
                else:
                    search_frontier.append((child, new_prefix))
        return words

    def check_distance_from_death(self, word_string, n_players):
        """
        Checks the distance from death of the given word, in a game
        with n_players.
        
        Will raise InvalidWordException if the word cannot be found
        """
        queried_node = self.get_node(word_string)
        if queried_node is not None:
            return queried_node.get_distance_from_death(n_players)
        else:
            raise InvalidWordException

    def __str__(self):
        """
        A representation of the tree
        """
        # start off with all the top level ones.
        # ['Z', 'Y', 'X', ... , 'C', 'B', 'A']
        # the zero is for the depth 0
        # the value is to start off the string
        print_frontier = [(node, 0, node.value) for node in reversed(sorted(self.root.children()))]
        
        lines = [] #the differente lines in the printout
        while print_frontier:
            node, depth, prefix = print_frontier.pop()
            line_value = ' ' * depth + node.value
            if node.is_word:
                line_value += ' | (%s)' % prefix
            lines.append(line_value)
            print_frontier.extend([(node, depth + 1, prefix + node.value) for node in reversed(sorted(node.children()))])
        return '\n'.join(lines)    
        
def do_stuff():
    test_words = [
        "CAT",
        "CAB",
        "DOG",
        "DONUT",
        "ABOUT",
        "HAT",
        "HELLO",
        "BOAT",
        "BAT",    
    ]
    
    lt = LetterTree(test_words)
    print lt
    
    
if __name__ == "__main__":
    do_stuff()
    
    
    
    
    
    
    
    