

class Tree:

    def __init__(self, model):
        self.model = model
        self.children = []
        self.best_move = -1

    def get_children(self):
        return self.children
    
    def add_child(self, child):
        self.children.append(child)

    def set_best_move(self, move):
        self.best_move = move

    def get_best_move(self):
        return self.best_move
