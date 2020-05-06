import networkx as nx
import dimod
import dwave_networkx.algorithms as dnx
from random import randint
from source_codes.aco import ant_colony_optimization

###################################################################################################

'''
The classical Travelling Salesman Problem expects a complete graph G = (E,V) to be undirected and
weighted where E = {Set of arcs/ edges of the graph} and N = {Set of all nodes of the graph} and 
|E| = N*(N-1)/2 where N = Number of elements in the set V = |V| (because, G is undirected).


The program here tests the efficacy of the developed ant colony optimization module in solving the 
TSP against two known algorithms:
                                (i) NetworkX's Hamiltonian Path Algorithm
                                (ii) D-Wave NetworkX's implementation of the TSP Algorithm 
'''


############################## Trivial Helper Functions. Can Skip to Next Section ##################

# Function for getting the index of a node in the list of nodes:
def get_node_index(node_list, node):
    temp_index = 0
    while node_list[temp_index] != node:
        temp_index += 1
    return temp_index


# -------------------------------------------------------------------------------------------------

# Function for creating and returning a dictionary
# with the adjacency information of the given
# graph object:
def adj_mat_to_dictionary(GraphObj):
    graph_nodes = list(GraphObj.nodes())
    adj_mat = nx.adjacency_matrix(GraphObj)
    dist = {}

    for u in graph_nodes:
        for v in graph_nodes:
            if u != v:
                u_index = get_node_index(graph_nodes, u)
                v_index = get_node_index(graph_nodes, v)
                dist[(u, v)] = adj_mat[u_index, v_index]
    return dist


# -------------------------------------------------------------------------------------------------

############################# End of Trivial Helper Functions #####################################


################################# Creating Sample Graphs ##########################################

# ------------- A complete, undirected & weighted graph with N = 4 -------------
G = nx.Graph()
G.add_edge('a', 'b', weight=3)
G.add_edge('a', 'c', weight=2)
G.add_edge('a', 'd', weight=12)
G.add_edge('b', 'c', weight=6)
G.add_edge('b', 'd', weight=7)
G.add_edge('d', 'c', weight=9)
# -------------------------------------------------------------------------------

# ----------------- A complete, undirected & weighted graph with N = 5 -----------

G2 = nx.Graph()

G2.add_edge('a', 'b', weight=8)
G2.add_edge('a', 'c', weight=6)
G2.add_edge('a', 'd', weight=17)
G2.add_edge('a', 'e', weight=5)
G2.add_edge('b', 'c', weight=9)
G2.add_edge('b', 'd', weight=13)
G2.add_edge('b', 'e', weight=11)
G2.add_edge('c', 'd', weight=9)
G2.add_edge('c', 'e', weight=2)
G2.add_edge('d', 'e', weight=2)

# ---------------------------------------------------------------------------------

# ------------------- A Directed, complete & weighted graph ----------------------
# ------------------- with adjustable number of nodes ------------------------------------------

G3 = nx.DiGraph()
n = 15
for u in range(0, n):
    for v in range(0, n):
        if u != v:
            node_u = str(u)
            node_v = str(v)
            w = randint(1, 100)
            G3.add_edge(node_u, node_v, weight=w)

# ------------------------------------------------------------------------------------

########################### End of Sample Graph Creation ############################################


################ Initializing the Parameters for Calling thr Ant Colony Optimization Function ########
max_iteration = 100
pheromone_evaporation_rate = 0.15  # 15% evaporation rate
alpha = 1
beta = 2.5
############################## End of Parameter Initialization #########################################


####################################### Testing Against NetworkX Algorithms ############################


print("################# Ant Colony Optimization Vs. NetworkX's Hamiltonian Path Algorithm #############\n")

# Format for calling the Ant Colony Optimization function
# is:
# ant_colony_optimization(Graph_Object,
#                       Number_Of_Artificial_Ants,
#                       Max_Number_Of_Optimization_Iteration,
#                       Pheromone_Evaporation_Rate,
#                       Alpha, Beta)
#
# The function will return two lists containing optimized tour info (node sequence and tour cost) performed
# by the specified number of artificial ants in the function call below:

tour_node_list, tour_cost_list = ant_colony_optimization(G3,
                                                         len(list(G3.nodes())),
                                                         max_iteration,
                                                         pheromone_evaporation_rate,
                                                         alpha, beta)

print("-------- Optimized Routes by Ant Colony Optimization ---------------------")
index = 0
while index < len(tour_node_list):
    print("Optimized Tour - ", (index + 1), ": ", tour_node_list[index])
    print("Optimized Tour Cost: ", tour_cost_list[index], "\n")
    index += 1

print("---------------------------------------------------------------------------\n")

print("---------- Output from NetworkX Tournament Hamiltonian Path Algorithm: -------")

nx_ham = nx.algorithms.tournament.hamiltonian_path(G3)

index = 0
adj_dict = adj_mat_to_dictionary(G3)
path_cost = 0

while index < len(nx_ham):

    if index < len(nx_ham) - 1:
        node_a = nx_ham[index]
        node_b = nx_ham[index + 1]
        path_cost += adj_dict[(node_a, node_b)]
        # print("Node: ", node_a, " to Node: ", node_b, " = ", adj_dict[(node_a, node_b)])


    else:
        node_a = nx_ham[index]
        node_b = nx_ham[0]
        path_cost += adj_dict[(node_a, node_b)]
        # print("Node: ", node_a, " to Node: ", node_b, " = ", adj_dict[(node_a, node_b)])

    index += 1

print("Sequence of Nodes: ", nx_ham)
print("Path Cost (considering connecting last and first node visited): ", path_cost)

print("##################################################################################################\n")

print("######## Ant Colony Optimization Vs. TSP Algorithm Implemented in Dwave-NetworkX ###################\n")

tour_node_list2 = []
tour_cost_list2 = []

tour_node_list2, tour_cost_list2 = ant_colony_optimization(G,
                                                           len(list(G.nodes())),
                                                           max_iteration,
                                                           pheromone_evaporation_rate,
                                                           alpha, beta)

print("-------- Optimized Routes by Ant Colony Optimization ---------------------")
print(len(tour_node_list2))
index = 0
while index < len(tour_node_list2):
    print("Optimized Tour - ", (index + 1), ": ", tour_node_list2[index])
    print("Optimized Tour Cost: ", tour_cost_list2[index], "\n")
    index += 1

print("---------------------------------------------------------------------------\n")

print(" ------------------ D-Wave NetworkX Traveling Salesman Algorithm --------------")

tsp_dwave = dnx.traveling_salesman(G, dimod.ExactSolver())

index = 0
adj_dict = adj_mat_to_dictionary(G)
path_cost = 0

while index < len(tsp_dwave):

    if index < len(tsp_dwave) - 1:
        node_a = tsp_dwave[index]
        node_b = tsp_dwave[index + 1]
        path_cost += adj_dict[(node_a, node_b)]
        # print("Node: ", node_a, " to Node: ", node_b, " = ", adj_dict[(node_a, node_b)])


    else:
        node_a = tsp_dwave[index]
        node_b = tsp_dwave[0]
        path_cost += adj_dict[(node_a, node_b)]
        # print("Node: ", node_a, " to Node: ", node_b, " = ", adj_dict[(node_a, node_b)])

    index += 1

print("Sequence of Nodes: ", tsp_dwave)
print("Path Cost (considering connecting last and first node visited): ", path_cost)

print("\n##################################################################################################")
