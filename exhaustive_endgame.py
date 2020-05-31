import random
import copy

from itertools import permutations

from tree_search import brie_search

def end_game_search(board, rack, other_rack, bag):

    global M, O, R, N

    #number of moves considered for player
    M = 20
    #number of moves for opponent
    O = 20
    #number of racks guessed
    R = 10

    unknown_tiles = other_rack + bag

    best_move = {
                "score" : 0,
                "word" : "N/A",
                "heuristic" : -9999999999
            }


    next_moves = brie_search(board, rack, M)

    leftover_tiles = len(unknown_tiles)
    if leftover_tiles > 10:
        return next_moves[0]
    else:
        bags = list(permutations(unknown_tiles))

    for bag in bags:

        print(bag)
        for move in next_moves:
            #get future value for each move

            if move["word"] != "N/A":

                future_score = 0

                alpha = float('inf')
                beta = float('-inf')

                future_score += move["score"] + (look_opponent_turn(board, list(bag), move["rack"], [], 0, alpha, beta))
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

        random_rack = self_rack + bag[:needed_letters]

        bag = bag[needed_letters:]

    else:
        random_rack = self_rack + bag

    next_moves = brie_search(board, random_rack, M)

    for move in next_moves:

        clean_board = copy.deepcopy(board)

        score = move["score"]

        move_score = accu + score

        word = move["word"]

        if word != "N/A":
            if move["direction"] == "horizontal":
                for i in range(len(word)):
                    clean_board[move["Y"]][move["X"]+i] = word[i]
            else:
                for i in range(len(word)):
                    clean_board[move["Y"]+i][move["X"]] = word[i]

            eval = look_opponent_turn(clean_board, bag, move["rack"], opp_rack, move_score, alpha, beta)
        else:
            eval = move_score

        if eval > max_future_score:
            max_future_score = eval

        # alpha = max(alpha, move_score)
        #
        # if beta <= alpha:
        #     break

    return max_future_score


def look_opponent_turn(board, bag, self_rack, opp_rack, accu, alpha, beta):

    #needs to take randomly from Bag

    global M, O, R, N

    #the value of a move is its score + future values
    needed_letters = 7 - len(opp_rack)

    min_future_score = float('inf')

    #the value of a move is its score + future values
    if len(bag) >= needed_letters:

        print(opp_rack)
        print(bag)

        random_rack = opp_rack + bag[:needed_letters]

        bag = bag[needed_letters:]

    else:
        random_rack = opp_rack + bag

    next_moves = brie_search(board, random_rack, O)

    for move in next_moves:

        clean_board = copy.deepcopy(board)

        score = move["score"]

        move_score = accu - score

        word = move["word"]

        if word != "N/A":
            if move["direction"] == "horizontal":
                for i in range(len(word)):
                    clean_board[move["Y"]][move["X"]+i] = word[i]
            else:
                for i in range(len(word)):
                    clean_board[move["Y"]+i][move["X"]] = word[i]

            eval = look_self_turn(clean_board, bag, self_rack, move["rack"], move_score, alpha, beta)
        else:
            eval = move_score

        if eval < min_future_score:
            min_future_score = eval
        # beta = min(beta, move_score)
        #
        # if beta <= alpha:
        #     break

    return min_future_score
