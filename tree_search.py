import json
import time
import itertools
import copy

not_letters = ["   ", " * ", "TLS", "TWS", "DLS", "DWS"]

start_time = time.time()
print("Opening")
with open('briedata.txt') as json_file:
    data = json.load(json_file)
    pass
print("--- %s seconds ---" % (time.time() - start_time))

def brie_search(board, rack, k):

    best_moves = []


    for n in range(k):
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
                        if column_number + i <= 14:
                            if board[row_number][column_number+i] not in not_letters:
                                word = word + board[row_number][column_number+i]
                                i += 1
                            else:
                                break
                        else:
                            break

                    node = data["children"][word[-1]]


                    moves = find_moves_horizontal(node, word, rack, board, row_number, column_number)

                    for move in moves:



                        (word, move_rack, move_row, move_column) = move

                        if len(move_rack) == len(rack):
                            continue

                        score = score_move(move, board, "horizontal", data)

                        if len(rack) - len(move_rack) == 7:
                            score += 50

                        if score > best_moves[0]["score"]:
                            for i in range(len(best_moves)):
                                if score < best_moves[i]["score"]:
                                    best_moves.insert(i,{ "score" : score, "word" : word, "X" : move_column, "Y" : move_row, "direction" : "horizontal"})
                                    del best_moves[0]
                                    break
                                if i == len(best_moves) - 1:
                                    best_moves.insert(i+1,{ "score" : score, "word" : word, "X" : move_column, "Y" : move_row, "direction" :"horizontal"})
                                    del best_moves[0]



                #vertical
                if board[row_number - 1][column_number] not in not_letters:
                    pass
                else:
                    i = 1
                    word = board[row_number][column_number]
                    while(True):
                        if row_number + i <= 14:
                            if board[row_number + i][column_number] not in not_letters:
                                word = word + board[row_number+i][column_number]
                                i += 1
                            else:
                                break
                        else:
                            break


                    node = data["children"][word[-1]]
                    #moves = find_words(node, word, rack)


                    moves = find_moves_vertical(node, word, rack, board, row_number, column_number)


                    for move in moves:

                        (word, move_rack, move_row, move_column) = move


                        if len(move_rack) == len(rack):
                            continue

                        score = score_move(move, board, "vertical", data)

                        if len(rack) - len(move_rack) == 7:
                            score += 50


                        if score > best_moves[0]["score"]:
                            for i in range(len(best_moves)):
                                if score < best_moves[i]["score"]:
                                    best_moves.insert(i,{ "score" : score, "word" : word, "X" : move_column, "Y" : move_row, "direction" : "vertical"})
                                    del best_moves[0]
                                    break
                                if i == len(best_moves) - 1:
                                    best_moves.insert(i+1,{ "score" : score, "word" : word, "X" : move_column, "Y" : move_row, "direction" :"vertical"})
                                    del best_moves[0]




            elif board[row_number][column_number] == " * ":
                # for tile in rack:
                #     node = data["children"][tile]
                #blank space
                word = ""

                node = data


                moves = find_moves_horizontal(node, word, rack, board, row_number, column_number + 1)

                for move in moves:

                    (word, move_rack, row, column) = move
                    #print(move)

                    score = score_move(move, board, "horizontal", data)

                    if len(rack) - len(move_rack) == 7:
                        score += 50

                    if score > best_moves[0]["score"]:
                        for i in range(len(best_moves)):
                            if score < best_moves[i]["score"]:
                                best_moves.insert(i,{ "score" : score, "word" : word, "X" : column, "Y" : row, "direction" : "horizontal"})
                                del best_moves[0]
                                break
                            if i == len(best_moves) - 1:
                                best_moves.insert(i+1,{ "score" : score, "word" : word, "X" : column, "Y" : row, "direction" :"horizontal"})
                                del best_moves[0]
                    # print(best_moves)
                    # print("~~~~")

    return best_moves



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
    #backwards_horizontal
    if column >= 1:
        backwards_horizontal(node, word, rack, word_list, board, row, column-1)
    elif "$" in node["children"]:
        if column + len(word) + 1 <= 14:
            forwards_horizontal(node["children"]["$"], word, rack, word_list, board, row, column + len(word))
    #forwards_horizontal
    # if "$" in node["children"]:
    #     node = node["children"]["$"]
    #     forwards_horizontal(node, word, rack, word_list, board, row, column + len(word))

    return word_list

def backwards_horizontal(node, word, rack, word_list, board, row, column):
    if board[row][column] in not_letters:

        if "$" in node["children"]:
            if column + len(word) + 1 <= 14:
                forwards_horizontal(node["children"]["$"], word, rack, word_list, board, row, column + 1 + len(word))
            else:
                if node["children"]["$"]["end"] == True:
                    word_list.append((word, rack, row, column + 1))


        if node["end"] == True:
            word_list.append((word, rack, row, column + 1))


        if column >= 1:
            for letter in set(rack):
                if letter == "#":
                    for child in node["children"]:
                        if child != "$":
                            new_word = child + word
                            copy_rack = copy.deepcopy(rack)
                            copy_rack.remove(letter)
                            backwards_horizontal(node["children"][child], new_word, copy_rack, word_list, board, row, column-1)
                else:
                    if letter in node["children"]:
                        new_word = letter + word
                        copy_rack = copy.deepcopy(rack)
                        copy_rack.remove(letter)
                        backwards_horizontal(node["children"][letter], new_word, copy_rack, word_list, board, row, column-1)
        else:
            for letter in set(rack):
                if letter == "#":
                    for child in node["children"]:
                        if child != "$":
                            new_word = child + word
                            copy_rack = copy.deepcopy(rack)
                            copy_rack.remove(letter)
                            new_node = node["children"][child]
                            if "$" in new_node["children"]:
                                if column + len(word) <= 14:
                                    forwards_horizontal(new_node["children"]["$"], new_word, rack, word_list, board, row, column + len(new_word))
                                else:
                                    if node["children"]["$"]["end"] == True:
                                        word_list.append((new_word, rack, row, column))


                else:
                    if letter in node["children"]:
                        new_word = letter + word
                        copy_rack = copy.deepcopy(rack)
                        copy_rack.remove(letter)
                        new_node = node["children"][letter]
                        if "$" in new_node["children"]:
                            if column + len(word) <= 14:
                                forwards_horizontal(new_node["children"]["$"], new_word, rack, word_list, board, row, column + len(new_word))
                            else:
                                if node["children"]["$"]["end"] == True:
                                    word_list.append((new_word, rack, row, column))

        #forwards_horizontal
    else:
        letter = board[row][column]
        if letter in node["children"]:
            new_word = letter + word
            if column >= 1:
                backwards_horizontal(node["children"][letter], new_word, rack, word_list, board, row, column - 1)
            elif "$" in node["children"]:
                if column + len(word) <= 14:
                    forwards_horizontal(node["children"]["$"], new_word, rack, word_list, board, row, column + len(word))
                else:
                    if node["children"]["$"]["end"] == True:
                        word_list.append((new_word, rack, row, column))

def forwards_horizontal(node, word, rack, word_list, board, row, column):
    if board[row][column] in not_letters:

        if node["end"] == True:
            word_list.append((word, rack, row, column-len(word)))


        if column <= 13:
            for letter in set(rack):
                if letter == "#":
                    for child in node["children"]:
                        if child != "$":
                            new_word = word + child
                            copy_rack = copy.deepcopy(rack)
                            copy_rack.remove(letter)
                            forwards_horizontal(node["children"][child], new_word, copy_rack, word_list, board, row, column+1)
                else:
                    if letter in node["children"]:
                        new_word = word + letter
                        copy_rack = copy.deepcopy(rack)
                        copy_rack.remove(letter)
                        forwards_horizontal(node["children"][letter], new_word, copy_rack, word_list, board, row, column+1)
        if column == 14:
            for letter in set(rack):
                if letter == "#":
                    for child in node["children"]:
                        if child != "$":
                            new_word = word + child
                            copy_rack = copy.deepcopy(rack)
                            copy_rack.remove(letter)
                            new_node = node["children"][child]
                            if new_node["end"] == True:
                                word_list.append((new_word, rack, row, column - len(word)))
                else:
                    if letter in node["children"]:
                        new_word = word + letter
                        copy_rack = copy.deepcopy(rack)
                        copy_rack.remove(letter)
                        new_node = node["children"][letter]
                        if new_node["end"] == True:
                            word_list.append((new_word, rack, row, column- len(word)))


        #forwards_horizontal
    else:
        letter = board[row][column]
        if letter in node["children"]:
            new_word = word + letter
            if column <= 13:
                forwards_horizontal(node["children"][letter], new_word, rack, word_list, board, row, column+1)
            else:
                new_node = node["children"][letter]
                if new_node["end"] == True:
                    word_list.append((new_word, rack, row, column -len(word) + 1))


def find_moves_vertical(node, word, rack, board, row, column):

    if word:
        i = 1
        for letter in word[-2::-1]:
            i += 1
            node = node["children"][letter]
    else:
        i = 0

    word_list = []

    #there is always at least one space
    #backwards_horizontal
    if row >= 1:
        backwards_vertical(node, word, rack, word_list, board, row-1, column)
    elif "$" in node["children"]:
        if row + 1 + len(word) <= 14:
            forwards_vertical(node["children"]["$"], word, rack, word_list, board, row + len(word), column)

    #forwards_horizontal
    # if "$" in node["children"]:
    #     node = node["children"]["$"]
    #     forwards_vertical(node, word, rack, word_list, board, row + len(word), column)


    return word_list

def backwards_vertical(node, word, rack, word_list, board, row, column):
    if board[row][column] in not_letters:

        if "$" in node["children"]:
            if row + 1 + len(word) <= 14:
                forwards_vertical(node["children"]["$"], word, rack, word_list, board, row + 1 + len(word), column)
            else:
                if node["children"]["$"]["end"] == True:
                    word_list.append((word, rack, row + 1, column))


        if node["end"] == True:
            word_list.append((word, rack, row + 1, column))

        if row >= 1:
            for letter in set(rack):
                if letter == "#":
                    for child in node["children"]:
                        if child != "$":
                            new_word = child + word
                            copy_rack = copy.deepcopy(rack)
                            copy_rack.remove(letter)
                            backwards_vertical(node["children"][child], new_word, copy_rack, word_list, board, row - 1, column)
                else:
                    if letter in node["children"]:
                        new_word = letter + word
                        copy_rack = copy.deepcopy(rack)
                        copy_rack.remove(letter)
                        backwards_vertical(node["children"][letter], new_word, copy_rack, word_list, board, row - 1, column)
        else:
            for letter in set(rack):
                if letter == "#":
                    for child in node["children"]:
                        if child != "$":
                            new_word = child + word
                            copy_rack = copy.deepcopy(rack)
                            copy_rack.remove(letter)
                            new_node = node["children"][child]
                            if "$" in new_node["children"]:
                                if row + len(word) <= 14:
                                    forwards_vertical(new_node["children"]["$"], new_word, rack, word_list, board, row + len(new_word), column)
                                else:
                                    if node["children"]["$"]["end"] == True:
                                        word_list.append((new_word, rack, row, column))

                else:
                    if letter in node["children"]:
                        new_word = letter + word
                        copy_rack = copy.deepcopy(rack)
                        copy_rack.remove(letter)
                        new_node = node["children"][letter]
                        if "$" in new_node["children"]:
                            if row + len(word) <= 14:
                                forwards_vertical(new_node["children"]["$"], new_word, rack, word_list, board, row + len(new_word), column)
                            else:
                                if node["children"]["$"]["end"] == True:
                                    word_list.append((new_word, rack, row, column))

        #forwards_horizontal
    else:
        letter = board[row][column]
        if letter in node["children"]:
            new_word = letter + word
            if row >= 1:
                backwards_vertical(node["children"][letter], new_word, rack, word_list, board, row - 1, column)
            elif "$" in node["children"]:
                    if row + len(word) <= 14:
                        forwards_vertical(node["children"]["$"], new_word, rack, word_list, board, row + len(word), column)
                    else:
                        if node["children"]["$"]["end"] == True:
                            word_list.append((new_word, rack, row, column))



def forwards_vertical(node, word, rack, word_list, board, row, column):
    if board[row][column] in not_letters:
        if node["end"] == True:
            word_list.append((word, rack, row-len(word), column))


        if row <= 13:
            for letter in set(rack):
                if letter == "#":
                    for child in node["children"]:
                        if child != "$":
                            new_word = word + child
                            copy_rack = copy.deepcopy(rack)
                            copy_rack.remove(letter)
                            forwards_vertical(node["children"][child], new_word, copy_rack, word_list, board, row + 1, column)
                else:
                    if letter in node["children"]:
                        new_word = word + letter
                        copy_rack = copy.deepcopy(rack)
                        copy_rack.remove(letter)
                        forwards_vertical(node["children"][letter], new_word, copy_rack, word_list, board, row + 1, column)
        if row == 14:
            for letter in set(rack):
                if letter == "#":
                    for child in node["children"]:
                        if child != "$":
                            new_word = word + child
                            copy_rack = copy.deepcopy(rack)
                            copy_rack.remove(letter)
                            new_node = node["children"][child]
                            if new_node["end"] == True:
                                word_list.append((new_word, rack, row - len(word), column))
                else:
                    if letter in node["children"]:
                        new_word = word + letter
                        copy_rack = copy.deepcopy(rack)
                        copy_rack.remove(letter)
                        new_node = node["children"][letter]
                        if new_node["end"] == True:
                            word_list.append((new_word, rack, row - len(word), column))

    else:
        letter = board[row][column]
        if letter in node["children"]:
            new_word = word + letter
            if row <= 13:
                forwards_vertical(node["children"][letter], new_word, rack, word_list, board, row + 1, column)
            else:
                new_node = node["children"][letter]
                if new_node["end"] == True:
                    word_list.append((new_word, rack, row-len(word) + 1, column))




def score_move(move, board, direction, data):
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

            node = data["children"][word[i]]

            while(row-count >= 0):
                try:
                    letter = board[row-count][column+i]
                    if letter not in not_letters:
                        if letter not in node["children"]:
                            return False
                        else:
                            new_word.insert(0,letter)
                            new_word_y = row - count
                            node = node["children"][letter]
                    else:
                        break
                    count += 1
                except:
                    break


            if "$" not in node["children"]:
                return False
            node = node["children"]["$"]

            count = 1
            while(True):
                try:
                    letter = board[row+count][column+i]
                    if letter not in not_letters:
                        if letter not in node["children"]:
                            return False
                        else:
                            new_word.append(letter)
                            node = node["children"][letter]

                    else:
                        break

                    count += 1
                except:
                    break

            if len(new_word) > 1:
                if node["end"] != True:
                    return False
                str = ""
                if board[row][column+i] in not_letters:
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

            node = data["children"][word[i]]
            while(column-count >= 0):
                letter = board[row+i][column-count]
                if letter not in not_letters:
                    if letter not in node["children"]:
                        return False
                    else:
                        new_word.insert(0,letter)
                        new_word_x = column - count
                        node = node["children"][letter]
                else:
                    break
                count += 1

            count = 1

            if "$" not in node["children"]:
                return False
            node = node["children"]["$"]

            while(True):
                try:
                    letter = board[row+i][column+count]
                    if letter not in not_letters:
                        if letter not in node["children"]:
                            return False
                        else:
                            new_word.append(letter)
                            node = node["children"][letter]
                    else:
                        break
                    count += 1
                except:
                    break

            if len(new_word) > 1:
                if node["end"] != True:
                    return False
                str = ""
                if board[row+i][column] in not_letters:
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
