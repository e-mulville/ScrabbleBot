import string
import time



class BrieNode:
    def __init__(self, letter, end, delimiter):
        self.letter = letter.upper()
        self.children = {}
        self.end = end
        self.delimiter = delimiter

    def add_child(self, letter, end = False, delimiter = False):
        letter = letter.upper()
        child_node = BrieNode(letter, end, delimiter)
        self.children[letter] = child_node
        self.end = end
        self.delimiter = delimiter

    def get_letter(self):
        return self.letter

    def get_children(self):
        return self.children

    def get_end(self):
        return self.end

    def get_delimiter(self):
        return self.delimiter

class BrieFirstNode:
    def __init__(self, word, end, delimiter):
        self.word = word.upper()
        self.children = {}
        self.end = end
        self.delimiter = delimiter

    def add_child(self, letter, end = False, delimiter = False):
        letter = letter.upper()
        child_node = BrieNode(letter, end, delimiter)
        self.children[letter] = child_node
        self.end = end
        self.delimiter = delimiter

    def get_letter(self):
        return self.letter

    def get_children(self):
        return self.children

    def get_end(self):
        return self.end

    def get_delimiter(self):
        return self.delimiter

class BrieStartNode:
    def __init__(self):
        self.children = {}
        self.end = False
        self.delimiter = False

    def add_child(self, word, end = False, delimiter = False):
        word = word.upper()
        child_node = BrieFirstNode(word, end, delimiter)
        self.children[word] = child_node

    def get_children(self):
        return self.children

    def get_end(self):
        return self.end


def print_dict_preffix(node, word = ""):
    new_word = word

    if node.get_delimiter() == True:
        new_word = word + "#"

    if node.get_end() == True:
        print(new_word)
        print("aaa")

    child_nodes = node.get_children()

    if not child_nodes:
        return

    if node.get_delimiter() == True:
        for child in child_nodes:
            print_dict_suffix(child_nodes[child], new_word)
    if node.get_delimiter() != True:
        for child in child_nodes:
            new_word = str(child) + word
            print_dict_preffix(child_nodes[child], new_word)
            #print_dict(child_node)

def print_dict_suffix(node, word = ""):
    if node.get_end() == True:
        #print(word)
        pass
    child_nodes = node.get_children()

    if not child_nodes:
        return
        
    for child in child_nodes:
        new_word = word + str(child)
        print_dict_suffix(child_nodes[child], new_word)
        #print_dict(child_node)

def main():

    start_time = time.time()

    dictionary = open("dic.txt", "r")
    clean_dictionary = list(string.ascii_uppercase)

    for word in dictionary:
        clean_dictionary.append(word[:-1])

    dictionary.close()

    start = BrieStartNode()

    for word in clean_dictionary[:20]:

        start.add_child(word)

        current_node = start.get_children()[word]

        for longer_word in clean_dictionary:
            if word in longer_word:
                current_node = start.get_children()[word]
                prefix, _, suffix = longer_word.partition(word)

                #TODO NEEDS CHANGING

                #print(prefix, word, suffix)

                for letter in prefix[::-1]:
                    letter = letter.upper()
                    child_nodes = current_node.get_children()
                    child_letters = [key for key in child_nodes]

                    if letter.upper() not in child_letters:
                        current_node.add_child(letter)

                    current_node = child_nodes[letter]

                if suffix:
                    current_node.add_child("#", delimiter = True)
                    child_nodes = current_node.get_children()
                    current_node = child_nodes["#"]

                    for letter in suffix[:-1]:
                        letter = letter.upper()
                        child_nodes = current_node.get_children()
                        child_letters = [key for key in child_nodes]

                        if letter.upper() not in child_letters:
                            current_node.add_child(letter)

                        current_node = child_nodes[letter]

                    letter = suffix[-1].upper()
                    current_node.add_child(letter, end = True)

                else:
                    current_node.add_child("#", end = True, delimiter = True)

    print("Done")
    print("--- %s seconds ---" % (time.time() - start_time))
    for child in start.get_children():
        print(child)
        print("~~~~~~~~~~~~~~~")
        print_dict_preffix(start.get_children()[child])


if __name__== "__main__":
    main()
