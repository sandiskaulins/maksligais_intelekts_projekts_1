import random

# Tiek izveidota klase, kas saturēs info par vienu virsotni kokā
class Node:
    # Klases konstruktors, kas inicializē visas mainīgos, kas mainās spēles gaitā
    def __init__(self, id, num_string, points, bank, level, player):
        self.id = id
        self.num_string = num_string
        self.points = points
        self.bank = bank
        self.level = level
        self.player = player

# Tiek izveidota spēles koka klase
class Tree:
    # Tiek izveidots konstruktors, kas inicializē virsotņu, loku un apmeklēto virsotņu kopas
    def __init__(self):
        self.nodes_list = []
        self.arc_dict = {}
        self.visited_nodes = {}
        self.level_counters = {}  # Glabā nākamos indeksus katram līmenim #Chatgbpt
        

    #ChatGbpt
    def get_next_id(self, level):
        if level not in self.level_counters:
            self.level_counters[level] = 1  # Sākam skaitīt no 1
        else:
            self.level_counters[level] += 1  # Palielinām skaitītāju
        return f"N.{level}.{self.level_counters[level]}"

    # Metode, kas pievieno jaunu virsotni spēles kokam un saglabā unikālo spēles stāvokli vārdnīcā
    def insert_node(self, Node):
        self.nodes_list.append(Node)
        # ChatGpt
        key = (Node.num_string, Node.points, Node.bank)
        self.visited_nodes[key] = Node.id 

    # Metode, kas pievieno jaunu loku spēles kokam
    def insert_arc(self, start_id, end_id):
        # ChatGpt
        if start_id not in self.arc_dict:
            self.arc_dict[start_id] = []
        if end_id not in self.arc_dict[start_id]:  # Pārbaude, vai loks jau pastāv
            self.arc_dict[start_id].append(end_id)

# Funkcija, kas izveido spēles koku rekursīvi
def generate_tree(node, tree):
    num_string = list(node.num_string) # Pārveido virkni uz saraktstu
    for i in range(len(num_string)-1): # Cikls 1 līmeņa visu virsotņu izveidei

        pairValue = int(num_string[i]) + int(num_string[i+1]) # Blakus esošo skaitļu summa
        points = node.points 
        bank = node.bank
        result = ""

        new_num_string = num_string[:] # Virknes kopijas izveide

        # Atkarībā no blakus esošo skaitļu summas veidojas dažādi stāvokļi virsotnēm
        if(pairValue>7):
            new_num_string[i]="1"
            points +=1
        elif(pairValue<7):
            new_num_string[i]="3"
            points -=1
        else:
            new_num_string[i]="2"
            bank +=1

        new_num_string.pop(i+1) # i+1 skaitļa dzēšana no virknes
        result = "".join(new_num_string) # saraksta pārveide uz string
        level = node.level + 1 # līmenis paliek dziļāks
        key = (result,points,bank) # unikālā atslēga
        
        # Pārbaude, vai virsotne ar šo stāvokli jau eksistē
        if key in tree.visited_nodes:
            existing_node_id = tree.visited_nodes[key]
            if int(existing_node_id.split('.')[1]) == level:  # Pārbaudām, vai tas ir nākamais līmenis
                # Pārbaude, vai loks starp divām virsotnēm jau pastāv
                tree.insert_arc(node.id, existing_node_id)
        else:
        # Ja neeksistē veidojam jaunu virsotni un loku
            id = node.id
            id1 = tree.get_next_id(level)  # Globāls secīgs ID katrā līmenī #ChatGbt
            next_player = 'dators' if node.player == 'cilvēks' else 'cilvēks' # šo ieviesa chatgpt
            newNode = Node(id1,result,points,bank,level,next_player)
            tree.insert_node(newNode)
            tree.insert_arc(id, id1)
        # Kamēr virknes garums nav 1 dodamies dziļāk kokā
            if len(new_num_string)>1:
                generate_tree(newNode,tree)

# Funkcija virknes ģenerēšanai
# def generate_num_string():
#     print("Ievadiet virknes garumu")
#     len_num_string = int(input())
#     if (15 <= len_num_string <= 25):
#         i = 0
#         num_string = ""
#         while(i<len_num_string):
#             num_string+= str(random.randint(1,9))
#             i+=1
#         return num_string
#     else :
#         print("Ievadiet skaitļu virknes garumu no 15 līdz 25 ieskaitot")
#         return generate_num_string()

def generate_num_string():
    print("Ievadiet virknes garumu")
    len_num_string = int(input())
    i = 0
    num_string = ""
    while(i<len_num_string):
        num_string+= str(random.randint(1,9))
        i+=1
    return num_string

# Funkcija rezūltātu pārbaudei
def result_check(points,bank):
    if(((points%2)==0) and ((bank%2)==0)):
        print("Uzvar spēlētājs, kas iesāka spēli")
    elif(((points%2)==1) and ((bank%2)==1)):
        print("Uzvar otrs spēlētājs")
    else:
        print("Neizšķirts")

def kurssākspēli():
    print("Kurš sāk spēli, ja cilvēks ieraksti c, ja dators ieraksti d")
    ievade = input()
    ievade = ievade.lower()
    if (ievade == "c"):
        return 'cilvēks' # šis tika ģenerēts ar AI es nesapratu kā pabeigt šo 
    elif (ievade == "d"):
        return 'dators' # un šī rinda
    else: 
        print("Mēģinat velreiz, kurš sāk spēli cilvēks vai dators, ja vēlaties, lai cilvēks sāk rakstat c, bet ja dators d ")
        return kurssākspēli()

def heiristiska_novertejuma_funkcija(starting_player, num_string_len, points, bank):
    # Katram jāimplementē viens faktors
    print("")


# Galvenā funkcija - ar ko sākas programma
def main():
    num_string = generate_num_string()
    tree = Tree()
    spēletājaizvēli = kurssākspēli()
    root = Node("N.0.0", num_string, 0, 0, 0, spēletājaizvēli) # un šo rindu AI modificēja ar to spēletājaizvēli
    tree.insert_node(root)

    generate_tree(root, tree)
    
    print("Sākotnējā virkne:", root.num_string)

    for x in tree.nodes_list:
        print(x.id,x.num_string,x.points,x.bank,x.level,x.player)
    
    for x, y in tree.arc_dict.items():
        print(x, y)   
        
if __name__ == "__main__":
    main()
