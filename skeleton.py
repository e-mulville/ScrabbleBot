import copy
from brute_force import BruteForce
from tree_search import brie_search
from look_ahead import look_ahead
from exhaustive_endgame import end_game_search

not_letters = ["   ", " * ", "TLS", "TWS", "DLS", "DWS"]

def find_best_moves(board, rack, other_rack, bag, player):

    rack = rack.rack
    other_rack = other_rack.rack
    bag = bag.bag
    board = board.board

    if player.name == "Bot1":
        #best_move = BruteForce(board, rack)
        #best_move = look_ahead(board, rack, other_rack, bag)
        best_move = brie_search(board,rack,1)[0]
    elif player.name == "Bot2":
        #best_move = BruteForce(board, rack)
        #best_move = look_ahead(board, rack, other_rack, bag)
        #best_move = brie_search(board,rack,1)[0]
        best_move = end_game_search(board, rack, other_rack, bag)

    return best_move
