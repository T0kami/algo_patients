import random


class Tree:
    def __init__(self, name):
        self.name = name
        self.children = []

    def count(self):
        if (not self):
            return 0
        c = 0
        for e in self.children:
            c += e.count()
        return c + 1

    def print(self):
        print(self.name)
        for child in self.children:
            child.print()

    def append(self, old, new):
        if not self:
            return False
        if self.name == old:
            self.children.append(Tree(new))
            return True
        for e in self.children:
            if e.append(old, new):
                return True


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
        if date > "06:00:00":
            break
        i = j + 2
        while j < len(line) and line[j] != ":":
            j += 1
        name = line[i:j]
        j += 2
        content = line[j:]
        print(date, ',', name, ',', content)
        chat.append(Message(date, name, content))


def search_infected(chat, name):
    infected_tree = Tree(name)
    infected_list = [name]
    print(name, "est infecte")
    for i in range(1, len(chat) - 1):
        if chat[i].name in infected_list:
            if random.uniform(0, 1) < 0.06 and not (chat[i - 1].name in infected_list):
                infected_list.append(chat[i - 1].name)
                print(chat[i - 1].name, "est infecte par", chat[i].name)
                infected_tree.append(chat[i].name, chat[i - 1].name)
            if random.uniform(0, 1) < 0.06 and not (chat[i + 1].name in infected_list):
                infected_list.append(chat[i + 1].name)
                print(chat[i + 1].name, "est infecte par", chat[i].name)
                infected_tree.append(chat[i].name, chat[i + 1].name)
    return infected_tree


def main():
    chat = []
    chat_parse(chat)
    infected_tree = search_infected(chat, "snowizz__")
    print("-------------------")
    infected_tree.print()
    print(infected_tree.count())


if __name__ == '__main__':
    main()
