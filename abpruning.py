from model import MancalaModel
from view import MancalaView



class AlphaBetaAgent:
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def __init__(self, player_num, depth):
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
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #self.value(gameState, gameState.get_player_turn(), self.depth, float("-inf"), float("inf"))
        # print("Computing actions")
        actions = {}
        index = gameState.get_player_turn()
        legal = gameState.get_legal_actions(index)
        alpha = float("-inf")
        beta = float("inf")
        for action in legal:
            actions[action] = self.value(gameState.generate_successor(index, action), self.depth, alpha, beta)
            alpha = max(alpha, actions[action])
            # print(f"Action: {action}, Value: {actions[action]}")
        best = max(actions, key=actions.get)
        self.action_dict[gameState] = best 
        
        

    def maxValue(self, gameState, depth, alpha, beta):
        v = -1000000000000
        index = gameState.get_player_turn()
        if depth <= 0:
            self.action_dict[gameState] = -1
            return self.evaluationFunction(gameState, index)
        max_action = None
        for action in gameState.get_legal_actions(index):
            action_val = self.value(gameState.generate_successor(index, action), depth, alpha, beta)
            if action_val > v:
                max_action = action
                v = action_val
            if v > beta:
                return v
            alpha = max(alpha, v)
        self.action_dict[gameState] = max_action
        return v


    
    def minValue(self, gameState, depth, alpha, beta):
        v = 1000000000000
        index = gameState.get_player_turn()
        for action in gameState.get_legal_actions(index):
            v = min(v, self.value(gameState.generate_successor(index, action), depth, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v


    def value(self, gameState, depth, alpha, beta):
        index = gameState.get_player_turn()
        if gameState.is_game_over():
            score = self.evaluationFunction(gameState, index)
            return score
        elif index == 0: # Player 0 turn
            v = self.maxValue(gameState, depth - 1, alpha, beta)
            return v
        else:            # Player 1 turn
            v = self.minValue(gameState, depth, alpha, beta)
            return v


     # Evaluates the current game state 
    def evaluationFunction(self, state, turn):
        discount = 0.2
        factor = state.get_num_pits()
        value = 0
        best_chain = 0
        player_side = state.board[turn]
        for pit_index in range(len(player_side)):
            pit_val = player_side[pit_index] 
            if pit_index == state.num_pits: continue # don't care about score pit 
            if pit_val == state.num_pits - pit_index: # Has move chain TODO: incorporate value from subsequent move 
                best_chain = max(discount * self.evaluationFunction(state.generate_successor(turn, pit_index), turn), best_chain) 
            if pit_val >= state.num_pits - pit_index: # has moves that can score 
                value += 1
                
            # TODO: stealing
            # TODO: defense 
        scores = state.get_scores()
        score_diffs = scores[turn] - scores[1 if turn == 0 else 0]
        # print("***Begin Eval***")
        # print(state.to_string())
        # print(f"Player: {self.player_num}, Value: {value}")
        # print("***End Eval***")
        return value + best_chain + 3 * score_diffs


def play_abpruning():
    model = MancalaModel(6, 48)
    view = MancalaView(model)
    agent0 = AlphaBetaAgent(0, 4)
    agent1 = AlphaBetaAgent(1, 4)
    while not model.is_game_over():
        print(model.to_string())
        turn = model.get_player_turn()
        print(f"Eval for current player: {agent1.evaluationFunction(model, turn)}")
        #print(f"Legal actions: {model.get_legal_actions(turn)}")
        if turn == 0: # our turn 
            #move = agent0.getAction(model)
            move = int(input())
        else:
            move = agent1.getAction(model)
        print(f"Player turn: {turn}, move selected: {move}")
        model.player_move(turn, move)
    
        
    winner = view.model.who_wins()
    if winner == -1:
        print(f"TIE!")
    else: 
        print(f"PLAYER {winner} wins!")


# model = MancalaModel(6, 48)
# print(model.to_string())
# print(model.get_scores())
# print(AlphaBetaAgent(0, 3).evaluationFunction(model, 0))
# model.player_move(0, 2)
# print(model.to_string())
# print(model.get_scores())
# print(AlphaBetaAgent(0, 3).evaluationFunction(model, 0))
# model.player_move(0, 5)
# print(model.to_string())
# print(model.get_scores())
# print(AlphaBetaAgent(0, 3).evaluationFunction(model, 0))
# model.player_move(1, 1)
# print(model.to_string())
# print(model.get_scores())
# print(AlphaBetaAgent(1, 3).evaluationFunction(model, 1))
# model.player_move(1, 5)
# print(model.to_string())
# print(model.get_scores())
# print(AlphaBetaAgent(1, 3).evaluationFunction(model, 1))
play_abpruning()