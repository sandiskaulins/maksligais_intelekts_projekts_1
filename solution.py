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
    def __init__(self, max_level=None):
        self.nodes_list = []
        self.arc_dict = {}
        self.visited_nodes = {}
        self.level_counters = {}  # Glabā nākamos indeksus katram līmenim #Chatgbpt
        self.max_level = max_level


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
    possible_actions = [] 
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
            if (len(new_num_string)>1) and (tree.max_level is None or level < tree.max_level):
                generate_tree(newNode,tree)


        possible_actions.append((new_num_string, points, bank, level))
    return possible_actions


# Funkcija virknes ģenerēšanai
def generate_num_string():
    while(True):
        try:
            print("Ievadiet virknes garumu")
            len_num_string = int(input())
            break 
        except:
            print("Ievadiet skaitli!")
    if(15 <= len_num_string <= 25):
        i = 0
        num_string = ""
        while(i<len_num_string):
            num_string+= str(random.randint(1,9))
            i+=1
        return num_string
    else:
        print("Ievadiet skaitļu virknes garumu no 15 līdz 25 ieskaitot")
        return generate_num_string()

# Funkcija rezūltātu pārbaudei
def result_check(points,bank):
    if(((points%2)==0) and ((bank%2)==0)):
        print("Uzvar spēlētājs, kas iesāka spēli")
    elif(((points%2)==1) and ((bank%2)==1)):
        print("Uzvar otrs spēlētājs")
    else:
        print("Neizšķirts")


def kurs_sak(): 
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
        return kurs_sak()


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

def utility(starting_player, points, bank):
    if(((points%2)==0) and ((bank%2)==0)):
        if (starting_player == 'dators'):
            return 1
        else:
            return -1
    elif(((points%2)==1) and ((bank%2)==1)):
        if (starting_player == 'dators'):
            return -1
        else:
            return 1
    else:
        return 0

def new_node(last_node):
    last_node.id = "N.0.1."
    last_node.level = 0
    return last_node

def minimax(node, maximizingplayer: bool, starting_player, points, bank): 
     # Pārbaude, vai virkne ir līdz 16 simboliem
    node.points = points
    node.bank = bank 
    if len(node.num_string) <= 16: 
        tree = Tree(max_level=None)
    else: 
        tree = Tree(max_level=10) 


    tree.insert_node(node)
    possible_actions = generate_tree(node, tree) # Generē iespējamos koka zarus
    if (len(node.num_string) == 1):
        return utility(starting_player, points, bank)
    if (node.level <=10):
        return heiristiska_novertejuma_funkcija_dziļumam(starting_player, points, bank)  

    if maximizingplayer:
        maxvalue = float('-inf')
        for action in possible_actions:
            new_num_string, updated_points, updated_bank = action
            new_id = tree.get_next_id(node.level + 1)
            new_state = Node(node.id, "".join(new_num_string), updated_points, updated_bank, node.level + 1)
            value = minimax(new_state, len(new_state.num_string), False, starting_player, updated_points, updated_bank, tree) # chats raksta šādi value = minimax(new_state, False, starting_player, tree) jo node objekts if(len(node...)returnutility šajā vietā) jau satur tos pārējos laukus 
            maxvalue = max(maxvalue, value) 

        return maxvalue

    else:
        minvalue = float('inf')
        for action in possible_actions:
            new_num_string, updated_points, updated_bank = action
            new_id = tree.get_next_id(node.level + 1)
            new_state = Node(node.id, "".join(new_num_string), updated_points, updated_bank, node.level + 1)
            value = minimax(new_state, len(new_state.num_string), True, starting_player, updated_points, updated_bank, tree)
            minvalue = min(minvalue, value)  

        return minvalue

def alpha_beta_minmax(state, depth, alpha, beta, maximizing_player, num_string):
    # Pārbaude, vai virkne ir līdz 16 simboliem
    root = Node("N.0.1", num_string, state.points, state.bank, 0) 
    if len(num_string) <= 16: 
        tree = Tree(max_level=None)
    else: 
        tree = Tree(max_level=10) 

    tree.insert_node(root)
    possible_actions = generate_tree(root, tree) # Generē iespējamos koka zarus

    if len(state.num_string) <= 16 or depth == 0:
        return utility(state.starting_player, state.points, state.bank)
    if len(state.num_string) <= 10:
        return heiristiska_novertejuma_funkcija_dziļumam(state.starting_player, state.points, state.bank)

    if maximizing_player:
        max_eval = float('-inf')
        for action in possible_actions:
            new_num_string, updated_points, updated_bank = action
            new_state = Node(state.id, "".join(new_num_string), updated_points, updated_bank, state.level + 1)
            eval = alpha_beta_minmax(new_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta nogriešana
        return max_eval
    else:
        min_eval = float('inf')
        for action in possible_actions:
            new_num_string, updated_points, updated_bank = action
            new_state = Node(state.id, "".join(new_num_string), updated_points, updated_bank, state.level + 1)
            eval = alpha_beta_minmax(new_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alfa nogriešana
        return min_eval
    
# Funkcija algoritma noteikšanai 

def which_alg():
    print("Kuru algoritmu izvēlēsies, ja minimax iavadi m, ja alfa - beta ievadi a")
    ievade = input()
    if (ievade == "m"):
        return "minimax"
    elif (ievade == "a"):
        return "alfa-beta"
    else: 
        print("Mēģinat velreiz, kuru algoritmu izvēlēsies, ja minimax iavadi m, ja alfa - beta ievadi a")
        return which_alg()
# Galvenā funkcija - ar ko sākas programma
def main():
    num_string = generate_num_string() # Ģenerējam skaitļu virkni
    algoritma_izvele = which_alg() # izvēlamies algoritmu
    starting_player = kurs_sak()

    print("Sākotnējā virkne:", num_string)

    if(algoritma_izvele == "minimax"):
        root = Node("N.0.1", num_string, 0, 0, 0) 
        if(starting_player=="dators"):
            minimax(root,True,starting_player,0,0)
        else:
            minimax(root,False,starting_player,0,0)
    else:
        if(starting_player=="dators"):
            alpha_beta_minmax()
        else:
            alpha_beta_minmax()


    print("Kods Galā")   
        
if __name__ == "__main__":
    main()
