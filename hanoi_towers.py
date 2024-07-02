from time import sleep
from typing import Literal


def game(disks_amount: int, who_plays: Literal['player', 'cpu']):
    def print_structure(structure):
        for i in range(len(structure['tower-1'])):
            if structure['tower-1'][i] >= 1:
                print('-' * structure['tower-1'][i], ' ' * (len(structure['tower-1']) - structure['tower-1'][i]),
                      end='')
            else:
                print('|', ' ' * (len(structure['tower-1']) - 1), end='')
            if structure['tower-2'][i] >= 1:
                print('-' * structure['tower-2'][i], ' ' * (len(structure['tower-2']) - structure['tower-2'][i]),
                      end='')
            else:
                print('|', ' ' * (len(structure['tower-2']) - 1), end='')
            if structure['tower-3'][i] >= 1:
                print('-' * structure['tower-3'][i], ' ' * (len(structure['tower-3']) - structure['tower-3'][i]),
                      end='')
            else:
                print('|', ' ' * (len(structure['tower-3']) - 1), end='')
            print('')

    def change_structure(structure):
        from_choice = None
        on_choice = None

        if who_plays == 'player':
            from_choice = input('Which tower do you want to move the disk from? Enter the tower number [0 to exit]\n> ')
            if from_choice == '0':
                print('Goodbye!')
                exit()
            on_choice = input('Which tower do you want to move the disk to? Enter the tower number [0 to exit]\n> ')
            if on_choice == '0':
                print('Goodbye!')
                exit()

            print('')

        elif who_plays == 'cpu':
            from_choice = steps.pop(0)
            on_choice = steps.pop(0)

        # disks change
        if from_choice in ['1', '2', '3'] and on_choice in ['1', '2', '3'] and from_choice != on_choice:
            i_to_take = None
            i_to_replace = None

            if structure[f'tower-{from_choice}'] == [0] * disks_amount:
                print('You can\'t take from an empty tower!')
                return False

            for element in structure[f'tower-{from_choice}']:
                if element != 0:
                    i_to_take = structure[f'tower-{from_choice}'].index(element)
                    break

            for element in structure[f'tower-{on_choice}'][::-1]:
                if element == 0:
                    i_to_replace = len(structure[f'tower-{on_choice}']) - 1 - structure[f'tower-{on_choice}'][
                                                                              ::-1].index(element)
                    break

            # block invalid moves
            if structure[f'tower-{on_choice}'][-1] != 0 and structure[f'tower-{from_choice}'][i_to_take] > \
                    structure[f'tower-{on_choice}'][i_to_replace + 1]:
                print('Invalid move!')
                return False
            else:
                structure[f'tower-{from_choice}'][i_to_take], structure[f'tower-{on_choice}'][i_to_replace] = \
                    structure[f'tower-{on_choice}'][i_to_replace], structure[f'tower-{from_choice}'][i_to_take]
                return True

        else:
            print('Invalid input!\n')

    steps = []

    def cpu_game(n, s_pole, d_pole, i_pole):
        if n == 1:
            steps.append(s_pole)
            steps.append(d_pole)
            return
        cpu_game(n - 1, s_pole, i_pole, d_pole)
        steps.append(s_pole)
        steps.append(d_pole)
        cpu_game(n - 1, i_pole, d_pole, s_pole)

    game_structure = {
        'tower-1': [x for x in range(1, disks_amount + 1)],
        'tower-2': [0] * disks_amount,
        'tower-3': [0] * disks_amount
    }

    moves_counter = 0

    if who_plays == 'player':
        while True:
            print_structure(game_structure)

            print(f'Number of moves made: {moves_counter}\n')

            # winning condition
            if game_structure['tower-3'] == [x for x in range(1, disks_amount + 1)]:
                print('You won! Congrats 😊')
                break

            if change_structure(game_structure):
                moves_counter += 1

    elif who_plays == 'cpu':
        cpu_game(disks_amount, '1', '3', '2')
        while True:
            print_structure(game_structure)

            print(f'Number of moves made: {moves_counter}\n')

            if game_structure['tower-3'] == [x for x in range(1, disks_amount + 1)]:
                print('Game has been won!')
                break

            sleep(1)

            change_structure(game_structure)
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
