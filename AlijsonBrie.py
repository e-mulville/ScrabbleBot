import string
import time
import json

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
            print(word)
            if word in longer_word:
                #print(word, longer_word)
                prefix, _, suffix = longer_word.partition(word)
                #needs changing

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

                    next_node = {
                        "letter" : suffix[-1],
                        "end" : True,
                        "delimiter" : False,
                        "children" : {}
                    }
                    prev_node["children"][suffix[-1]] = next_node
                else:
                    next_node = {
                        "letter" : "#",
                        "end" : True,
                        "delimiter" : True,
                        "children" : {}
                    }
                    prev_node["children"]["#"] = next_node


    print("Done")
    print("--- %s seconds ---" % (time.time() - start_time))

    print(start)

    for child in start["children"]:
        word_node = start["children"][child]
        for i in word_node["children"]:
            print_dict_preffix(word_node["children"][i], "")




if __name__ == "__main__":
    main()