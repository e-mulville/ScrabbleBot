class BrieNode:
    def __init__(self, letter, end, delimiter):
        self.letter = letter.upper()
        self.children = {}
        self.end = end
        self.delimiter = delimiter

    def add_child(self, letter, end = False, delimiter = False):
        letter = letter.upper()
        child_node = BrieNode(letter, end)
        self.children[letter] = child_node
        self.end = end
        self.delimiter = delimiter

    def get_letter(self):
        return self.letter

    def get_children(self):
        return self.children

    def get_end(self):
        return self.end


class BrieStartNode:
    def __init__(self):
        self.children = {}
        self.end = False

    def add_child(self, letter, end = False):
        letter = letter.upper()
        child_node = BrieNode(letter, end)
        self.children[letter] = child_node
        pass

    def get_children(self):
        return self.children

    def get_end(self):
        return self.end


def print_dict(node, word = ""):
    if node.get_end() == True:
        print(word)

    child_nodes = node.get_children()
    if not child_nodes:
        return


    for child in child_nodes:
        new_word = word + str(child)
        print_dict(child_nodes[child], new_word)
        #print_dict(child_node)

def main():

    dictionary = open("dic.txt", "r")
    clean_dictionary = []

    for word in dictionary:
        clean_dictionary.append(word[:-1])

    dictionary.close()

    start = BrieStartNode()

    for word in clean_dictionary:
        children = [key for key in start.get_children()]
        if word[0].upper() not in children:
            start.add_child(word[0])

        current_node = start.get_children()[word[0].upper()]
        for letter in word[1:-1]:
            letter = letter.upper()
            child_nodes = current_node.get_children()
            child_letters = [key for key in child_nodes]

            if letter.upper() not in child_letters:
                current_node.add_child(letter)

            current_node = child_nodes[letter]

        letter = word[-1].upper()
        current_node.add_child(letter, end = True)

    print_dict(start)


if __name__== "__main__":
    main()
