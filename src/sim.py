import random
from pyvis.network import Network
###############################################
#       Creation d'un arbre d'infectes        #
#Etonnament le programme tourne plutot pas mal#
###############################################

#Arbre
class Tree:
    
    def __init__(self, name, date):
        self.name = name
        self.date = date
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

    def append(self, old, new, date):
        if not self:
            return False
        if self.name == old:
            self.children.append(Tree(new,date))
            return True
        for e in self.children:
            if e.append(old, new, date):
                return True

#Message, stockes dans une liste
class Message:
    def __init__(self, date, name, content):
        self.date = date
        self.name = name
        self.content = content

#Mini parsing du chat en list de message
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
        #print(date, ',', name, ',', content)
        chat.append(Message(date, name, content))

#Creation de l'arbre a partir d'un patient passe en argument
def search_infected(chat, name):
    infected_tree = Tree(name,'00:00:00')
    infected_list = [name]
    #print(name, "est infecte")
    for i in range(1, len(chat) - 1):
        if chat[i].name in infected_list:
            if random.uniform(0, 1) < 0.058 and not (chat[i - 1].name in infected_list):
                infected_list.append(chat[i - 1].name)
                #print(chat[i - 1].name, "est infecte par", chat[i].name)
                infected_tree.append(chat[i].name, chat[i - 1].name, chat[i].date)
            if random.uniform(0, 1) < 0.058 and not (chat[i + 1].name in infected_list):
                infected_list.append(chat[i + 1].name)
                #print(chat[i + 1].name, "est infecte par", chat[i].name)
                infected_tree.append(chat[i].name, chat[i + 1].name, chat[i].date)
    return infected_tree

#Recuperation de tous ceux qui ont parles dans les 5 premieres minutes
def fill_list(chat):
    name_list = set()
    for message in chat:
        if "00:20:00"< message.date:
            break
        name_list.add(message.name)
    return name_list

#%%
def generate_graph(arbre):
    got_net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    got_net.add_node(arbre.name,value=len(arbre.children),color='#00FF00')         
    recursive(arbre,got_net,arbre.name)
    got_net.show_buttons(filter_=['nodes'])
#    network.Network.set_options()
    got_net.show("test.html")
    
#%%
def recursive(arbre,got_net,node_pere):
    for child in arbre.children:
        got_net.add_node(child.name,value=len(child.children))
        got_net.add_edge(node_pere, child.name, title=child.date)
        recursive(child,got_net,child.name)
#%%
    
def main():
    chat = []
    chat_parse(chat)
    name_list = ['Sarakzite']
#    name_list = fill_list(chat)
    Liste_plus_probable=[]
    print(name_list)
    for name in name_list:
        results_list = []
        tri_list=[]
        for i in range(10):
            infected_tree = search_infected(chat, name)
            tri_list.append((infected_tree,infected_tree.count()))
            results_list.append(infected_tree.count())
        results_list.sort()
        if results_list[len(results_list) // 2]>300:
            for arbre,nb in tri_list:
                if nb==results_list[len(results_list) // 2]:
                    arbre_median=arbre
                    generate_graph(arbre_median)
            Liste_plus_probable.append(name)
            fichier=open('../data/Liste_plus_probable.csv', 'a')
            line=str(name)+ ","+ str(results_list[0])+ ","+ str(results_list[len(results_list) // 2])+ ","+ str(results_list[len(results_list) - 1])+"\n"
            fichier.write(line)

        #On affiche le resultat des 100 simulations pour la personne, tout ca dans le terminal, j'ai rien mis sous forme de graph
            print("-------------------")
            print("name:", name, ", min:", results_list[0], ", med:", results_list[len(results_list) // 2], ", max:", results_list[len(results_list) - 1])


    
if __name__ == '__main__':
    main()
