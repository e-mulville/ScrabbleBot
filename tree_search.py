import json
import time
import itertools

not_letters = ["   ", " * ", "TLS", "TWS", "DLS", "DWS"]

def brie_search(board, rack):

    start_time = time.time()

    print("Opening")
    with open('briedata.txt') as json_file:
        data = json.load(json_file)
        pass
    print("--- %s seconds ---" % (time.time() - start_time))


    word = "A"
    print(word[-1])
    print(rack)

    node = data["children"][word[-1]]

    for letter in word[-2::-1]:
        node = node["children"][letter]

    word_list = []

    #print(node)
    for child in node["children"]:
        print(child)
        find_word_preffix(node["children"][child], word[1:], rack, word_list)
    print(word_list)


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
                    for letter in word[-2::-1]:
                        node = node["children"][letter]



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
                    for letter in word[-2::-1]:
                        node = node["children"][letter]
            elif board[row_number][column_number] == " * ":
                # for tile in rack:
                #     node = data["children"][tile]
                #blank space
                pass



def find_word_preffix(node, word, rack, word_list):
    copy_rack = rack
    if node["delimiter"] == True:
        if node["end"] == True:
            word_list.append(word)

        for child in node["children"]:
            next_node = node["children"][child]

            if next_node["delimiter"] == False:
                if child in copy_rack or "#" in copy_rack:
                    if child in copy_rack:
                        copy_rack = rack
                        copy_rack.remove(child)
                        find_word_suffix(next_node, word, copy_rack, word_list)
                    if "#" in copy_rack:
                        copy_rack = rack
                        copy_rack.remove("#")
                        find_word_suffix(next_node, word, copy_rack, word_list)
                else:
                    return
            else:
                find_word_suffix(next_node, new_word, rack, word_list)

    if node["delimiter"] == False:
        new_word = node["letter"] + word

        if node["end"] == True:
            word_list.append(new_word)

        for child in node["children"]:
            next_node = node["children"][child]

            if next_node["delimiter"] == False:
                if child in copy_rack or "#" in copy_rack:
                    if child in copy_rack:
                        copy_rack = rack
                        copy_rack.remove(child)
                        find_word_preffix(next_node, new_word, copy_rack, word_list)
                    if "#" in copy_rack:
                        copy_rack = rack
                        copy_rack.remove("#")
                        find_word_preffix(next_node, new_word, copy_rack, word_list)
                else:
                    return
            else:
                find_word_preffix(next_node, new_word, rack, word_list)

    if not node["children"]:
        return

def find_word_suffix(node, word, rack, word_list):
    new_word = word + node["letter"]

    if node["end"] == True:
        word_list.append(new_word)

    if not node["children"]:
        return


    for child in node["children"]:

        next_node = node["children"][child]

        if child in copy_rack or "#" in copy_rack:
            if child in copy_rack:
                copy_rack = rack
                copy_rack.remove(child)
                find_word_suffix(next_node, new_word, copy_rack, word_list)
            if "#" in copy_rack:
                copy_rack = rack
                copy_rack.remove("#")
                find_word_suffix(next_node, new_word, copy_rack, word_list)
            else:
                return
        else:
            find_word_suffix(next_node, new_word, rack, word_list)
