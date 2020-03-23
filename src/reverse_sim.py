import random


class Tree:
    def __init__(self, name):
        self.name = name
        self.children = []

    def print(self):
        print(self.name)
        for child in self.children:
            print("\t", end="")
            child.print()

    def append(self, child):
        self.children.append(child)


class Message:
    def __init__(self, date, name, content):
        self.date = date
        self.name = name
        self.content = content


def chat_parse(chat):
    file = open('../data/chatlog.txt', 'r')
    lines = file.readlines()
    for line in lines:
        j = 0
        while j < len(line) and line[j] != "]":
            j += 1
        date = line[1:(j - 4)]
        if date > "00:01:00":
            break
        i = j + 2
        while j < len(line) and line[j] != ":":
            j += 1
        name = line[i:j]
        j += 2
        content = line[j:]
        print(date, ',', name, ',', content)
        chat.insert(0, Message(date, name, content))


def search_infected(chat, curr, index):
    infected_tree = Tree(curr)
    #print(curr)
    for i in range(index, len(chat) - 1):
        if chat[i].name == curr:
            child1 = search_infected(chat, chat[i - 1].name, i)
            infected_tree.append(child1)
            child2 = search_infected(chat, chat[i + 1].name, i)
            infected_tree.append(child2)
    return infected_tree


def main():
    chat = []
    chat_parse(chat)
    infected_tree = search_infected(chat, "Kao0", 1)
    infected_tree.print()


if __name__ == '__main__':
    main()
