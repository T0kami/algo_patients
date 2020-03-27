import random
from pyvis.network import Network
import statistics
import parsing_all_logs


###############################################
#       Creation d'un arbre d'infectes        #
# Etonnament le programme tourne plutot pas mal#
###############################################

# Arbre
class Tree:

    def __init__(self, name, date):
        self.name = name
        self.date = date
        self.status = 'infected'
        self.children = []

    def count(self):
        if not self:
            return 0
        c = 0
        for e in self.children:
            c += e.count()
        return c + 1
    
    
    def count_dead(self):
        if not self:
            return 0
        c = 0
        if self.status=='dead':
            c+=1
        for e in self.children:
            c += e.count_dead()
        return c


    def count_cured(self):
        if not self:
            return 0
        c = 0
        if self.status=='cured':
            c+=1
        for e in self.children:
            c += e.count_cured()
        return c

    def count_infected(self):
        if not self:
            return 0
        c = 0
        if self.status=='infected':
            c+=1
        for e in self.children:
            c += e.count_infected()
        return c

    def print(self):
        print(self.name)
        for child in self.children:
            child.print()

    def append(self, old, new, date):
        if not self:
            return False
        if self.name == old:
            self.children.append(Tree(new, date))
            return True
        for e in self.children:
            if e.append(old, new, date):
                return True

    def update(self, name, status):
        if not self:
            return False
        if self.name == name:
            self.status=status
            return True
        if len(self.children)==0:
            return False
        for e in self.children:
            if e.update(name, status):
                return True
    
    def find(self, name):
        if not self:
            return False
        if self.name == name:
            return self
        if len(self.children)==0:
            return False
        for e in self.children:
            f=e.find(name)
            if f:
                return f
    
# Message, stockes dans une liste
class Message:
    def __init__(self, date, name, content):
        self.date = date
        self.name = name
        self.content = content


# Mini parsing du chat en list de message
def chat_parse(chat):
    file = open('../data/chatlog.txt', encoding="utf8")
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
        # print(date, ',', name, ',', content)
        chat.append(Message(date, name, content))


# Creation de l'arbre a partir d'un patient passe en argument
def search_infected(chat, name, rate, rate_guerison):
    infected_tree = Tree(name, 0)
    infected_list = [name]
    cured_list = []
    dead_list = []
    # print(name, "est infecte")
    for i in range(1, len(chat) - 1):
        if (chat[i].name in infected_list) and (chat[i].name not in cured_list) and (chat[i].name not in dead_list):
            if random.uniform(0, 1) < rate and not (chat[i - 1].name in infected_list):
                infected_list.append(chat[i - 1].name)
                # print(chat[i - 1].name, "est infecte par", chat[i].name)
                infected_tree.append(chat[i].name, chat[i - 1].name, chat[i].date)
            if random.uniform(0, 1) < rate and not (chat[i + 1].name in infected_list):
                infected_list.append(chat[i + 1].name)
                # print(chat[i + 1].name, "est infecte par", chat[i].name)
                infected_tree.append(chat[i].name, chat[i + 1].name, chat[i].date)
            if random.uniform(0, 1) < rate_guerison/12.5 and (chat[i].date-infected_tree.find(chat[i].name).date)>3600*24*2:
                infected_tree.update(chat[i].name, 'dead')   
                dead_list.append(chat[i].name)
            elif random.uniform(0, 1) < rate_guerison and (chat[i].date-infected_tree.find(chat[i].name).date)>3600*24*2:
                infected_tree.update(chat[i].name, 'cured')
                cured_list.append(chat[i].name)
     
    return infected_tree


# Recuperation de tous ceux qui ont parles dans les 5 premieres minutes
def fill_list(chat):
    name_list = set()
    for message in chat:
        if "00:20:00" < message.date:
            break
        name_list.add(message.name)
    return name_list


# %%
def generate_graph(arbre):
    got_net = Network(height="100%", width="100%", bgcolor="#222222", font_color="white")
    got_net.add_node(arbre.name, value=(1000*len(arbre.children)**5), color='#FFFF00')
    recursive(arbre, got_net, arbre.name)
    got_net.show_buttons()
    got_net.save_graph("../data/graphs/" + arbre.name + ".html")


# %%
def recursive(arbre, got_net, node_pere):
    for child in arbre.children:
        if child.status=='infected':
            got_net.add_node(child.name, value=(1000*len(child.children)**5))
        if child.status=='cured':
            got_net.add_node(child.name, value=(1000*len(child.children)**5), color='#00FF00')
        if child.status=='dead':
            got_net.add_node(child.name, value=(1000*len(child.children)**5), color='#FF0000')            

        got_net.add_edge(node_pere, child.name, title=child.date)
        recursive(child, got_net, child.name)


# %%


def compute(chat, name_list, rate, rate_guerison, iterations):

    # liste_plus_probable = []
    for name in name_list:
        infected_list = []
        cured_list = []
        dead_list = []
        tree_list = []
        for i in range(iterations):
            print(name, i + 1, "/", iterations)
            infected_tree = search_infected(chat, name, rate, rate_guerison)
            tree_list.append((infected_tree, infected_tree.count()))
            infected_list.append(infected_tree.count())
            cured_list.append(infected_tree.count_cured())
            dead_list.append(infected_tree.count_dead())
        infected_med = statistics.median_low(infected_list)
        dead_med = statistics.median_low(dead_list)
        cured_med = statistics.median_low(cured_list)
        for arbre, nb in tree_list:
            if nb == infected_med:
                arbre_median = arbre
                generate_graph(arbre_median)
                break
        # liste_plus_probable.append(name)
        # fichier = open('../data/Liste_plus_probable.csv', 'a')
        # line = str(name) + "," + str(results_list[0]) + "," + str(results_list[len(results_list) // 2]) + "," + str(
        #     results_list[len(results_list) - 1]) + "\n"
        # fichier.write(line)

        # On affiche le resultat des 100 simulations pour la personne, tout ca dans le terminal, j'ai rien mis sous forme de graph
        print("infected, min:", min(infected_list), ", med:", infected_med, ", max:", max(infected_list))
        print("cured, min:", min(cured_list), ", med:", cured_med, ", max:", max(cured_list))
        print("dead, min:", min(dead_list), ", med:", dead_med, ", max:", max(dead_list))
        print("-------------------")


def main():
    chat=parsing_all_logs.parseur()
    name_list = ['Sarakzite']
    # name_list = fill_list(chat)
    compute(chat, name_list, 0.07, 0.5, 20)


if __name__ == '__main__':
    main()
