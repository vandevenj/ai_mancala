

from model import MancalaModel
from view import MancalaView
from tree import Tree


class MiniMax:
    """
    MiniMax AI implementation.
    """

    def __init__(self, model, player_num, depth):
        # TODO
        self.model = model
        self.current_player = 0 # Current moving player 
        self.player_num = player_num # What number the agent is 
        self.depth = depth # the depth to execute minimax until, all nodes at this depth treated as terminal
        self.tree = Tree(model) # the game state tree

    def getAction(self, gameState):
        """
        Returns the minimax action from the current state of the game
        """
        actions = {}
        legal = gameState.get_legal_actions(self.current_player) 
        for action in legal:
            successor = gameState.generate_successor(self.current_player, action)
            self.tree.add_child(Tree(successor))
            actions[action] = self.value(successor, self.model.next_player(self.current_player), self.depth)
            
        # print(actions)
        best = max(actions, key=actions.get)
        print("Chose action: " + str(best) + " with a score of " + str(actions[best]))
        
        self.tree.set_best_move(best)
        return best
        
    def maxValue(self, gameState, index, depth):
        #print("Getting max move value for index: " + str(index))
        v = -1000000000000
        if depth <= 0:
            return self.evaluationFunction(gameState)
        nextIndex = (index + 1) % gameState.get_num_players()
        for action in gameState.get_legal_actions(index):
            v = max(v, self.value(gameState.generate_successor(index, action), nextIndex, depth))
        return v

    def minValue(self, gameState, index, depth):
        v = 1000000000000
        nextIndex = (index + 1) % gameState.get_num_players()
        for action in gameState.get_legal_actions(index):
            v = min(v, self.value(gameState.generate_successor(index, action), nextIndex, depth))
        return v

    def value(self, gameState, index, depth, tree):
        child = Tree(gameState)
        if gameState.is_game_over():
            score = self.evaluationFunction(gameState)
            return score
        elif index == self.player_num:
            # if its the player's turn
            return self.maxValue(gameState, index, depth - 1)
        else:       
            # if its the CPU's turn
            return self.minValue(gameState, index, depth)

    # Evaluates the current game state 
    def evaluationFunction(self, state):
        scores = state.get_scores()
        return scores[self.player_num] - scores[1 if self.player_num == 0 else 0]


def play_minimax():
    model = MancalaModel(4, 8)
    view = MancalaView(model)
    agent = MiniMax(model, 1, 4)

    action = agent.getAction(model)
    
    winner = view.model.who_wins()
    if winner == -1:
        print(f"TIE!")
    else: 
        print(f"PLAYER {winner} wins!")


if __name__ == "__main__":
    play_minimax()