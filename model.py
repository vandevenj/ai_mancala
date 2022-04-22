import copy

class MancalaModel:
    def __init__(self, num_pits, num_beans):
        # num_pits is number of non-score pits
        # num beans is total beans on board
        # TODO - add more rule specifications
        self.num_players = 2
        self.num_beans = num_beans
        if num_pits <= 0:
            raise Exception("Number of pits on the board must be greater than 0")
        self.num_pits = num_pits # score pit numbr 
        self.player_turn = 0
        self.board = []
        for i in range(0, self.num_players):
            # TODO - weird bean number logic, needs to be verified -- off by ones?
            self.board.append([int(num_beans / num_pits / self.num_players)] * (num_pits))
            self.board[i].append(0)

    # Gets the current board as a 2d array 
    def get_current_board(self):
        # produces copy of game board 
        return copy.deepcopy(self.board)

    # gets the number of players
    def get_num_players(self):
        return self.num_players

    # Gets the player ID whose turn it is 
    def get_player_turn(self):
        return self.player_turn

    # Gets the number of pits on each player's side of board 
    def get_num_pits(self):
        return self.num_pits
    
    # Determines if the pit at the current indexes is empty 
    def is_empty_pit(self, player_id, pit_id):
        return self.board[player_id][pit_id] == 0

    # Gets the number of the next player to move 
    def next_player(self, player_id):
        return (player_id + 1) % self.num_players

    def is_game_over(self):
        p1_actions = self.get_legal_actions(0)
        p2_actions = self.get_legal_actions(1)
        game_over = len(p1_actions) == 0 or len(p2_actions) == 0

        if game_over:
            for player in  range(0, len(self.board)):
                for pit in range(0, self.num_pits):
                    self.board[player][self.num_pits] += self.board[player][pit] 
                    self.board[player][pit] = 0
            return True
        return False

    def who_wins(self):
        # Note: hardcoded for two players
        # check if player zero wins
        zero = self.board[0][self.num_pits] > self.board[1][self.num_pits]
        # check if player one wins
        one = self.board[1][self.num_pits] > self.board[0][self.num_pits]
        # if neither win then tie
        return 0 if zero else 1 if one else -1

    # Stealing!! 
    def snatch_unguarded_pit(self, curr_player, curr_pit):
        # get unguarded pit
        unguarded_pit = self.num_pits - curr_pit - 1 #TODO - check accuracy of which pit is being snatched
        # empty current pit
        self.board[curr_player][curr_pit] -= 1 #should be 0 after this
        # add opponent unguarded pit to player's score pit
        self.board[curr_player][self.num_pits] += 1 + self.board[self.next_player(curr_player)][unguarded_pit]
        # empty oppoinent's pit
        self.board[self.next_player(curr_player)][unguarded_pit] = 0

        # performs a player move 
    def player_move(self, player_id, pit_to_move):
        if player_id != self.player_turn:
            raise Exception(f"Player {player_id} tried to move when it is player {self.player_turn}'s turn")
        another_turn = False
        # if pit has any beans in it
        num_beans_to_move = self.board[player_id][pit_to_move]
        self.board[player_id][pit_to_move] = 0
        curr_pit = pit_to_move
        curr_player = player_id

        while num_beans_to_move > 0:
            
            curr_pit += 1

            # if curr_pit is score pit, end of player's board, reset to start of next player's board
            if self.num_pits == curr_pit:
                # only increment beans in current turn's player's score pit
                if curr_player == player_id:
                    # increment beans in pit
                    self.board[curr_player][curr_pit] += 1
                    num_beans_to_move -= 1
                    if num_beans_to_move == 0 and not self.is_game_over():
                        # print(self.to_string())
                        another_turn = True

                curr_pit = -1
                curr_player = self.next_player(player_id)

            else:
                # increment beans in pit
                self.board[curr_player][curr_pit] += 1
                num_beans_to_move -= 1
                # if the last bean is put into an empty pit on the current turn player's board, steal from corresponding opponent's pit
                if num_beans_to_move == 0 and curr_player == self.player_turn and self.board[curr_player][curr_pit] == 1:
                    self.snatch_unguarded_pit(curr_player, curr_pit) 
        if not another_turn:
            self.player_turn = self.next_player(player_id)

    # Returns a 2-item list of the scores
    def get_scores(self):
        scores = []
        for player in range(self.num_players):
            scores.append(self.board[player][self.num_pits])
        return scores

    # ----------------------------------------------------------------------------------------------  #
    # NOTE: MiniMax-related functions below this line! Everything above needed for Standard Mancala.
    # ----------------------------------------------------------------------------------------------  #

    # gets the legal actions on a player's side 
    def get_legal_actions(self, player):
        player_side = self.board[player]
        result = []
        for i in range(self.num_pits):
            if self.is_legal_move(player, i):
                result.append(i)
        return result
        
    # returns true if the move is not on an empty space or the goal space 
    def is_legal_move(self, player, index):
        in_range = len(self.board[0]) > index and index >= 0
        return not self.is_empty_pit(player, index) and self.get_num_pits() != index and in_range

    # Returns a representation of the model after performing the specified move (without mutating the original)
    def generate_successor(self, player_id, pit_to_move):
        successor = copy.deepcopy(self)
        successor.player_move(player_id, pit_to_move)
        return successor

    def to_string(self):
         # NOTE currently hardcoded for two players; last pit is score pit
        board = self.get_current_board()
        num_pits = self.get_num_pits()
        player = board[1]
        output = "\n|"
        pit = num_pits
        while pit >= 0:
            # score pit
            if pit == num_pits:
                output += f"[{player[pit]:02}]|"
            # movable pit
            else:
                output += f"{player[pit]:02}|"
            pit -= 1
            
        # user, b
        player = board[0]
        output += f"\n     |"
        for pit in range(0, len(player)):
            # score pit
            if pit == num_pits:
                output += f"[{player[pit]:02}]|"
            # movable pit
            else:
                output += f"{player[pit]:02}|"
        return output

    #Necessary for using as dict keys 
    def __hash__(self) -> int:
        return hash(self.to_string())

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.board == other.board and self.player_turn == other.player_turn
    



            





