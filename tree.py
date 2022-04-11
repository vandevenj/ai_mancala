
import copy

class Tree:
    """
    Data structure to hold the game decision tree,
    with each node holding its game state (model), 
    its next possible states resulting from actions (children),
    and the best move from the node's state.
    """

    def __init__(self, model):
        self.model = model
        self.children = []
        self.best_move = -1

    def get_children(self):
        """
        Returns a copy of the children from this game tree node.
        """
        return copy.deepcopy(self.children)
    
    def add_child(self, child):
        self.children.append(child)

    def set_best_move(self, move):
        self.best_move = move

    def get_best_move(self):
        return self.best_move
