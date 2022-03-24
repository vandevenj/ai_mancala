


from model import MancalaModel
from view import MancalaView


class MancalaController:

    def __init__(self, num_pits, num_beans):
        self.model = MancalaModel(num_pits, num_beans)
        self.view = MancalaView()

    def play(self):
        print(self.view.display())
        user_pit_to_move = int(input())
        self.player_plays(0, user_pit_to_move)
    
    def player_plays(self, player_id, pit_to_move):
        # TODO: prevent moving score pit?
        self.model.move(player_id, pit_to_move)

    def get_current_board(self):
        return self.model.get_current_board()
    
    def get_num_pits(self):
        return self.model.get_num_pits()
        

