

from controller import MancalaController


class MancalaView:

    def __init__(self):
        self.controller = MancalaController()

    def display(self):
        # NOTE currently hardcoded for two players
        board = self.controller.get_current_board()
        num_pits = self.controller.get_num_pits()
        player = board[1]
        print(f"\n|")
        pit = num_pits - 1
        while pit >= 0:
            if pit == num_pits - 1:
                print(f" [{player[pit]}] |")
            else:
                print(f" {player[pit]} |")
            pit -= 1
            
        # user, b
        player = board[0]
        print(f"\n|")
        for pit in range(0, len(player)):
            if pit == num_pits - 1:
                print(f" [{player[pit]}] |")
            else:
                print(f" {player[pit]} |")
        