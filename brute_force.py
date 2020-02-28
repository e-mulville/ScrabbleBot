import copy

dictionary = open("dic.txt", "r")
clean_dictionary = []

for word in dictionary:
    clean_dictionary.append(word[:-1])

dictionary.close()

not_letters = ["   ", " * ", "TLS", "TWS", "DLS", "DWS"]


def BruteForce(board, rack):

    rack = [ rack.rack[i].get_letter() for i in range(len(rack.rack)) ]

    clean_board = copy.deepcopy(board.board)


    best_move = {
        "word" : "N/A",
        "score" : 0,
        "X" : 0,
        "Y" : 1,
        "direction" : "N/A"
    }
    for row_number, row in enumerate(clean_board):
        for column_number, tile in enumerate(row):


            word_playable = False
            tiles_available = len(rack)

            while(tiles_available != 0):
                template = []
                tiles = 0
                bingo = 0
                position = 0
                empty_space = False #there is an empty space
                valid_move = False #it could be placed there
                while(True):
                    try:
                        if clean_board[row_number][column_number+position] in not_letters:
                            empty_space = True

                            if tiles == tiles_available:
                                if tiles == 7:
                                    bingo = 1
                                break

                            template.append(clean_board[row_number][column_number+position])
                            tiles += 1
                            if clean_board[row_number][column_number+position] == " * ":
                                valid_move = True
                        else:
                            template.append(clean_board[row_number][column_number+position])
                            valid_move = True


                        #can be placed at the end of a vertical word
                        if row_number != 0:
                            if clean_board[row_number-1][column_number+position] not in not_letters:
                                valid_move = True #floating word

                        if row_number != 14:
                            if clean_board[row_number+1][column_number+position] not in not_letters:
                                valid_move = True

                        position += 1


                    except:
                        break


                #use template and see if a word will fit


                if valid_move == True and empty_space == True:
                    for word in clean_dictionary:
                        if len(word) == len(template):
                            if is_valid_word(template, word):
                                if word_has_available_tiles(rack,template,word):
                                    valid_position = is_valid_position(word, clean_board, "horizontal", column_number, row_number)
                                    if valid_position != False:
                                        if valid_position > best_move["score"]:
                                                best_move["score"] = valid_position + 50*bingo
                                                best_move["word"] = word
                                                best_move["X"] = column_number
                                                best_move["Y"] = row_number
                                                best_move["direction"] = "horizontal"

                tiles_available -= 1


            tiles_available = len(rack)
            while(tiles_available != 0):

                template = []
                tiles = 0
                bingo = 0
                position = 0
                empty_space = False #there is an empty space
                valid_move = False #it could be placed there

                while(True):
                    try:
                        if clean_board[row_number+position][column_number] in not_letters:
                            empty_space = True
                            if tiles == tiles_available:
                                if tiles == 7:
                                    bingo = 1
                                break
                            template.append(clean_board[row_number+position][column_number])
                            tiles += 1
                            if clean_board[row_number+position][column_number] == " * ":
                                valid_move = True
                        else:
                            template.append(clean_board[row_number+position][column_number])
                            valid_move = True

                        #can be placed at the end of a horizontal word
                        if column_number != 0:
                            if clean_board[row_number+position][column_number-1] not in not_letters:
                                valid_move = True

                        if column_number != 14:
                            if clean_board[row_number+position][column_number+1] not in not_letters:
                                valid_move = True

                        position += 1
                    except:
                        break


                #use template and see if a word will fit
                if valid_move == True and empty_space == True:
                    for word in clean_dictionary:
                        if len(word) == len(template):
                            if is_valid_word(template, word):
                                if word_has_available_tiles(rack,template,word):
                                    valid_position = is_valid_position(word, clean_board, "vertical", column_number, row_number)
                                    if valid_position != False:
                                        if valid_position > best_move["score"]:
                                                best_move["score"] = valid_position + 50*bingo
                                                best_move["word"] = word
                                                best_move["X"] = column_number
                                                best_move["Y"] = row_number
                                                best_move["direction"] = "vertical"

                tiles_available -= 1




    return best_move

def is_valid_position(word, board, direction, x, y):
    #checks if a word can be played there without breaking any rules
    score_sum = 0
    if direction == "horizontal":

        try:
            if board[y][x-1] not in not_letters:
                return False
        except:
            pass

        for i in range(len(word)):
            count = 1
            new_word = [word[i]]
            new_word_y = y
            while(y-count >= 0):
                try:
                    if board[y-count][x+i] not in not_letters:
                        new_word.insert(0,board[y-count][x+i])
                        new_word_y = y - count
                    else:
                        break
                    count += 1
                except:
                    break

            count = 1
            while(True):
                try:
                    if board[y+count][x+i] not in not_letters:
                        new_word.append(board[y+count][x+i])
                    else:
                        break

                    count += 1
                except:
                    break

            if len(new_word) > 1:
                str = ""
                if not is_word_in_dictionary(str.join(new_word)):
                    return False
                elif board[y][x+i] in not_letters:
                    new_word_x = x+i
                    score_sum += score_word(board, str.join(new_word), "vertical", new_word_x, new_word_y) ##why does this not do stuff
        return score_sum + score_word(board, word, "horizontal", x, y)

    elif direction == "vertical":
        try:
            if board[y-1][x] not in not_letters:
                return False
        except:
            pass

        for i in range(len(word)):
            count = 1
            new_word = [word[i]]
            new_word_x = x
            while(x-count >= 0):
                try:
                    if board[y+i][x-count] not in not_letters:
                        new_word.insert(0,board[y+i][x-count])
                        new_word_x = x - count
                    else:
                        break
                    count += 1
                except:
                    break

            count = 1
            while(True):
                try:
                    if board[y+i][x+count] not in not_letters:
                        new_word.append(board[y+i][x+count])
                    else:
                        break
                    count += 1
                except:
                    break

            if len(new_word) > 1:
                str = ""
                if not is_word_in_dictionary(str.join(new_word)):
                    return False
                elif board[y+i][x] in not_letters:
                    new_word_y = y+i
                    score_sum += score_word(board, str.join(new_word), "horizontal", new_word_x, new_word_y) ##why does this not do stuff
        return score_sum + score_word(board, word, "vertical", x, y)


def word_has_available_tiles(rack,template,word):
    #checks if a word can be made from the tiles in the rack
    copy_rack = copy.deepcopy(rack)
    for index, letter in enumerate(template):
        if letter in not_letters:
            if word[index] in copy_rack:
                copy_rack.remove(word[index])
            elif "#" in copy_rack:
                copy_rack.remove("#")
            else:
                return False

    return True


def is_valid_word(template, word):
    #compares a word to a template to see if it would fit
    split_word = [char for char in word]
    for index, letter in enumerate(template):
        if letter not in not_letters:
            if split_word[index] != letter:
                return False
    return True

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
