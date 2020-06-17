from random import shuffle
from skeleton import find_best_moves
import time



"""
Scrabble Game
Classes:
Tile - keeps track of the tile letter and value
Rack - keeps track of the tiles in a player's letter rack
Bag - keeps track of the remaining tiles in the bag
Word - checks the validity of a word and its placement
Board - keeps track of the tiles' location on the board
"""
#Keeps track of the score-worth of each letter-tile.

total_time = 0
wins = (0,0)
games = 0

start_time = time.time()

# scores_per_turn = {"1": {}, "2" : {}}
scores_per_turn = []
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


class Bag:
    """
    Creates the bag of all tiles that will be available during the game. Contains 98 letters and two blank tiles.
    Takes no arguments to initialize.
    """
    def __init__(self):
        #Creates the bag full of game tiles, and calls the initialize_bag() method, which adds the default 100 tiles to the bag.
        #Takes no arguments.
        self.bag = []
        self.initialize_bag()

    def add_to_bag(self, tile, quantity):
        #Adds a certain quantity of a certain tile to the bag. Takes a tile and an integer quantity as arguments.
        for i in range(quantity):
            self.bag.append(tile)

    def initialize_bag(self):
        #Adds the intiial 100 tiles to the bag.
        global LETTER_VALUES
        self.add_to_bag("A", 9)
        self.add_to_bag("B", 2)
        self.add_to_bag("C", 2)
        self.add_to_bag("D", 4)
        self.add_to_bag("E", 12)
        self.add_to_bag("F", 2)
        self.add_to_bag("G", 3)
        self.add_to_bag("H", 2)
        self.add_to_bag("I", 9)
        self.add_to_bag("J", 9)
        self.add_to_bag("K", 1)
        self.add_to_bag("L", 4)
        self.add_to_bag("M", 2)
        self.add_to_bag("N", 6)
        self.add_to_bag("O", 8)
        self.add_to_bag("P", 2)
        self.add_to_bag("Q", 1)
        self.add_to_bag("R", 6)
        self.add_to_bag("S", 4)
        self.add_to_bag("T", 6)
        self.add_to_bag("U", 4)
        self.add_to_bag("V", 2)
        self.add_to_bag("W", 2)
        self.add_to_bag("X", 1)
        self.add_to_bag("Y", 2)
        self.add_to_bag("Z", 1)
        self.add_to_bag("#", 2)
        shuffle(self.bag)

    def take_from_bag(self):
        #Removes a tile from the bag and returns it to the user. This is used for replenishing the rack.
        return self.bag.pop()

    def get_remaining_tiles(self):
        #Returns the number of tiles left in the bag.
        return len(self.bag)

class Rack:
    """
    Creates each player's 'dock', or 'hand'. Allows players to add, remove and replenish the number of tiles in their hand.
    """
    def __init__(self, bag):
        #Initializes the player's rack/hand. Takes the bag from which the racks tiles will come as an argument.
        self.rack = []
        self.bag = bag
        self.initialize()

    def add_to_rack(self):
        #Takes a tile from the bag and adds it to the player's rack.
        self.rack.append(self.bag.take_from_bag())

    def initialize(self):
        #Adds the initial 7 tiles to the player's hand.
        for i in range(7):
            self.add_to_rack()

    def remove_from_rack(self, tile):
        #Removes a tile from the rack (for example, when a tile is being played).
        self.rack.remove(tile)

    def get_rack_length(self):
        #Returns the number of tiles left in the rack.
        return len(self.rack)

    def replenish_rack(self):
        #Adds tiles to the rack after a turn such that the rack will have 7 tiles (assuming a proper number of tiles in the bag).
        while self.get_rack_length() < 7 and self.bag.get_remaining_tiles() > 0:
            self.add_to_rack()

class Player:
    """
    Creates an instance of a player. Initializes the player's rack, and allows you to set/get a player name.
    """
    def __init__(self, bag):
        #Intializes a player instance. Creates the player's rack by creating an instance of that class.
        #Takes the bag as an argument, in order to create the rack.
        self.name = ""
        self.rack = Rack(bag)
        self.score = 0

    def set_name(self, name):
        #Sets the player's name.
        self.name = name

    def get_name(self):
        #Gets the player's name.
        return self.name

    def get_rack(self):
        return self.rack

    def increase_score(self, increase):
        #Increases the player's score by a certain amount. Takes the increase (int) as an argument and adds it to the score.
        self.score += increase

    def get_score(self):
        #Returns the player's score
        return self.score

class Board:
    """
    Creates the scrabble board.
    """
    def __init__(self):
        #Creates a 2-dimensional array that will serve as the board, as well as adds in the premium squares.
        self.board = [["   " for i in range(15)] for j in range(15)]
        self.add_premium_squares()
        self.board[7][7] = " * "

    def get_board_string(self):
        #Returns the board in string form.
        board_str = "   |  " + "  |  ".join(str(item) for item in range(10)) + "  | " + "  | ".join(str(item) for item in range(10, 15)) + " |"
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        board = list(self.board)
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

    def add_premium_squares(self):
        #Adds all of the premium squares that influence the word's score.
        TRIPLE_WORD_SCORE = ((0,0), (7, 0), (14,0), (0, 7), (14, 7), (0, 14), (7, 14), (14,14))
        DOUBLE_WORD_SCORE = ((1,1), (2,2), (3,3), (4,4), (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3), (10, 4), (13,13), (12, 12), (11,11), (10,10))
        TRIPLE_LETTER_SCORE = ((1,5), (1, 9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13, 5), (13,9))
        DOUBLE_LETTER_SCORE = ((0, 3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8, 12), (11,0), (11,7), (11,14), (12,6), (12,8), (14, 3), (14, 11))

        for coordinate in TRIPLE_WORD_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "TWS"
        for coordinate in TRIPLE_LETTER_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "TLS"
        for coordinate in DOUBLE_WORD_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "DWS"
        for coordinate in DOUBLE_LETTER_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "DLS"

    def place_word(self, word, location, direction, player):
        #Allows you to play words, assuming that they have already been confirmed as valid.
        global premium_spots
        premium_spots = []
        direction.lower()
        word = word.upper()

        #Places the word going rightwards
        if direction.lower() == "right":
            for i in range(len(word)):
                if self.board[location[0]][location[1]+i] != "   ":
                    premium_spots.append((word[i], self.board[location[0]][location[1]+i]))
                self.board[location[0]][location[1]+i] = word[i]

        #Places the word going downwards
        elif direction.lower() == "down":
            for i in range(len(word)):
                if self.board[location[0]+i][location[1]] != "   ":
                    premium_spots.append((word[i], self.board[location[0]+i][location[1]]))
                self.board[location[0]+i][location[1]] = word[i]


        #Removes tiles from player's rack and replaces them with tiles from the bag.
        for letter in word:
            removed = False
            for tile in player.rack.rack:
                if tile == letter:
                    player.rack.remove_from_rack(tile)
                    removed = True
            if removed == False:
                for tile in player.rack.rack:
                    if tile == "#":
                        player.rack.remove_from_rack(tile)



        player.rack.replenish_rack()

    def get_board(self):
        #Returns the 2-dimensional board array.
        return self.board

class Word:
    def __init__(self, word, location, player, direction, board):
        self.word = word.upper()
        self.location = location
        self.player = player
        self.direction = direction.lower()
        self.board = board

    def set_word(self, word):
        self.word = word

    def set_location(self, location):
        self.location = location

    def set_direction(self, direction):
        self.direction = direction

    def get_word(self):
        return self.word

def turn(player, board, bag):
    #Begins a turn, by displaying the current board, getting the information to play a turn, and creates a recursive loop to allow the next person to play.
    global round_number, players, skipped_turns,turns, scores_per_turn

    #If the number of skipped turns is less than 6 and a row, and there are either tiles in the bag, or no players have run out of tiles, play the turn.
    #Otherwise, end the game.
    if (skipped_turns < 6) and not (player.rack.get_rack_length() == 0 and bag.get_remaining_tiles() == 0):
        #print("Skipped turns: " + str(skipped_turns))

        #Displays whose turn it is, the current board, and the player's rack.
        #print("\nRound " + str(round_number) + ": " + player.get_name() + "'s turn \n")
        #print(board.get_board_string())
        #print("\n" + player.get_name() + "'s Letter Rack: " + player.get_rack_str())

        word_score = 0
        valid_moves = 0

        bestmove = {}

        if 1 == 1:
            if players.index(player) != (len(players)-1):
                opponent = players[players.index(player)+1]
            else:
                opponent = players[0]

            best_move = find_best_moves(board, player.rack, opponent.rack, bag, player)
            turns += 1

            word_score = best_move["score"]
            word_to_play = best_move["word"]
            if word_to_play == "N/A":
                word_to_play = ""
                location = [1, 1]
                direction = "right"
            else:
                location = [best_move["Y"], best_move["X"]]
                if best_move["direction"] == "horizontal":
                    direction = "right"
                else:
                    direction = "down"
            word = Word(word_to_play, location, player, direction, board.get_board())

        else:
            #Gets information in order to play a word.
            word_to_play = input("Word to play: ")
            location = []
            col = input("Column number: ")
            row = input("Row number: ")
            if (col == "" or row == "") or (col not in [str(x) for x in range(15)] or row not in [str(x) for x in range(15)]):
                location = [-1, -1]
            else:
                location = [int(row), int(col)]
            direction = input("Direction of word (right or down): ")

            word = Word(word_to_play, location, player, direction, board.get_board())

        #If the first word throws an error, creates a recursive loop until the information is given correctly.

        #If the user has confirmed that they would like to skip their turn, skip it.
        #Otherwise, plays the correct word and prints the board.
        if word.get_word() == "":
            print("Your turn has been skipped.")
            skipped_turns += 1
        else:



            board.place_word(word_to_play, location, direction, player)
            #
            # while len(scores_per_turn) < round_number:
            #     scores_per_turn.append((0,0))

            #
            # if round_number == 1:
            #     if player.name == "Bot1":
            #         for letter in best_move["used"]:
            #             if letter in scores_per_turn["1"]:
            #                 scores_per_turn["1"][letter] += 1
            #             else:
            #                 scores_per_turn["1"][letter] = 1
            #     elif player.name == "Bot2":
            #         for letter in best_move["used"]:
            #             if letter in scores_per_turn["2"]:
            #                 scores_per_turn["2"][letter] += 1
            #             else:
            #                 scores_per_turn["2"][letter] = 1

            # if player.name == "Bot1":
            #     (bot1, bot2) = scores_per_turn[round_number - 1]
            #     scores_per_turn[round_number - 1] = (bot1 + valid_moves, bot2)
            # elif player.name == "Bot2":
            #     (bot1, bot2) = scores_per_turn[round_number - 1]
            #     scores_per_turn[round_number - 1] = (bot1, bot2 + valid_moves)
            player.increase_score(word_score)
            skipped_turns = 0

        #Prints the current player's score
        #print("\n" + player.get_name() + "'s score is: " + str(player.get_score()))

        #Gets the next player.
        if players.index(player) != (len(players)-1):
            player = players[players.index(player)+1]
        else:
            player = players[0]
            round_number += 1

        #Recursively calls the function in order to play the next turn.
        turn(player, board, bag)

    #If the number of skipped turns is over 6 or the bag has both run out of tiles and a player is out of tiles, end the game.
    else:
        end_game()

def start_game():


    #Begins the game and calls the turn function.
    global round_number, players, skipped_turns, start_time, wins, turns, games
    board = Board()
    bag = Bag()
    #Asks the player for the number of players.
    num_of_players = 2
    turns = 0

    #Welcomes players to the game and allows players to choose their name.
    print("\nWelcome to Scrabble! Please enter the names of the players below.")
    Bot1 = Player(bag)
    Bot1.set_name("Bot1")

    Bot2 = Player(bag)
    Bot2.set_name("Bot2")

    players = [Bot1, Bot2]

    #Sets the default value of global variables.
    games += 1
    round_number = 1
    skipped_turns = 0
    current_player = players[0]
    turn(current_player, board, bag)

def end_game():
    #Forces the game to end when the bag runs out of tiles.
    global players, start_time, turns, wins, games, scores_per_turn

    a = time.time() - start_time
    print(a/games)
    print("For game")
    print(a/(turns*games))
    print("Per go")
    highest_score = 0
    winning_player = ""
    for player in players:
        print(player.get_name())
        print(player.get_score())
        if player.get_score() > highest_score:
            highest_score = player.get_score()
            winning_player = player.get_name()

    if winning_player == "Bot1":
        (bot_1, bot_2) = wins
        wins = (bot_1 + 1, bot_2)
    else:
        (bot_1, bot_2) = wins
        wins = (bot_1, bot_2 + 1)
    # #
    # for player in scores_per_turn:
    #     print(player)
    #     for letter in scores_per_turn[player]:
    #         print( (letter, scores_per_turn[player][letter]/games))
    total = 0
    # for turn in scores_per_turn:
    #     (a,b) = turn
    #     total += a + b
    #     print( ( a /games, b / games))
    # print( total /(len(scores_per_turn)* games * 2))

    print("The game is over! " + winning_player + ", you have won!")
    print("Score is:" + str(wins))


while(True):
    start_game()
