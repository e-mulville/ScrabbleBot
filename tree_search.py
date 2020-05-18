import json
import time
import itertools
import copy

not_letters = ["   ", " * ", "TLS", "TWS", "DLS", "DWS"]

def brie_search(board, rack):

    start_time = time.time()

    print("Opening")
    with open('briedata.txt') as json_file:
        data = json.load(json_file)
        pass
    print("--- %s seconds ---" % (time.time() - start_time))

    best_moves = []

    for n in range(2):
        best_moves.append({
            "score" : 0,
            "word" : "N/A"
        })


    for row_number, row in enumerate(board):
        for column_number, tile in enumerate(row):
            if board[row_number][column_number] not in not_letters:
                #horizontal
                if board[row_number][column_number-1] not in not_letters:
                    pass
                    #only take a first letter
                else:
                    i = 1
                    word = board[row_number][column_number]
                    while(True):
                        if board[row_number][column_number+i] not in not_letters:
                            word = word + board[row_number][column_number+i]
                            i += 1
                        else:
                            break

                    print(word)
                    node = data["children"][word[-1]]

                    moves = find_moves_horizontal(node, word, rack, board, row_number, column_number)

                    for move in moves:

                        (word, rack, row, column) = move

                        score = score_move(move, board, "horizontal")
                        if score > best_moves[0]["score"]:
                            for i in range(len(best_moves)):
                                if score < best_moves[i]["score"]:
                                    best_moves.insert(i,{ "score" : score, "word" : word, "X" : column, "Y" : row, "direction" : "horizontal"})
                                    del best_moves[0]
                                    break
                                if i == len(best_moves) - 1:
                                    best_moves.insert(i+1,{ "score" : score, "word" : word, "X" : column, "Y" : row, "direction" :"horizontal"})
                                    del best_moves[0]



                #vertical
                if board[row_number - 1][column_number] not in not_letters:
                    pass
                else:
                    i = 1
                    word = board[row_number][column_number]
                    while(True):
                        if board[row_number][column_number+i] not in not_letters:
                            word = word + board[row_number][column_number+i]
                            i += 1
                        else:
                            break

                    node = data["children"][word[-1]]
                    #moves = find_words(node, word, rack)




            elif board[row_number][column_number] == " * ":
                # for tile in rack:
                #     node = data["children"][tile]
                #blank space
                word = ""
                if word:
                    node = data["children"][word[-1]]
                else:
                    node = data


                moves = find_moves_horizontal(node, word, rack, board, row_number, column_number)

                for move in moves:

                    (word, rack, row, column) = move

                    score = score_move(move, board, "horizontal")
                    if score > best_moves[0]["score"]:
                        for i in range(len(best_moves)):
                            if score < best_moves[i]["score"]:
                                best_moves.insert(i,{ "score" : score, "word" : word, "X" : column, "Y" : row, "direction" : "horizontal"})
                                del best_moves[0]
                                break
                            if i == len(best_moves) - 1:
                                best_moves.insert(i+1,{ "score" : score, "word" : word, "X" : column, "Y" : row, "direction" :"horizontal"})
                                del best_moves[0]

    return best_moves[-1]



def find_moves_horizontal(node, word, rack, board, row, column):

    if word:
        i = 1
        for letter in word[-2::-1]:
            i += 1
            node = node["children"][letter]
    else:
        i = 0

    word_list = []
    #there is always at least one space
    #backwards
    backwards(node, word, rack, word_list, board, row, column-i)
    #forwards
    if "$" in node["children"]:
        forwards()

    return word_list



def backwards(node, word, rack, word_list, board, row, column):
    if board[row][column] in not_letters:

        if "$" in node["children"]:
            forwards(node["children"]["$"], word, rack, word_list, board, row, column + len(word))

        if node["end"] == True:
            word_list.append((word, rack, row, column))

        for letter in rack:
            if letter == "#":
                for child in node["children"]:
                    if child != "$":
                        new_word = child + word
                        copy_rack = copy.deepcopy(rack)
                        copy_rack.remove(letter)
                        backwards(node["children"][child], new_word, copy_rack, word_list, board, row, column-1)
            else:
                if letter in node["children"]:
                    new_word = letter + word
                    copy_rack = copy.deepcopy(rack)
                    copy_rack.remove(letter)
                    backwards(node["children"][letter], new_word, copy_rack, word_list, board, row, column-1)


        #forwards
    else:
        letter = board[row][column]
        if letter in node["children"]:
            new_word = letter + word
            backwards(node["children"][letter], new_word, rack, word_list, board, row, column-1)



    pass

def forwards(node, word, rack, word_list, board, row, column):
    if board[row][column] in not_letters:

        if node["end"] == True:
            word_list.append((word, rack, row, column-len(word)))

        for letter in rack:
            if letter == "#":
                for child in node["children"]:
                    if child != "$":
                        new_word = word + child
                        copy_rack = copy.deepcopy(rack)
                        copy_rack.remove(letter)
                        forwards(node["children"][child], new_word, copy_rack, word_list, board, row, column+1)
            else:
                if letter in node["children"]:
                    new_word = word + letter
                    copy_rack = copy.deepcopy(rack)
                    copy_rack.remove(letter)
                    forwards(node["children"][letter], new_word, copy_rack, word_list, board, row, column+1)


        #forwards
    else:
        letter = board[row][column]
        if letter in node["children"]:
            new_word = letter + word
            forwards(node["children"][letter], new_word, copy_rack, word_list, board, row, column+1)


def score_move(move, board, direction):
    (word, rack, row, column) = move

    score_sum = 0
    if direction == "horizontal":

        try:
            if board[row][column-1] not in not_letters:
                return False
        except:
            pass

        for i in range(len(word)):
            count = 1
            new_word = [word[i]]
            new_word_y = row
            while(row-count >= 0):
                try:
                    if board[row-count][column+i] not in not_letters:
                        new_word.insert(0,board[row-count][column+i])
                        new_word_y = row - count
                    else:
                        break
                    count += 1
                except:
                    break

            count = 1
            while(True):
                try:
                    if board[row+count][column+i] not in not_letters:
                        new_word.append(board[row+count][column+i])
                    else:
                        break

                    count += 1
                except:
                    break

            if len(new_word) > 1:
                str = ""
                if not is_word_in_dictionary(str.join(new_word)):
                    return False
                elif board[row][column+i] in not_letters:
                    new_word_x = column+i
                    score_sum += score_word(board, str.join(new_word), "vertical", new_word_x, new_word_y) ##why does this not do stuff
        return score_sum + score_word(board, word, "horizontal", column, row)

    elif direction == "vertical":
        try:
            if board[row-1][column] not in not_letters:
                return False
        except:
            pass

        for i in range(len(word)):
            count = 1
            new_word = [word[i]]
            new_word_x = column
            while(column-count >= 0):
                try:
                    if board[row+i][column-count] not in not_letters:
                        new_word.insert(0,board[row+i][column-count])
                        new_word_x = column - count
                    else:
                        break
                    count += 1
                except:
                    break

            count = 1
            while(True):
                try:
                    if board[row+i][column+count] not in not_letters:
                        new_word.append(board[row+i][column+count])
                    else:
                        break
                    count += 1
                except:
                    break

            if len(new_word) > 1:
                str = ""
                if not is_word_in_dictionary(str.join(new_word)):
                    return False
                elif board[row+i][column] in not_letters:
                    new_word_y = row+i
                    score_sum += score_word(board, str.join(new_word), "horizontal", new_word_x, new_word_y) ##why does this not do stuff
        return score_sum + score_word(board, word, "vertical", column, row)


def score_word(board, word, direction, column, row):
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
            board_char = board[row][column+index]
        elif direction == "vertical":
            board_char = board[row+index][column]

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
