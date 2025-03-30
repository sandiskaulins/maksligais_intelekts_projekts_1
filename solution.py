import random
import tkinter as tk
from tkinter import messagebox

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

def alpha_beta_minmax(state, depth, alpha, beta, maximizing_player, num_string, starting_player):
    root = Node("N.0.1", num_string, state.points, state.bank, 0)
    if len(num_string) <= 16:
        tree = Tree(max_level=None)
    else:
        tree = Tree(max_level=10)

    tree.insert_node(root)
    possible_actions = generate_tree(root, tree)  # Generē iespējamos koka zarus

    if len(state.num_string) <= 16 or depth == 0:
        return utility(starting_player, state.points, state.bank)
    if len(state.num_string) <= 10:
        return heiristiska_novertejuma_funkcija_dziļumam(starting_player, state.points, state.bank)

    if maximizing_player:
        max_eval = float('-inf')
        for action in possible_actions:
            new_num_string, updated_points, updated_bank, level = action  
            new_state = Node(state.id, "".join(new_num_string), updated_points, updated_bank, state.level + 1)
            eval = alpha_beta_minmax(new_state, depth - 1, alpha, beta, False, num_string, starting_player)  
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta nogriešana
        return max_eval
    else:
        min_eval = float('inf')
        for action in possible_actions:
            new_num_string, updated_points, updated_bank, level = action  
            new_state = Node(state.id, "".join(new_num_string), updated_points, updated_bank, state.level + 1)
            eval = alpha_beta_minmax(new_state, depth - 1, alpha, beta, True, num_string, starting_player)  
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alfa nogriešana
        return min_eval
    
# Funkcija, kas izvēlas labāko iespējamo datora gājienu, balstoties uz heuristiku
def best_computer_move(num_string, points, bank, starting_player, algorithm):
    node = Node("N.0.1", num_string, points, bank, 0)  # Izveido sākuma virsotni
    tree = Tree(max_level=5)  # Izveido koku ar ierobežotu dziļumu
    tree.insert_node(node)  # Pievieno saknes virsotni kokam
    actions = generate_tree(node, tree)  # Ģenerē visus iespējamos nākamos stāvokļus

    best_score = float('-inf')  # Sākotnēji labākais rezultāts ir ļoti zems
    best_action = None  # Saglabās labāko atrasto darbību

    for action in actions:
        new_str, new_points, new_bank, _ = action  # Atrod nākamo stāvokli
        new_node = Node("tmp", "".join(new_str), new_points, new_bank, 1)  # Izveido pagaidu virsotni

        # Izvērtē stāvokli ar izvēlēto algoritmu
        if algorithm == "minimax":
            score = heiristiska_novertejuma_funkcija_dziļumam(starting_player, new_points, new_bank)
        else:
            score = heiristiska_novertejuma_funkcija_dziļumam(starting_player, new_points, new_bank)

        # Saglabā labāko gājienu
        if score > best_score:
            best_score = score
            best_action = action

    return best_action  # Atgriež labāko izvēlēto gājienu
  
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
    num_string = generate_num_string()  # Ģenerējam skaitļu virkni
    algoritma_izvele = which_alg()  # Izvēlamies algoritmu
    starting_player = kurs_sak()

    print("Sākotnējā virkne:", num_string)

    root = Node("N.0.1", num_string, 0, 0, 0)

    if algoritma_izvele == "minimax":
        if starting_player == "dators":
            minimax(root, True, starting_player, 0, 0)
        else:
            minimax(root, False, starting_player, 0, 0)
    else:
        if starting_player == "dators":
            alpha_beta_minmax(root, depth=10, alpha=float('-inf'), beta=float('inf'), maximizing_player=True, num_string=num_string, starting_player=starting_player)
        else:
            alpha_beta_minmax(root, depth=10, alpha=float('-inf'), beta=float('inf'), maximizing_player=False, num_string=num_string, starting_player=starting_player)

    print("Kods Galā")
    
# --------------------------------GUI-----------------------------------------------
# Klase, kas veido spēles galveno ekrānu un ļauj veikt gājienus
class GameScreen:
    def __init__(self, root, num_string, starting_player, algorithm):
        self.root = root  # Galvenais tkinter logs
        self.algorithm = algorithm  # Izvēlētais algoritms
        self.starting_player = starting_player  # Kurš sāk spēli
        self.current_string = list(num_string)  # Skaitļu virkne kā saraksts
        self.points = 0  # Sākotnējie punkti
        self.bank = 0  # Sākotnējā banka
        self.player_turn = (starting_player == "cilvēks")  # True, ja cilvēks sāk

        self.frame = tk.Frame(self.root)  # Galvenais spēles ietvars
        self.frame.pack()

        self.status_label = tk.Label(self.frame, text="", font=("Helvetica", 12))  # Informācija par gājienu
        self.status_label.pack(pady=5)

        self.string_frame = tk.Frame(self.frame)  # Ietvars virknes attēlošanai
        self.string_frame.pack()

        self.stats_label = tk.Label(self.frame, text="")  # Parāda punktus un banku
        self.stats_label.pack(pady=5)

        self.refresh_ui()  # Uzzīmē sākuma ekrānu

    # Atjauno spēles ekrānu pēc katra gājiena
    def refresh_ui(self):
        for widget in self.string_frame.winfo_children():
            widget.destroy()  # Notīra iepriekšējo virkni

        # Izveido pogas katram skaitļu pārim
        for i in range(len(self.current_string)-1):
            btn = tk.Button(self.string_frame, text=f"{self.current_string[i]} {self.current_string[i+1]}", command=lambda i=i: self.player_move(i))
            btn.grid(row=0, column=i, padx=2)

        # Atjauno punktu un bankas informāciju
        self.stats_label.config(text=f"Virkne: {''.join(self.current_string)} | Punkti: {self.points} | Banka: {self.bank}")

        # Ja palicis tikai viens skaitlis, spēle beidzas
        if len(self.current_string) == 1:
            self.end_game()
        else:
            # Parāda, kurš tagad veic gājienu
            self.status_label.config(text="Tavs gājiens!" if self.player_turn else "Dators domā...")
            if not self.player_turn:
                self.root.after(1000, self.computer_move)  # Dators veic gājienu pēc nelielas pauzes

    # Apstrādā cilvēka izvēlēto gājienu
    def player_move(self, index):
        if not self.player_turn or index >= len(self.current_string)-1:
            return  # Ja nav cilvēka gājiens vai kļūdains indekss

        a = int(self.current_string[index])
        b = int(self.current_string[index+1])
        pair_sum = a + b

        # Aizvieto pārīti pēc spēles noteikumiem
        if pair_sum > 7:
            self.current_string[index] = "1"
            self.points += 1
        elif pair_sum < 7:
            self.current_string[index] = "3"
            self.points -= 1
        else:
            self.current_string[index] = "2"
            self.bank += 1

        self.current_string.pop(index+1)  # Noņem otru skaitli no virknes
        self.player_turn = False  # Pāriet pie datora gājiena
        self.refresh_ui()  # Atjauno skatu

    # Funkcija, kas izsauc datora gājienu
    def computer_move(self):
        move = best_computer_move("".join(self.current_string), self.points, self.bank, self.starting_player, self.algorithm)
        if move:
            self.current_string, self.points, self.bank, _ = move  # Atjauno stāvokli
        self.player_turn = True  # Pāriet atpakaļ pie cilvēka
        self.refresh_ui()

    # Funkcija, kas izvada rezultātu un atgriež sākuma ekrānu
    def end_game(self):
        winner = utility(self.starting_player, self.points, self.bank)

        # Noteic uzvarētāju
        if winner == 1:
            result = "Uzvar dators!" if self.starting_player == "dators" else "Tu uzvarēji!"
        elif winner == -1:
            result = "Tu uzvarēji!" if self.starting_player == "dators" else "Uzvar dators!"
        else:
            result = "Neizšķirts!"

        # Parāda rezultātu ziņojumā
        messagebox.showinfo("Spēles beigas", f"{result}\nVirkne: {''.join(self.current_string)}\nPunkti: {self.points}\nBanka: {self.bank}")

        # Atiestata GUI uz sākuma ekrānu
        for widget in self.root.winfo_children():
            widget.destroy()
        GameGUI(self.root)


        
# Klase, kas veido sākuma izvēlni ar lietotāja ievadi
class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Divspēlētāju Spēle")  # Logs nosaukums

        tk.Label(root, text="Spēles uzstādījumi", font=("Helvetica", 16)).pack(pady=10)  # Virsraksts

        # Ievade virknes garumam
        tk.Label(root, text="Virknes garums (15–25):").pack()
        self.length_entry = tk.Entry(root)
        self.length_entry.pack()

        # Izvēle – kurš sāk spēli
        tk.Label(root, text="Kurš sāk spēli:").pack(pady=5)
        self.starting_player = tk.StringVar(value="cilvēks")
        tk.Radiobutton(root, text="Cilvēks", variable=self.starting_player, value="cilvēks").pack()
        tk.Radiobutton(root, text="Dators", variable=self.starting_player, value="dators").pack()

        # Izvēle – kurš algoritms tiks izmantots
        tk.Label(root, text="Izvēlies algoritmu:").pack(pady=5)
        self.algorithm = tk.StringVar(value="minimax")
        tk.Radiobutton(root, text="Minimakss", variable=self.algorithm, value="minimax").pack()
        tk.Radiobutton(root, text="Alfa-beta", variable=self.algorithm, value="alfa-beta").pack()

        # Poga spēles sākšanai
        tk.Button(root, text="Sākt spēli", command=self.start_game).pack(pady=10)

    # Apstrādā sākuma formas datus un palaiž spēli
    def start_game(self):
        try:
            length = int(self.length_entry.get())  # Pārbauda, vai ievadīts skaitlis
            if not (15 <= length <= 25):
                raise ValueError
        except ValueError:
            messagebox.showerror("Kļūda", "Nepareizs cipars")  # Kļūda, ja nav derīgs ievads
            return

        num_string = ''.join(str(random.randint(1, 9)) for _ in range(length))  # Ģenerē virkni
        starting_player = self.starting_player.get()  # Saglabā izvēlēto spēlētāju
        algorithm = self.algorithm.get()  # Saglabā izvēlēto algoritmu

        # Notīra sākuma loga elementus
        for widget in self.root.winfo_children():
            widget.destroy()

        # Pāriet uz spēles ekrānu
        GameScreen(self.root, num_string, starting_player, algorithm)


if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()