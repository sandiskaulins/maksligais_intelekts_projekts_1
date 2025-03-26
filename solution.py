import random

# Tiek izveidota klase, kas saturēs info par vienu virsotni kokā
class Node:
    # Klases konstruktors, kas inicializē visas mainīgos, kas mainās spēles gaitā
    def __init__(self, id, num_string, points, bank, level):
        self.id = id
        self.num_string = num_string
        self.points = points
        self.bank = bank
        self.level = level

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
            newNode = Node(id1,result,points,bank,level)
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

# starting_player =' '

def kurssākspēli():
    print("Kurš sāk spēli, ja cilvēks ieraksti c, ja dators ieraksti d")
    ievade = input()
    if (ievade == "c"):
        # starting_player = 'cilvēks'
        return "cilvēks"
    elif (ievade == "d"):
        # starting_player = 'dators'
        return "dators"
    else: 
        print("Mēģinat velreiz, kurš sāk spēli cilvēks vai dators, ja vēlaties, lai cilvēks sāk rakstat c, bet ja dators d ")
        return kurssākspēli()

    
def get_children(node): # visu uzrakstija chats nav manis modificēts šis 
    # Iegūstam visus iespējamos bērnus (iespējamie gājieni)
    children = []
    num_string = list(node.num_string)
    for i in range(len(num_string)-1):  # Pāriem visiem iespējamiem pāriem
        new_num_string = num_string[:]
        pair_value = int(new_num_string[i]) + int(new_num_string[i+1])
        points = node.points
        bank = node.bank

        if pair_value > 7:
            new_num_string[i] = "1"
            points += 1
        elif pair_value < 7:
            new_num_string[i] = "3"
            points -= 1
        else:
            new_num_string[i] = "2"
            bank += 1

        new_num_string.pop(i+1)
        children.append(Node("N." + str(node.level + 1), "".join(new_num_string), points, bank, node.level + 1))
    return children

def heiristiska_novertejuma_funkcija_dziļumam(starting_player, points, bank):
    score = 0
    if starting_player == "dators":
        if points % 2 == 0 and bank % 2 == 0: # ja dators sāk spēli, tad tā mērķis ir iegūt gan kop. skaitu, gan bankas kā pāra skaitli
            score += 10 # += 10 nozīmē, ka šis stāvoklis ir izdevīgs datoram, jo tas mēģina lai abi būtu pāra skaitļi, tādējadi +10 ir heiristiskas funkcijas vērtējums 
        elif points % 2 == 1 and bank % 2 == 1: # ja abi skaitļi ir nepāra, tad šis nav izdevīgi datoram, jo tad uzvarēs cilvēks
            score -=10 # līdz ar to heiristiskas funkcijas vērtējums ir -10
        else:
            score +=5 # nav izdevīgi datoram un nav izdevīgi cilvēkam, bet labāk, kā zaudējums
                
    else: # ja cilvēks sāk spēli
        if points % 2 == 1 and bank % 2 == 1:
            score +=10 # šis stavoklis ir labvēlīgs datoram, gadījumā ja cilvēks sāk spēli, jo datora mērķis ir iegūt nepāra skaitļus
        elif points % 2 == 0 and bank % 2 == 0:
            score -= 10 # šis stāvoklis ir nelabvēlīgs datoram, līdz ar to heiristiskas funkc vērtējums -10
        else:
            score +=5 # nav izdevīgi datoram un nav izdevīgi cilvēkam, bet labāk, kā zaudējums

    return score             

def heiristiska_novertejuma_funkcija(starting_player, points, bank,heiristisks_vērtējuma_punkti):
    heiristisks_vērtējuma_punkti = 0
    if (starting_player == 'dators'):
        if(((points%2)==0) and ((bank%2)==0)):
            heiristisks_vērtējuma_punkti = 1
        elif(((points%2)==1) and ((bank%2)==1)):
            heiristisks_vērtējuma_punkti = -1
        else:
            heiristisks_vērtējuma_punkti = 0
    else:
        if(((points%2)==0) and ((bank%2)==0)):
            heiristisks_vērtējuma_punkti = -1
        elif(((points%2)==1) and ((bank%2)==1)):
            heiristisks_vērtējuma_punkti = 1
        else:
            heiristisks_vērtējuma_punkti = 0 
    return heiristisks_vērtējuma_punkti

def minimax (starting_player, dzilums, node, next_player, heiristiskafunkcija, len_num_string):
    if (len_num_string <= 17): # ja virknes garums nav lielāks par 17
        num_string = list(node.num_string) # Pārveido virkni uz saraktstu
        if (len(node.num_string) == 1):   # kad mūsu virknē palika tikai 1 simbols
            return heiristiska_novertejuma_funkcija   # piešķiram tam 1 0 -1 

        if (starting_player == 'dators'):  #maksimizētais 
            sakumavertiba = -float('inf')  # Sākam ar ļoti negatīvu vērtību
            for child in get_children(node):  # Iegūstam visus bērnus (iespējamos gājienus)
                
            # spēles stāvokli mēs varam uzzināt no root = Node("N.0.0", num_string, 0, 0, 0) 
            # id N.0.0 - ir virsotne ar simbolu virkni ģenereto num_string, tālāk ir point 0, tālāk ir bank 0, ir līmenis 0)
            # pēc līmeņiem man ir jāsadala min max atkarībā no tā kurš spēli
            # ar num_string mums jaatrod kad palika viens tad jāpiešķir heiristiskanovertejumafunkcijas 1 0 -1, balstoties uz points un bank

            
# def minimax(maksimizetajs, minimizetajs, dzilums, starting_player, points, bank, node, heiristiskafunkcija, next_player):
#     num_string = list(node.num_string)  
#     if len(node.num_string) == 1:
#         if starting_player == 'dators':
#             next_player = 'cilvēks'  
#             if maksimizetajs:  
#                 heiristiskafunkcija = heiristiska_novertejuma_funkcija('dators', points, bank)# šī rinda chats
#         else:
#             next_player = 'dators'  
#             if minimizetajs:  
#                 heiristiskafunkcija = heiristiska_novertejuma_funkcija('cilvēks', points, bank) # šī rinda chats

#         return heiristiskafunkcija

    # if (heiristisks_vērtējuma_punkti > heiristisks_vērtējuma_punkti nākamajā gājienā):
    #     slikts gajiens
    # elif (heiristisks_vērtējuma_punkti < heiristisks_vērtējuma_punkti nākamajā gājienā):
    #     labs gājiens
    # else:
    #     nekas namainās nav slikti




# Galvenā funkcija - ar ko sākas programma
def main():
    num_string = generate_num_string()
    tree = Tree()
    #player = kurssākspēli()
    root = Node("N.0.0", num_string, 0, 0, 0) 
    tree.insert_node(root)

    generate_tree(root, tree)
    
    print("Sākotnējā virkne:", root.num_string)

    for x in tree.nodes_list:
        print(x.id,x.num_string,x.points,x.bank,x.level)
    
    for x, y in tree.arc_dict.items():
        print(x, y)   
        
if __name__ == "__main__":
    main()
