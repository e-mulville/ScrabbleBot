import random
import copy

from itertools import combinations

from tree_search import brie_search

from brute_force import get_board

def end_game_search(board, rack, other_rack, bag):

    global M, O, R, N

    #number of moves considered for player
    M = 10
    #number of moves for opponent
    O = 10

    unknown_tiles = other_rack + bag

    best_move = {
                "score" : 0,
                "word" : "N/A",
                "heuristic" : float('-inf')
            }


    next_moves = brie_search(board, rack, M)

    leftover_tiles = len(unknown_tiles)

    if leftover_tiles > 8:
        return next_moves[-1]
    else:
        opp_racks = list(combinations(unknown_tiles,min(7, leftover_tiles)))

    for move in next_moves:

        clean_board = copy.deepcopy(board)

        word = move["word"]

        if move["word"] != "N/A":
            if move["direction"] == "horizontal":
                for i in range(len(word)):
                    clean_board[move["Y"]][move["X"]+i] = word[i]
            else:
                for i in range(len(word)):
                    clean_board[move["Y"]+i][move["X"]] = word[i]

        future_score = 0

        i = 0
        for opp_rack in opp_racks:
            i += 1
            #try different combos of opponent racks
            remaining_letters = copy.deepcopy(unknown_tiles)

            for letter in list(opp_rack):
                remaining_letters.remove(letter)

            #get future value for each move

            if move["word"] != "N/A":

                alpha = float('inf')
                beta = float('-inf')

                future_score += move["score"] + look_opponent_turn(clean_board, remaining_letters, move["rack"], list(opp_rack), 0, alpha, beta)

        if move["word"] != "N/A":
            if future_score > best_move["heuristic"]:
                best_move = { "score" : move["score"], "word" : move["word"], "X" : move["X"], "Y" : move["Y"], "direction" : move["direction"], "heuristic" : future_score}

    return best_move



def look_self_turn(board, bag, self_rack, opp_rack, accu, alpha, beta):
    #needs to take randomly from Bag

    global M, O, R, N

    needed_letters = 7 - len(self_rack)

    max_future_score = float('-inf')

    #the value of a move is its score + future values
    if len(bag) >= needed_letters:
        random_racks = list(combinations(bag,needed_letters))
    else:
        random_racks = [tuple(bag)]

    average_accu = 0

    for rack in random_racks:

        random_rack = self_rack + list(rack)

        remaining_letters = copy.deepcopy(bag)

        for letter in list(rack):
            remaining_letters.remove(letter)

        next_moves = brie_search(board, random_rack, M)

        for move in next_moves:

            word = move["word"]

            if word != "N/A":

                clean_board = copy.deepcopy(board)

                score = move["score"]

                move_score = accu + score

                if move["direction"] == "horizontal":
                    for i in range(len(word)):
                        clean_board[move["Y"]][move["X"]+i] = word[i]
                else:
                    for i in range(len(word)):
                        clean_board[move["Y"]+i][move["X"]] = word[i]

                eval = look_opponent_turn(clean_board, remaining_letters, move["rack"], opp_rack, move_score, alpha, beta)
            else:
                eval = accu

            if eval > max_future_score:
                max_future_score = eval


        average_accu += max_future_score
        # alpha = max(alpha, move_score)
        #
        # if beta <= alpha:
        #     break

    return average_accu / len(random_racks)


def look_opponent_turn(board, bag, self_rack, opp_rack, accu, alpha, beta):

    #needs to take randomly from Bag

    global M, O, R, N

    #the value of a move is its score + future values
    needed_letters = 7 - len(opp_rack)

    min_future_score = float('inf')

    #the value of a move is its score + future values
    if len(bag) >= needed_letters:
        random_racks = list(combinations(bag,needed_letters))
    else:
        random_racks = [tuple(bag)]

    average_accu = 0

    for rack in random_racks:

        random_rack = opp_rack + list(rack)

        remaining_letters = copy.deepcopy(bag)

        for letter in list(rack):
            remaining_letters.remove(letter)

        next_moves = brie_search(board, random_rack, O)

        for move in next_moves:

            word = move["word"]

            if word != "N/A":

                clean_board = copy.deepcopy(board)

                score = move["score"]

                move_score = accu - score

                if move["direction"] == "horizontal":
                    for i in range(len(word)):
                        clean_board[move["Y"]][move["X"]+i] = word[i]
                else:
                    for i in range(len(word)):
                        clean_board[move["Y"]+i][move["X"]] = word[i]

                eval = look_self_turn(clean_board, remaining_letters, self_rack, move["rack"], move_score, alpha, beta)
            else:
                eval = accu

            if eval < min_future_score:
                min_future_score = eval


        average_accu += min_future_score
        # alpha = max(alpha, move_score)
        #
        # if beta <= alpha:
        #     break

    return average_accu / len(random_racks)
