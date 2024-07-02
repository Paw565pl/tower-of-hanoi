from time import sleep
from typing import Literal


def game(disks_amount: int, who_plays: Literal['player', 'cpu']):
    def print_board(board):
        for i in range(len(board[0])):
            if board[0][i] >= 1:
                print('-' * board[0][i], ' ' * (len(board[0]) - board[0][i]),
                      end='')
            else:
                print('|', ' ' * (len(board[0]) - 1), end='')
            if board[1][i] >= 1:
                print('-' * board[1][i], ' ' * (len(board[1]) - board[1][i]),
                      end='')
            else:
                print('|', ' ' * (len(board[1]) - 1), end='')
            if board[2][i] >= 1:
                print('-' * board[2][i], ' ' * (len(board[2]) - board[2][i]),
                      end='')
            else:
                print('|', ' ' * (len(board[2]) - 1), end='')
            print('')

    def change_structure(structure):
        from_choice = None
        on_choice = None

        if who_plays == 'player':
            from_choice = int(input('Which tower do you want to move the disk from? Enter the tower number [0 to exit]\n> '))
            if from_choice == 0:
                print('Goodbye!')
                exit()
            on_choice = int(input('Which tower do you want to move the disk to? Enter the tower number [0 to exit]\n> '))
            if on_choice == 0:
                print('Goodbye!')
                exit()

            print('')

        elif who_plays == 'cpu':
            from_choice = steps.pop(0)
            on_choice = steps.pop(0)

        from_choice -= 1
        on_choice -= 1

        # disks change
        if from_choice in [0, 1, 2] and on_choice in [0, 1, 2] and from_choice != on_choice:
            i_to_take = None
            i_to_replace = None

            if structure[from_choice] == [0] * disks_amount:
                print('You can\'t take from an empty tower!')
                return False

            for element in structure[from_choice]:
                if element != 0:
                    i_to_take = structure[from_choice].index(element)
                    break

            for element in structure[on_choice][::-1]:
                if element == 0:
                    i_to_replace = len(structure[on_choice]) - 1 - structure[on_choice][
                                                                              ::-1].index(element)
                    break

            # block invalid moves
            if structure[on_choice][-1] != 0 and structure[from_choice][i_to_take] > \
                    structure[on_choice][i_to_replace + 1]:
                print('Invalid move!')
                return False
            else:
                structure[from_choice][i_to_take], structure[on_choice][i_to_replace] = \
                    structure[on_choice][i_to_replace], structure[from_choice][i_to_take]
                return True

        else:
            print('Invalid input!\n')

    steps = []

    def find_game_solution(n, s_pole, d_pole, i_pole):
        if n == 1:
            steps.append(s_pole)
            steps.append(d_pole)
            return
        
        find_game_solution(n - 1, s_pole, i_pole, d_pole)
        steps.append(s_pole)
        steps.append(d_pole)
        find_game_solution(n - 1, i_pole, d_pole, s_pole)

    game_board = [
        [x for x in range(1, disks_amount + 1)],
        [0] * disks_amount,
        [0] * disks_amount
    ]

    moves_counter = 0

    if who_plays == 'player':
        while True:
            print_board(game_board)

            print(f'Number of moves made: {moves_counter}\n')

            # winning condition
            if game_board[2] == [x for x in range(1, disks_amount + 1)]:
                print('You won! Congrats 😊')
                break

            if change_structure(game_board):
                moves_counter += 1

    elif who_plays == 'cpu':
        find_game_solution(disks_amount, 1, 3, 2)
        while True:
            print_board(game_board)

            print(f'Number of moves made: {moves_counter}\n')

            if game_board[2] == [x for x in range(1, disks_amount + 1)]:
                print('Game has been won!')
                break

            sleep(1)

            change_structure(game_board)
            moves_counter += 1


def main():
    print(
        'Welcome to the "Tower of Hanoi" game!\nYour goal is to move the disks to the last peg.'
        '\nYou cannot place larger disks on top of smaller ones. Good luck!'
    )
    while True:
        game_choice = input('\n[1] Play\n[2] Let the CPU play\n[0] Exit\n> ')
        if game_choice == '1':
            print('')
            disk_choice = int(input('How many disks?\n> '))
            game(disk_choice, 'player')
        elif game_choice == '2':
            print('')
            disk_choice = int(input('How many disks?\n> '))
            game(disk_choice, 'cpu')
        elif game_choice == '0':
            print('Goodbye!')
            break
        else:
            print('Invalid input!')

if __name__ == '__main__':
    main()
