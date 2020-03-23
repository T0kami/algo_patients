import random
###############################################
#       Creation d'un arbre d'infectes        #
#Etonnament le programme tourne plutot pas mal#
###############################################

#Arbre
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

#Message, stockes dans une liste
class Message:
    def __init__(self, date, name, content):
        self.date = date
        self.name = name
        self.content = content

#Mini parsing du chat en list de message
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
        #print(date, ',', name, ',', content)
        chat.append(Message(date, name, content))

#Creation de l'arbre a partir d'un patient passe en argument
def search_infected(chat, name):
    infected_tree = Tree(name)
    infected_list = [name]
    #print(name, "est infecte")
    for i in range(1, len(chat) - 1):
        if chat[i].name in infected_list:
            if random.uniform(0, 1) < 0.065 and not (chat[i - 1].name in infected_list):
                infected_list.append(chat[i - 1].name)
                #print(chat[i - 1].name, "est infecte par", chat[i].name)
                infected_tree.append(chat[i].name, chat[i - 1].name)
            if random.uniform(0, 1) < 0.065 and not (chat[i + 1].name in infected_list):
                infected_list.append(chat[i + 1].name)
                #print(chat[i + 1].name, "est infecte par", chat[i].name)
                infected_tree.append(chat[i].name, chat[i + 1].name)
    return infected_tree

#Recuperation de tous ceux qui ont parles dans les 5 premieres minutes
def fill_list(chat):
    name_list = set()
    for message in chat:
        if message.date > "00:05:00":
            break
        name_list.add(message.name)
    return name_list


def main():
    chat = []
    chat_parse(chat)
    #name_list = ["g3nya", "Kao0", "Sarukog", "NahJoTV", "captainfarn", "frenchkowstar", "wollows", "NUCKTROOPER", "snowizz__", "attendspyro", "mrkabo77", "primzen0", "is0phys", "lolix_idontknow"]
    name_list = fill_list(chat)
    print(name_list)
    for name in name_list:
        results_list = []
        for i in range(100):
            infected_tree = search_infected(chat, name)
            results_list.append(infected_tree.count())
        results_list.sort()
        #On affiche le resultat des 100 simulations pour la personne, tout ca dans le terminal, j'ai rien mis sous forme de graph
        print("-------------------")
        print("name:", name, ", min:", results_list[0], ", med:", results_list[len(results_list) // 2], ", max:", results_list[len(results_list) - 1])


if __name__ == '__main__':
    main()
