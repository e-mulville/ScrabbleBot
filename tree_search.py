import json
import time
import itertools

not_letters = ["   ", " * ", "TLS", "TWS", "DLS", "DWS"]

def brie_search(board, rack):

    start_time = time.time()

    print("Opening")
    with open('briedata.txt') as json_file:
        #data = json.load(json_file)
        pass
    print("--- %s seconds ---" % (time.time() - start_time))

    for row_number, row in enumerate(board):
        for column_number, tile in enumerate(row):
            if board[row_number][column_number] not in not_letters:
                #horizontal
                if board[row_number][column_number-1] not in not_letters:
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

                    print(word)
                    node = data["children"][word]

                #vertical
                if board[row_number][column_number-1] not in not_letters:
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

                    node = data["children"][word]
            else:
                for tile in rack:
                    node = data["children"][tile]
                #blank space
                pass
