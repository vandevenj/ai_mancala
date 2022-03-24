

from model import MancalaModel


class MancalaView:

    def __init__(self, num_pits, num_beans):
        self.model = MancalaModel(num_pits, num_beans)

    def display(self):
        # NOTE currently hardcoded for two players
        board = self.model.get_current_board()
        num_pits = self.model.get_num_pits()
        player = board[1]
        output = "\n|"
        pit = num_pits
        while pit >= 0:
            # score pit
            if pit == num_pits:
                output += f" [{player[pit]}] |"
            # movable pit
            else:
                output += f" {player[pit]} |"
            pit -= 1
            
        # user, b
        player = board[0]
        output += f"\n|"
        for pit in range(0, len(player)):
            # score pit
            if pit == num_pits:
                output += f" [{player[pit]}] |"
            # movable pit
            else:
                output += f" {player[pit]} |"
        print(output)

    def player_plays(self, player_id, pit_to_move):
        # TODO: prevent moving score pit?
        while(self.model.is_empty_pit(player_id, pit_to_move)):
            pit_to_move = int(input("Cannot choose empty pit. Choose again: \n"))
        self.model.player_move(player_id, pit_to_move)
    
    def is_game_over(self):
        return self.model.is_game_over()
        

    def play(self):
        while(not self.is_game_over()):
            self.display()
            # if user, player 0 turn
            if self.model.player_turn == 0:
                print(f"PLAYER TURN: {self.model.player_turn}")
                user_pit_to_move = int(input())
                self.player_plays(0, user_pit_to_move)
            
            else:
                print(f"PLAYER TURN: {self.model.player_turn}")
                user_pit_to_move = int(input())
                self.player_plays(1, user_pit_to_move)
        winner = self.model.who_wins()
        if winner == -1:
            print(f"TIE!")
        else: 
            print(f"PLAYER {winner} wins!")

mancala = MancalaView(4, 8)  
mancala.play()