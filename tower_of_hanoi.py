from time import sleep
from typing import Literal


def get_int_input(prompt: str) -> int:
    try:
        value = int(input(prompt))
        return value
    except ValueError:
        print("Invalid input! Expected integer number.")


def print_board(board):
    for i in range(len(board[0])):
        if board[0][i] >= 1:
            print("-" * board[0][i], " " * (len(board[0]) - board[0][i]), end="")
        else:
            print("|", " " * (len(board[0]) - 1), end="")
        if board[1][i] >= 1:
            print("-" * board[1][i], " " * (len(board[1]) - board[1][i]), end="")
        else:
            print("|", " " * (len(board[1]) - 1), end="")
        if board[2][i] >= 1:
            print("-" * board[2][i], " " * (len(board[2]) - board[2][i]), end="")
        else:
            print("|", " " * (len(board[2]) - 1), end="")
        print("")


def move_disk(board, disks_amount: int, from_peg: int, to_peg: int) -> bool:
    from_peg -= 1
    to_peg -= 1

    if from_peg not in [0, 1, 2] or to_peg not in [0, 1, 2] or from_peg == to_peg:
        return False

    # disks change
    i_to_take = None
    i_to_replace = None

    if board[from_peg] == [0] * disks_amount:
        return False

    for element in board[from_peg]:
        if element != 0:
            i_to_take = board[from_peg].index(element)
            break

    for element in board[to_peg][::-1]:
        if element == 0:
            i_to_replace = len(board[to_peg]) - 1 - board[to_peg][::-1].index(element)
            break

    # block invalid moves
    if (
        board[to_peg][-1] != 0
        and board[from_peg][i_to_take] > board[to_peg][i_to_replace + 1]
    ):
        return False
    else:
        board[from_peg][i_to_take], board[to_peg][i_to_replace] = (
            board[to_peg][i_to_replace],
            board[from_peg][i_to_take],
        )
        return True


def find_solution(
    disks_amount: int, source_peg: int, destination_peg: int, auxiliary_peg: int
) -> list[tuple[int, int]]:
    steps = []

    def helper(n: int, s_pole: int, d_pole: int, i_pole: int):
        if n == 1:
            steps.append((s_pole, d_pole))
            return

        helper(n - 1, s_pole, i_pole, d_pole)
        steps.append((s_pole, d_pole))
        helper(n - 1, i_pole, d_pole, s_pole)

    helper(disks_amount, source_peg, destination_peg, auxiliary_peg)
    return steps


def game(disks_amount: int, who_plays: Literal["player", "cpu"]):
    board = [
        [x for x in range(1, disks_amount + 1)],
        [0] * disks_amount,
        [0] * disks_amount,
    ]

    moves_counter = 0

    if who_plays == "player":
        while True:
            print_board(board)
            print(f"Number of moves made: {moves_counter}\n")

            # winning condition
            if board[2] == [x for x in range(1, disks_amount + 1)]:
                print("You won! Congrats 😊\n")
                break

            from_peg = get_int_input(
                "Which tower do you want to move the disk from? Enter the tower number [0 to exit]\n> "
            )
            if from_peg == 0:
                return

            to_peg = get_int_input(
                "Which tower do you want to move the disk to? Enter the tower number [0 to exit]\n> "
            )
            if to_peg == 0:
                return

            is_move_successful = move_disk(board, disks_amount, from_peg, to_peg)
            if is_move_successful:
                moves_counter += 1
            else:
                print("Invalid move!")

    elif who_plays == "cpu":
        solution = find_solution(disks_amount, 1, 3, 2)
        for i in range(0, len(solution) + 1):
            print_board(board)
            print(f"Number of moves made: {moves_counter}\n")

            # winning condition
            if board[2] == [x for x in range(1, disks_amount + 1)]:
                print("Game has been won!\n")
                break

            sleep(1)

            from_peg, to_peg = solution[i]
            move_disk(board, disks_amount, from_peg, to_peg)
            moves_counter += 1


def main():
    print(
        """Welcome to the "Tower of Hanoi" game! Your goal is to move the disks to the last peg.
You cannot place larger disks on top of smaller ones. Good luck!
"""
    )

    while True:
        print("Type your choice in the console.")
        choice = input("[1] Play\n[2] Let the CPU play\n[0] Exit\n> ")
        if choice == "1":
            disk_choice = int(input("How many disks?\n> "))
            game(disk_choice, "player")
        elif choice == "2":
            disk_choice = int(input("How many disks?\n> "))
            game(disk_choice, "cpu")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid input!")


if __name__ == "__main__":
    main()
