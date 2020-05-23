import random
import copy

from tree_search import brie_search

def look_ahead(board, rack, other_rack, bag):

    #number of moves considered for player
    M = 2
    #number of moves for opponent
    O = 2
    #number of racks guessed
    R = 5
    #number of turns in
    N = 2

    unknown_tiles = other_rack + bag

    best_move = {
                "score" : 0,
                "word" : "N/A",
                "heuristic" : -9999999999
            }


    next_moves = brie_search(board, rack, M)

    for move in next_moves:
        #get future value for each move


        look_self_turn(board,rack, unknown_tiles, 0, 0)

        if score - opponent_score > best_move["heuristic"]:
            best_move = { "score" : score, "word" : word, "X" :move["X"], "Y" : move["Y"], "direction" : move["direction"], "heuristic" : score - opponent_score}


        print(best_move["heuristic"])
        return best_move





def look_self_turn(board,rack, bag, level, heuristic):
    #needs to take randomly from Bag

    #the value of a move is its score + future values
    try:

        future_scores = 0

        for iterations in range(R):
            random_rack = random.sample(bag, 7)

            next_moves = brie_search(board, rack, M)

            for move in next_moves:
                clean_board = copy.deepcopy(board)

                score = move["score"]

                future_score += score

                word = move["word"]

                if word != "N/A":
                    if move["direction"] == "horizontal":
                        for i in range(len(word)):
                            clean_board[move["Y"]][move["X"]+i] = word[i]
                    else:
                        for i in range(len(word)):
                            clean_board[move["Y"]+i][move["X"]] = word[i]

                if level != N:
                    future_scores += look_opponent_turn(clean_board, rack, bag, level + 1, heuristic + score)

        return future_scores/ (M*R)
    except:
        random_rack = unknown_tiles

        next_moves = brie_search(board, rack, M)

        future_scores = 0

        for move in next_moves:
            clean_board = copy.deepcopy(board)

            score = move["score"]

            future_score += score

            word = move["word"]

            if word != "N/A":
                if move["direction"] == "horizontal":
                    for i in range(len(word)):
                        clean_board[move["Y"]][move["X"]+i] = word[i]
                else:
                    for i in range(len(word)):
                        clean_board[move["Y"]+i][move["X"]] = word[i]

        return future_scores/M






def look_opponent_turn(board, rack, bag, level):
    #needs to take randomly from Bag

    #the value of a move is its score + future values
    try:

        future_scores = 0

        for iterations in range(R):
            random_rack = random.sample(bag, 7)

            next_moves = brie_search(board, rack, M)

            for move in next_moves:
                clean_board = copy.deepcopy(board)

                score = move["score"]

                future_score -= score

                word = move["word"]

                if word != "N/A":
                    if move["direction"] == "horizontal":
                        for i in range(len(word)):
                            clean_board[move["Y"]][move["X"]+i] = word[i]
                    else:
                        for i in range(len(word)):
                            clean_board[move["Y"]+i][move["X"]] = word[i]

                if level != N:
                    future_scores += look_opponent_turn(clean_board, rack, bag, level + 1, heuristic + score)

        return future_scores / (M*R)
    except:
        random_rack = unknown_tiles

        next_moves = brie_search(board, rack, M)

        future_scores = 0

        for move in next_moves:
            clean_board = copy.deepcopy(board)

            score = move["score"]

            future_score -= score

            word = move["word"]

            if word != "N/A":
                if move["direction"] == "horizontal":
                    for i in range(len(word)):
                        clean_board[move["Y"]][move["X"]+i] = word[i]
                else:
                    for i in range(len(word)):
                        clean_board[move["Y"]+i][move["X"]] = word[i]

        return future_scores/M

        #average_score
