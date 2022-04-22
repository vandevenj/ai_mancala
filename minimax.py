
from model import MancalaModel
from view import MancalaView


class MiniMax:

    def __init__(self, player_num, depth):
        # TODO
        self.player_num = player_num # What number the agent is 
        self.depth = depth
        self.action_dict = {} # dict <State, action>


    def getAction(self, gameState):
        if gameState in self.action_dict.keys() and not (self.action_dict[gameState] == -1) :
            return self.action_dict[gameState]
        else:
            self.action_dict = {} # dump previous as we have most likely reached the previous depth
            self.computeActions(gameState)
            return self.getAction(gameState) # Should not infinitely recur 



    def computeActions(self, gameState):
        """
        Computes the actions up until self.depth. 
        """
        "*** YOUR CODE HERE ***"
        if gameState.is_game_over():
            print("Game is over!")
        else:
            if self.player_num == gameState.get_player_turn():
                self.maxValue(gameState, self.depth)
            else:
                self.minValue(gameState, self.depth)
        

    # Now stores what the best option is in the given gameState
    def maxValue(self, gameState, depth):
        v = -1000000000000
        maxAction = -1 
        if depth <= 0:
            self.action_dict[gameState] = maxAction
            return self.evaluationFunction(gameState)
        nextIndex = gameState.get_player_turn()
        #print(f"Max: nextIndex: {nextIndex}")
        #print(gameState.is_game_over())
        #print(len(gameState.get_legal_actions(nextIndex)))
        for action in gameState.get_legal_actions(nextIndex):
            action_val = self.value(gameState.generate_successor(nextIndex, action), depth)
            if action_val > v:
                maxAction = action
                v = action_val
        self.action_dict[gameState] = maxAction
        return v


    
    def minValue(self, gameState, depth):
        v = 1000000000000
        nextIndex = gameState.get_player_turn()
        #print(f"Min: nextIndex: {nextIndex}")
        for action in gameState.get_legal_actions(nextIndex):
            v = min(v, self.value(gameState.generate_successor(nextIndex, action), depth))
        return v


    def value(self, gameState, depth):
        nextIndex = gameState.get_player_turn()
        # print(gameState.to_string())
        if gameState.is_game_over():
            score = self.evaluationFunction(gameState)
            self.action_dict[gameState] = -1 # No action needed 
            return score
        elif nextIndex == self.player_num:
            return self.maxValue(gameState, depth - 1)
        else:            # Ghost turn
            return self.minValue(gameState, depth)

    # Evaluates the current game state 
    def evaluationFunction(self, state):
        value = 0
        player_side = state.board[self.player_num]
        for pit_index in range(len(player_side)):
            pit_val = player_side[pit_index] 
            if pit_index == state.num_pits: continue # don't care about score pit 
            if pit_val == state.num_pits - pit_index: # Has move chain TODO: incorporate value from subsequent move 
                value += 5 
            if pit_val >= state.num_pits - pit_index: # has moves that can score 
                value += 1
                
            # TODO: stealing
            # TODO: defense 
        scores = state.get_scores()
        score_diffs = scores[self.player_num] - scores[1 if self.player_num == 0 else 0]
        value += score_diffs
        # print("***Begin Eval***")
        # print(state.to_string())
        # print(f"Player: {self.player_num}, Value: {value}")
        # print("***End Eval***")
        return value
    



def play_minimax():
    model = MancalaModel(3, 12)
    view = MancalaView(model)
    agent0 = MiniMax(0, 3)
    agent1 = MiniMax(1, 3)
    while not model.is_game_over():
        print(model.to_string())
        turn = model.get_player_turn()
        print(f"Player turn: {turn}")
        if turn == 0: # our turn 
            move = agent0.getAction(model)
        else:
            move = agent1.getAction(model)
        print(f"Player turn: {turn}")
        model.player_move(turn, move)
    
        
    winner = view.model.who_wins()
    if winner == -1:
        print(f"TIE!")
    else: 
        print(f"PLAYER {winner} wins!")



play_minimax()

# agent1 = MiniMax(0, 4)
# agent2 = MiniMax(1, 4)
# model = MancalaModel(4, 8)
# move = agent1.getAction(model)
# print(move)
# model.player_move(0, agent1.getAction(model))
# model.player_move(1, agent2.getAction(model))