import time
import random


#Moteur de Jeu de la Machine :
def successors(s):
  #Répartir les données du programmes principale pour le traitement de la machine
    player = s[-1] #On place le numero du joeur dans la position (-1) dans la liste
    piles = s[0] #On place La liste consitué de piles dans la position (1) dans la liste
    successor_states = []
    successors = []

  #Lorsque c'est le tour de la machine on alterne sur le joueur pour le prochain tour
    if player == 1:
        player = 2
    if player == 2:
        player == 1
    for i, pile in enumerate(piles):
        if pile < 3 :
            j = 1 
        else :
            ran=round(pile/2) #la moitié de la pile
            for remove in range(1, ran+1):
                    result = pile - remove
                    if result != 0:
                        next_piles = sorted(piles[:i] + [result] + piles[i+1:])
                    else:
                        next_piles = sorted(piles[:i] + piles[i+1:])
                    next_piles.append(remove)
                    successor_states.append(next_piles)
    import itertools
    successor_states.sort()
    successor_states = list(successor_states for successor_states, _ in itertools.groupby(successor_states))
    for i in range(len(successor_states)):
        successors.append([successor_states[i], player])
    return successors

#Une fonction pour determiner quand est ce qu' on arrive à un état final
def terminal_test(state):
    terminal_state = False
    for i in state[0] :
        if i < 3:
            terminal_state = True
    return terminal_state

#attribuer des valeurs heuristique (-1,1)
def utility_test(state):
    for i in state[0] :
        if i < 3 :
            utility = 1
        else:
            utility = -1
    return utility

#Retourner la valeur maximale(pour minimax)
def max_value(max_state):
    v = 1
    terminal_state, utility = terminal_test(max_state)
    if not terminal_state:
        for s in successors(max_state):
            v = min(v, min_value(s))
        return v
    else:
        return terminal_test(max_state)
#Retourner la valeur minimale(pour minimax)

def min_value(min_state):
    v = -1
    terminal_state, utility = terminal_test(min_state)
    if not terminal_state:
        for s in successors(min_state):
            v = max(v, max_value(s))
        return v
    else:
        return terminal_test(min_state)

#fonction minimax
def min_max(state):
    if state[1] == 1:
        utility = max_value(state)
    else:
        utility = min_value(state)
    if utility == 1:
        print("Max")
    if utility == -1:
        print("Min")
    return utility

#La valeur maximale (pour Alphabeta)
def max_value_ab(min_state, a, b):
    v = 1
    terminal_state = terminal_test(min_state)
    utility = utility_test(min_state)
    if not terminal_state:

        for s in successors(min_state):

            if v > utility:
                utility = v
            if v >= b:
                return utility
            if v > a:
                a = v
        v = min(v, min_value_ab(min_state, a, b))
    return utility

#La valeur minimale pour Alphabeta
def min_value_ab(max_state, a, b):
    v = -1
    terminal_state = terminal_test(max_state)
    utility = utility_test(max_state)
    if not terminal_state:

        for s in successors(max_state):

            if v < utility:
                utility = v
            if v <= a:
                return utility
            if v < b:
                b = v
        v = max(v, max_value_ab(max_state, a, b))

    return utility

#fonction minimax améliorée : Alpha Beta
def AlphaBeta(state):
    start = time.time()
    alpha = 0
    beta = 0
    if state[1] == 1:
        utility_value = min_value_ab(state, alpha, beta)

    else:
        utility_value = max_value_ab(state, alpha, beta)
    end = time.time()

    return utility_value

#Corps principale du Jeu
def main():
    #Incrémenter le nombre de pile et rajouter au fur et à mesures
    number_of_piles = int("1")
    maximum_pile_size = int(input("Nombre de Jetons: "))
    first_player = int(input("Qui commence : (1) l'ordinateur, (2) Le Joueur : "))
    initial_piles = []
    for pile in range(0, number_of_piles):
        pile_size = maximum_pile_size
        initial_piles.append(pile_size)
    state = (initial_piles, first_player)
    pile_stack = 1 #Cette valeur servira a bloquer le joueur lors d'un choix de pile qui n'existe pas.
    while True:
        # Definier le joueur (1 - Ordinateur) et (2 - Pour le joueur)
        if state[1] == 2:
            player = "Joueur"
        else:
            player = "Machine"
        #Afficher le dourelement du jeu actuellement.
        print("C'est le tour de :", player)
        print("********************* Etat *********************")
        Piles_s = state[0]
        p = 1
        for i in enumerate(Piles_s):
            print("Pile %s contient : " % (p), Piles_s[p-1], " Jetons")
            p = p + 1
        print("**************************************************\n")
        
        #Partie : Tour du Joueur
        if state[1] == 2:
            piles = state[0]
            while True :
                pile_number = (int(input("Selectionner le numéro de  la pile que vous allez diviser: ")) - 1)

                if (pile_number <= pile_stack) :
                    if piles[pile_number] < 3 :
                        print("Vous ne pouvez pas diviser cette pile ! Recommence")
                    else :
                        pile_stack = pile_stack + 1
                        break
                else :
                    print("Numéro de pile non-valide ! Recommence")

            pile = piles[pile_number]
            while True :
                pick = int(input("Nombre de jetons a déplacer: (Pas plus de la moitié)"))
                if pick < (pile/2):
                    piles[pile_number] = pile - pick
                    piles.append(pick)
                    state = (piles, 1)
                    break
                else:
                    print("Hors cible ! recommencez")
        #Partie Tour Machine
        elif state[1] == 1:
            list_of_successors = successors(state)
            number_of_next_states = len(list_of_successors)
            for s, next_state in enumerate(list_of_successors):
                utility_value = AlphaBeta(next_state)
                if utility_value == -1:
                    state = next_state
                elif utility_value == 1:
                    state = list_of_successors[random.randrange(0, number_of_next_states)]
                    state = next_state
        #Vérificateur fin de partie.
        ending = 1
        for j in state[0]:
            if j > 2 :
                ending = 0
        if ending == 1 :
            util = utility_test(state)
            print("Gagnant : ",player)
            break

        AlphaBeta(state)


main()
