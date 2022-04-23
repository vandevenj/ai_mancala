
from inspect import indentsize
from model import MancalaModel
from view import MancalaView

class MancalaDT:

    def __init__(self, playerNum):
        self.player_num = playerNum
        self.other_player_num = 1 - playerNum


    def getAction(self, gameState):
        actionDict = {}
        for action in gameState.get_legal_actions(self.player_num):
            actionDict[action] = self.evaluateAction(gameState, action)
            #print(f"Evaluating action {action}, result: {actionDict[action]}")
        print(actionDict)
        return max(actionDict, key=actionDict.get)


    def evaluateAction(self, gameState, index):
        nextIndex = (0 if self.player_num == 0 else 7) + index + 1
        beans = gameState.board[self.player_num][index]
        #print(f" \n\nEvaluating action {index} with {beans} bean(s), NextIndex = {nextIndex}")
        return self.evaluate_pit_consequences(gameState, nextIndex, beans, index)
        # player_side = gameState.board[self.player_num]
        # num_pits = gameState.get_num_pits()
        # pit_val = player_side[index]
        # landing_pit = index + pit_val
        # # Chain move
        # if num_pits == landing_pit:
        #     return index + 1 + num_pits # Cap unless there is a steal 
        # # Steals
        # elif landing_pit < num_pits and player_side[landing_pit] == 0: # lands on our side in empty pit
        #     opposite_pit_val = gameState.board[self.other_player_num][num_pits - landing_pit - 1]
        #     if not opposite_pit_val == 0:
        #         return opposite_pit_val + 1
        # # Defense
        # elif landing_pit > num_pits:
        #     val = pit_val + index - num_pits
        #     # Don't give them chain move
        #     opposite_index = (landing_pit - 1) % num_pits
        #     for affected_pit in range(0, opposite_index + 1): 
        #         affected_pit_val = gameState.board[self.other_player_num][affected_pit]
        #         if affected_pit_val + affected_pit == num_pits: # ruins opponent chain move
        #             val = val + num_pits + 1
        #         elif affected_pit_val + affected_pit + 1 == num_pits: #would set up opponent chain move
        #             val = val - num_pits

        #     opposite_pit_val = gameState.board[self.other_player_num][opposite_index]
        #     if opposite_pit_val + 1 == num_pits - opposite_index:
        #         return -num_pits - opposite_index # TODO
        #     else:
        #         return index - num_pits + 1
        # # Lands on our side
        # else: 
        #     val = pit_val + index - num_pits # Lower value move if nearly a chain 
        #     for affected_pit in range(index + 1, landing_pit):
        #         affected_pit_val = player_side[affected_pit]
        #         if affected_pit_val + affected_pit == num_pits: #if ruins chain move
        #             val = val - num_pits
        #         elif affected_pit_val + affected_pit + 1 == num_pits: # sets up chain move
        #             val = val + num_pits + 1
        #     return val


    def evaluate_pit_consequences(self, gamestate, index, current_beans, currentTotal):
        num_pits = gamestate.get_num_pits()
        maxIndex = (2 * num_pits + 1)
        onOurSide = not ((index <= num_pits) ^ (self.player_num == 0)) #bean is on our side of board 
        opponentScorePit = maxIndex - (num_pits + 1) * self.player_num
        scorePitIndex = maxIndex - (num_pits + 1) * self.other_player_num
        sideIndex = (index % num_pits) if index <= 6 else (index - 1) % num_pits
        #print(f"index: {index}, sideIndex: {sideIndex}, On our side: {onOurSide}, current beans: {current_beans}")
        #print(f"On our side: {onOurSide}, Opponent Score pit: {opponentScorePit}, our score pit: {scorePitIndex}, Side index: {sideIndex}, current beans: {current_beans}, Current total: {currentTotal}")
        if current_beans == 0:
            return currentTotal + (0 if index > num_pits else 1)
        if opponentScorePit == index:
            return self.evaluate_pit_consequences(gamestate, (index + 1) % (maxIndex + 1), current_beans, currentTotal) # move on to next pit
        if index == scorePitIndex and not current_beans == 1:
            return self.evaluate_pit_consequences(gamestate, (index + 1) % (maxIndex + 1), current_beans - 1, currentTotal + 1)
        pit_val = gamestate.board[self.player_num if onOurSide else self.other_player_num][sideIndex]
        opposite_pit_index = abs(sideIndex - num_pits + 1)
        opposite_pit_val = gamestate.board[self.other_player_num if onOurSide else self.player_num][opposite_pit_index]
        if onOurSide:
            if current_beans == 1:
                #print(f"With one marble, index: {index}")
                if index == scorePitIndex: # Chain
                    #print("Successful chain")
                    currentTotal += 2 * num_pits + 1
                elif pit_val == 0 and opposite_pit_val > 0: # steal
                        #print(f"Successful steal at index {index}")
                        currentTotal += opposite_pit_val + 1
            elif pit_val == num_pits - sideIndex: # ruined our chain 
                #print(f"Would ruin our chain move at index {index}")
                currentTotal -= num_pits 
            elif pit_val + 1 == num_pits - sideIndex: # created our chain
                #print(f"Would create our chain move at index {index}")
                #print(sideIndex)
                currentTotal += num_pits 

        else:
            if pit_val == num_pits - sideIndex: # ruined enemy chain
                #print(f"Would ruin their chain move at index {index}")
                currentTotal += num_pits * 0.8
            elif pit_val + 1 == num_pits - sideIndex: # created enemy chain
                #print(f"Would create their chain move at index {index}, sideindex: {sideIndex}")
                currentTotal -= num_pits * 0.8
        return self.evaluate_pit_consequences(gamestate, (index + 1) % (maxIndex + 1), current_beans - 1, currentTotal)
            
            
        



def play_dt():
    model = MancalaModel(6, 48)
    view = MancalaView(model)
    agent0 = MancalaDT(0)
    agent1 = MancalaDT(1)
    while not model.is_game_over():
        print(model.to_string())
        turn = model.get_player_turn()
        print(f"Player turn: {turn}")
        if turn == 0: # our turn 
            move = agent0.getAction(model)
            #move = int(input())
        else:
            move = agent1.getAction(model)
        #print(f"Player turn: {turn}, move selected: {move}")
        model.player_move(turn, move)
    
        
    winner = view.model.who_wins()
    if winner == -1:
        print(f"TIE!")
    else: 
        print(f"PLAYER {winner} wins!")


play_dt()