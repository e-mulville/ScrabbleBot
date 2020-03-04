import string
import time
import json

def find_offsets(haystack, needle):
    """
    Find the start of all (possibly-overlapping) instances of needle in haystack
    """
    offs = -1
    while True:
        offs = haystack.find(needle, offs+1)
        if offs == -1:
            break
        else:
            yield offs


def print_dict_preffix(node, word):
    if node["delimiter"] == True:
        new_word = word + "#"

        if node["end"] == True:
            print(new_word)

        for child in node["children"]:
            next_node = node["children"][child]
            print_dict_suffix(next_node, new_word)

    if node["delimiter"] == False:
        new_word = node["letter"] + word

        if node["end"] == True:
            print(new_word)

        for child in node["children"]:
            next_node = node["children"][child]
            print_dict_preffix(next_node, new_word)


    if not node["children"]:
        return

def print_dict_suffix(node, word):
    new_word = word + node["letter"]

    if node["end"] == True:
        print(new_word)

    if not node["children"]:
        return

    for child in node["children"]:
        next_node = node["children"][child]
        print_dict_suffix(next_node, new_word)

def main():
    start_time = time.time()

    dictionary = open("dic.txt", "r")
    clean_dictionary = list(string.ascii_uppercase)

    for word in dictionary:
        clean_dictionary.append(word[:-1])

    dictionary.close()

    start = { "children" : {} }

    for word in clean_dictionary:
        start_node = {
            "word" : word,
            "children" : {}
        }

        start["children"][word] = start_node

        for longer_word in clean_dictionary:
            for offs in find_offsets(longer_word, word):
                #needs changing
                prefix = longer_word[:offs]
                suffix = longer_word[offs+1:]

                prev_node = start_node

                for letter in prefix[::-1]:
                    if letter not in prev_node["children"]:
                        next_node = {
                            "letter" : letter,
                            "end" : False,
                            "delimiter" : False,
                            "children" : {}
                        }
                        prev_node["children"][letter] = next_node
                        prev_node = next_node
                    else:
                        prev_node = prev_node["children"][letter]

                if suffix:
                    if "#" not in prev_node["children"]:
                        next_node = {
                            "letter" : "#",
                            "end" : False,
                            "delimiter" : True,
                            "children" : {}
                        }
                        prev_node["children"]["#"] = next_node
                        prev_node = next_node
                    else:
                        prev_node = prev_node["children"]["#"]


                    for letter in suffix[:-1]:
                        if letter not in prev_node["children"]:
                            next_node = {
                                "letter" : letter,
                                "end" : False,
                                "delimiter" : False,
                                "children" : {}
                            }
                            prev_node["children"][letter] = next_node
                            prev_node = next_node
                        else:
                            prev_node = prev_node["children"][letter]

                    if suffix[-1] not in prev_node["children"]:
                        next_node = {
                            "letter" : suffix[-1],
                            "end" : True,
                            "delimiter" : False,
                            "children" : {}
                        }
                        prev_node["children"][suffix[-1]] = next_node
                    else:
                        prev_node["children"][suffix[-1]]["end"] = True


                else:
                    if "#" not in prev_node["children"]:
                        next_node = {
                            "letter" : "#",
                            "end" : True,
                            "delimiter" : True,
                            "children" : {}
                        }
                        prev_node["children"]["#"] = next_node
                    else:
                        prev_node["children"]["#"]["end"] = True


    print("Done")
    print("--- %s seconds ---" % (time.time() - start_time))

    with open('briedata.txt', 'w') as outfile:
        json.dump(start, outfile)

    # for child in start["children"]:
    #     word_node = start["children"][child]
    #     for i in word_node["children"]:
    #         print_dict_preffix(word_node["children"][i], "")




if __name__ == "__main__":
    main()
