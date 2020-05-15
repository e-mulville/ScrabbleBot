import copy
from brute_force import BruteForce
from tree_search import brie_search

not_letters = ["   ", " * ", "TLS", "TWS", "DLS", "DWS"]

def find_best_moves(board, rack):

    rack = [ rack.rack[i].get_letter() for i in range(len(rack.rack)) ]

    clean_board = copy.deepcopy(board.board)


    #best_move = BruteForce(board, rack)
    best_move = brie_search(clean_board,rack)

    return best_move

def score_word(board, word, direction, x, y):
    LETTER_VALUES = {"A": 1,
                     "B": 3,
                     "C": 3,
                     "D": 2,
                     "E": 1,
                     "F": 4,
                     "G": 2,
                     "H": 4,
                     "I": 1,
                     "J": 1,
                     "K": 5,
                     "L": 1,
                     "M": 3,
                     "N": 1,
                     "O": 1,
                     "P": 3,
                     "Q": 10,
                     "R": 1,
                     "S": 1,
                     "T": 1,
                     "U": 1,
                     "V": 4,
                     "W": 4,
                     "X": 8,
                     "Y": 4,
                     "Z": 10,
                     "#": 0}

    sum = 0

    multiplier = 1

    #score any horizontal words
    for index, char in enumerate(word):
        if direction == "horizontal":
            board_char = board[y][x+index]
        elif direction == "vertical":
            board_char = board[y+index][x]

        if board_char == "DLS":
            sum += LETTER_VALUES[char] * 2
        elif board_char == "TLS":
            sum += LETTER_VALUES[char] * 3

        elif board_char == "DWS":
            multiplier = multiplier * 2
            sum += LETTER_VALUES[char]
        elif board_char == " * ":
            multiplier = multiplier * 2
            sum += LETTER_VALUES[char]

        elif board_char == "TWS":
            multiplier = multiplier * 3
            sum += LETTER_VALUES[char]

        else:
            sum += LETTER_VALUES[char]

    return sum * multiplier

def is_word_in_dictionary(word):
    return word in clean_dictionary

def get_board(clean_board):
    #Returns the board in string form.
    board_str = "   |  " + "  |  ".join(str(item) for item in range(10)) + "  | " + "  | ".join(str(item) for item in range(10, 15)) + " |"
    board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    board = copy.deepcopy(clean_board)
    for i in range(len(board)):
        if i < 10:
            spaced_items = []
            for item in board[i]:
                if item != "TLS" and item != "TWS" and item != "DLS" and item != "DWS" and item != " * "and item != "   ":
                    spaced_items.append(" " + item + " ")
                else:
                    spaced_items.append(item)

            board[i] = str(i) + "  | " + " | ".join(str(item) for item in spaced_items) + " |"
        if i >= 10:
            spaced_items = []
            for item in board[i]:
                if item != "TLS" and item != "TWS" and item != "DLS" and item != "DWS" and item != " * "and item != "   ":
                    spaced_items.append(" " + item + " ")
                else:
                    spaced_items.append(item)
            board[i] = str(i) + " | " + " | ".join(str(item) for item in spaced_items) + " |"
    board_str += "\n   |_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|\n".join(board)
    board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _"
    return board_str
