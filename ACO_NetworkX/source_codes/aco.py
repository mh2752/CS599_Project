from source_codes.single_ant import SingleAnt
import networkx as nx
from random import randint
import numpy as np
import random

# -------------------------- Global variables -----------------------------------------------
# The adjacency matrix as a dictionary:
dist = {}

# Vector containing nodes:
graph_nodes = []

# The pheromone matrix as a dictionary:
pheromone = {}

# Choice info matrix as a dictionary
choice_info = {}

# m is the number of ants:
m = 0
# n is the number of cities:
n = 0
# list for containing m number of artificial ants:
ant = []

# Number of iterations for finding the optimal solution:
max_num_of_iteration = 0

# Evaporation rate:
rate_of_evaporation = 0.0

# Alpha controls the effect of pheromone.
# Default value is 1 as recommended in the ACO book (pg-71).
alpha = 1

# Beta controls the effect of heuristics. Giving a default
# value 2.5 which is in the recommended range [2,5].
beta = 2.5


# -------------------------------- End of Global Variables ----------------------


###################### Helper Functions to the Main Optimization Function ##################

# ------------- Function for getting index of the graph node ---------
def get_node_index(node):
    index = 0
    while graph_nodes[index] != node:
        index += 1
    return index


# -------------- Function for converting adjacency matrix to a dictionary -------
def adj_mat_to_dictionary(adj_mat):
    # --- Global variable for modification --------
    global dist
    # ---------------------------------------------
    for u in graph_nodes:
        for v in graph_nodes:
            if u != v:
                u_index = get_node_index(u)
                v_index = get_node_index(v)
                dist[(u, v)] = adj_mat[u_index, v_index]
    return


# ----------------------------------------------------------------


# -------------- as_decision_rule() Function ----------------------------------
def as_decision_rule(k, i):
    # ---- Global Variables Block Needed for Modifying ----------
    global ant
    # --------------------------------------------------------------

    # Getting current city of the ant:
    c = ant[k].tour[i - 1]
    c_index = get_node_index(c)

    sum_probabilities = 0.0

    selection_probability = {}

    for j in graph_nodes:
        j_index = get_node_index(j)
        if ant[k].visited[j_index]:
            selection_probability[j] = 0.0
        else:
            selection_probability[j] = choice_info[(c, j)]
            sum_probabilities += selection_probability[j]

    r = random.uniform(0, sum_probabilities)
    index = 0
    j = graph_nodes[index]
    p = selection_probability[j]

    while p < r:
        index += 1
        j = graph_nodes[index]
        p += selection_probability[j]
    '''
    if k == 0:
        print("--------- Ant 0 Start ------------")
        print("Step Number: ", i)
        print("Current city: ", graph_nodes[c_index])
        print("ant[k].visited: ", ant[k].visited)
        print("selection prob.: ", selection_probability)
        print("random value: ", r)
        print("value of p: ", p)
        print("Selected city: ", graph_nodes[index])
        print("----------- Ant 0 End ------------")
    '''

    ant[k].tour[i] = graph_nodes[index]
    ant[k].visited[index] = True


# ---------- End of as_decision_rule() --------------------------------------


# ------------- Function for computing tour length ----------------------------
def compute_tour_length(k):
    # ---- Global Variables Block Needed for Modifying ----------
    global ant
    global choice_info
    # --------------------------------------------------------------
    temp_tour_length = 0
    index = 0

    kth_ant = ant[k]

    while index < n:
        node_u = kth_ant.tour[index]
        node_v = kth_ant.tour[index + 1]

        temp_dist = dist[(node_u, node_v)]  # Getting distance from the adjacency matrix
        temp_tour_length += temp_dist
        index += 1

    return temp_tour_length


# -------------- End of compute_tour_length() ------------------------


# ----------- Function for constructing the solution: ----------------------
def construct_solutions():
    # --------- Global variables for modification -------------
    global ant
    # ---------------------------------------------------------

    # Resetting ants' visited data:
    for k in range(0, m):
        last_city = 0
        for i in range(0, n):
            ant[k].visited[i] = False
            ant[k].tour[i] = None
            last_city = i
        ant[k].tour[last_city] = None

    step = 0
    # Placing each ant in random starting nodes:
    for k in range(0, m):
        r = randint(0, (n - 1))
        ant[k].tour[step] = graph_nodes[r]
        ant[k].visited[r] = True

    while step < n:
        step += 1
        for k in range(0, m):
            as_decision_rule(k, step)

    for k in range(0, m):
        ant[k].tour[n] = ant[k].tour[0]
        ant[k].tour_length = compute_tour_length(k)


# --------------- End of construct_solutions() ---------------------


# ------------- Function for evaporating pheromone levels -------------
def evaporate():
    # ------- Global variable for modification ---------
    global pheromone
    # --------------------------------------------------

    for i in graph_nodes:
        for j in graph_nodes:
            if i != j:
                pheromone[(i, j)] = (1 - rate_of_evaporation) * pheromone[(i, j)]
                pheromone[(j, i)] = pheromone[(i, j)]


# ------------------ End of evaporate() -----------------------------------


# ------------------ Function for depositing pheromone ----------------------
def deposit_pheromone(k):
    # -------------- Global variable for modification -------------
    global pheromone
    # ---------------------------------------------------------------
    # k identifies the specific instance of ant in the 'ant' list

    # Depositing pheromone only if the ant has traveled some distance:
    if ant[k].tour_length != 0:
        tau = 1 / ant[k].tour_length
        for i in range(0, n):
            j_node = ant[k].tour[i]
            l_node = ant[k].tour[i + 1]
            pheromone[(j_node, l_node)] = pheromone[(j_node, l_node)] + tau
            pheromone[(l_node, j_node)] = pheromone[(j_node, l_node)]


# ------------------ End of deposit_pheromone() ----------------------------


# ------------------ Function for computing choice information -----------
def compute_choice_information():
    # ------------- Global variable for modification ---------------
    global choice_info
    # ---------------------------------------------------------------
    for i in graph_nodes:
        for j in graph_nodes:
            if i != j:
                d_ij = dist[(i, j)]
                tau_ij = pheromone[(i, j)]
                ita_ij = 1.0 / d_ij
                choice_info[(i, j)] = pow(tau_ij, alpha) * pow(ita_ij, beta)


# ------------------- End of compute_choice_information() -----------------


# ---------------- Function for updating pheromone trails: ------------
def update_pheromone_trails():
    evaporate()

    for k in range(0, m):
        deposit_pheromone(k)

    compute_choice_information()


# ----------------- End of update_pheromone_trails() ------------------


############################# Main Optimization Function Below ############################

def ant_colony_optimization(graph_object, num_ant, num_of_iter, evap_rate, alpha_value, beta_value):
    # ---- Global Variables Block Needed for Modifying ----------
    global n
    global dist
    global graph_nodes
    global m
    global ant
    global pheromone
    global choice_info
    global max_num_of_iteration
    global rate_of_evaporation
    global alpha
    global beta
    # --------------------------------------------------------------

    # --------------- InitializeData Portion ------------------------

    # n is number of nodes in the graph:
    n = len(graph_object.nodes())

    # Getting the nodes list:
    graph_nodes = list(graph_object.nodes())

    # Converting the adjacency matrix to a dictionary format:
    adj_mat_to_dictionary(nx.adjacency_matrix(graph_object))

    # m is the number of artificial ants:
    m = num_ant

    # Setting max. number of iteration for finding optimal solution:
    max_num_of_iteration = num_of_iter

    # Setting pheromone evaporation rate:
    rate_of_evaporation = evap_rate

    # Setting alpha and beta values to user-defined values:
    alpha = alpha_value
    beta = beta_value

    # Creating and appending m number of ants to the 'ant' list:
    for a in range(0, m):
        x = SingleAnt(n)
        ant.append(x)

    # Creating and initializing pheromone matrix:
    # pheromone = [[0.1] * n] * n  # It's an n-by-n matrix
    for u in graph_nodes:
        for v in graph_nodes:
            if u != v:
                pheromone[(u, v)] = 0.1

    # Creating and initializing choice_info matrix:
    # choice_info = [[0.0] * n] * n  # It's also an n-by-n matrix
    for u in graph_nodes:
        for v in graph_nodes:
            if u != v:
                choice_info[(u, v)] = 0.0

    # initializing choice_info matrix
    compute_choice_information()
    # ---------------- InitializeData Portion Ends --------------------------------

    # -------------------- Executing the Optimal Solution Finding Steps -----------
    counter = 0
    while counter < max_num_of_iteration:
        construct_solutions()
        update_pheromone_trails()
        counter += 1
    # ------------------------------------------------------------------------------

    # ------------------------ Returning all the Optimal Solutions ------------------
    # ------------------------ Found by m Number of Ants ----------------------------

    return_tour_list = []
    return_tour_cost_list = []

    # ------- Preparing final result ------------------------------------------------
    for i in range(0, m):
        return_tour_list.append(ant[i].tour)
        return_tour_cost_list.append(ant[i].tour_length)

    # ------------- Resetting all global variables ---------------------------------
    dist = {}
    graph_nodes = []
    pheromone = {}
    choice_info = {}
    m = 0
    n = 0
    ant = []
    max_num_of_iteration = 0
    rate_of_evaporation = 0.0
    alpha = 0
    beta = 0
    # ------------------------------------------------------------------------------

    # Returning the two lists containing the m number of
    # ants' optimized tour info:
    return return_tour_list, return_tour_cost_list
