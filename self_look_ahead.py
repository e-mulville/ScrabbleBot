import random
import copy

from tree_search import brie_search

def self_look_ahead(board, rack, other_rack, bag):

    global M, O, R, N

    #number of moves considered for player
    M = 10
    #number of moves for opponent
    O = 1
    #number of racks guessed
    R = 1
    #number of turns in
    N = 4

    unknown_tiles = other_rack + bag

    best_move = {
                "score" : 0,
                "word" : "N/A",
                "heuristic" : -9999999999
            }

    next_moves = brie_search(board, rack, M)

    randomness = max(len(unknown_tiles) - 7, 1)

    for move in next_moves:
        #get future value for each move

        if move["word"] != "N/A":

            word = move["word"]

            clean_board = copy.deepcopy(board)

            if move["direction"] == "horizontal":
                for i in range(len(word)):
                    clean_board[move["Y"]][move["X"]+i] = word[i]
            else:
                for i in range(len(word)):
                    clean_board[move["Y"]+i][move["X"]] = word[i]

            future_score = 0

            for iterations in range(R):

                random.shuffle(unknown_tiles)


                alpha = float('inf')
                beta = float('-inf')

                future_score += move["score"] + (look_self_turn(clean_board, unknown_tiles, N, move["rack"], [], 0, alpha, beta) / randomness)

            if (future_score/R) > best_move["heuristic"]:
                best_move = { "score" : move["score"], "word" : move["word"], "X" : move["X"], "Y" : move["Y"], "direction" : move["direction"], "heuristic" : future_score/R}

    return best_move



def look_self_turn(board, bag, level, self_rack, opp_rack, accu, alpha, beta):
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

    next_moves = brie_search(board, random_rack, 1)

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

        if level > 1:
            eval = look_self_turn(clean_board, bag, level - 1, move["rack"], opp_rack, move_score, alpha, beta)
        else:
            eval = move_score

        if eval > max_future_score:
            max_future_score = eval

        # alpha = max(alpha, move_score)
        #
        # if beta <= alpha:
        #     break

    return max_future_score
