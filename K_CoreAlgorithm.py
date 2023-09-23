import numpy as npy
import networkx as ntwx
import matplotlib.pyplot as matplt

# Task -1: Function to implement the k-core algorithm to find the k neighbors
def k_Algorithm(mtrx, k):
    
    matlen = len(mtrx)
    nodeDegree = npy.sum(mtrx, axis=1)
    
    rem_nodes = [i for i in range(matlen) if nodeDegree[i] < k]
    
    subgraph = []
    for i in range(matlen):
        if i not in rem_nodes:
            row = []
            for j in range(matlen):
                if j not in rem_nodes:
                    row.append(mtrx[i][j])
            subgraph.append(row)
    
    subDeg = [sum(subgraph[i]) for i in range(len(subgraph))]
    if not any([d < k for d in subDeg]) or not subgraph:
        return [l for l in range(matlen) if l not in rem_nodes]
    else:
        return k_Algorithm(subgraph, k)

# Task - 2: Generate the adjacency matrix from the given UTD Student ID.
def genAdjacencyMatrix(uid):
    
    bitSeq = ''
    for i in uid:
        if int(i) % 2 == 1:
            bitSeq += '1'
        else:
            bitSeq += '0'
    bitSeq *= 73

    totalRw = 27
    totalCl = 27
    adjMatrx = [[0 for j in range(totalCl)] for i in range(totalRw)]

    for row in range(totalRw):
        fIndex = row*totalCl
        lIndex = fIndex + totalCl
        bin_Numbers = bitSeq[fIndex:lIndex]
        dcml_Numbers = [int(b, 2) for b in bin_Numbers]
        adjMatrx[row] = dcml_Numbers

    for i in range(totalRw):
        if npy.sum(adjMatrx[i]) == 0:
            adjMtrx[i][0] = adjMatrx[i][-1] = adjMtrx[0][i] = adjMatrx[-1][i] = 1
        adjMatrx[i][i] = 0
        for j in range(i):
            adjMatrx[i][j] = adjMatrx[j][i]

    return adjMatrx

# Task - 3: Perform k-core algorithm for k-values from 1 to 27 on the adjacency matrix generated from student id.
def get_nodes(adjMtrx):
    nodes = {}
    for k in range(1, 28):
        nodes[k] = k_Algorithm(adjMtrx, k)
        if nodes[k]:
            print(f'For k={k} Nodes in the cluster:{nodes[k]}')


# Task - 4: Generate the graph for the edges obtained for k-nodes from all k-values from 1 to 27 
def get_edges(clstr_nodes, adjMtrx):
    edges = []
    for i in clstr_nodes:
        for j in clstr_nodes:
            if i < j and adjMtrx[i][j] == 1:
                edges.append((i, j))
    return edges


def genGraph(adjMtrx):
    clstr_edges = []
    for k in range(1, 28):
        nodes = k_Algorithm(adjMtrx, k)
        if len(nodes) > 0:
            clstr_edges += get_edges(nodes, adjMtrx)

    Clstr = ntwx.Graph()
    Clstr.add_edges_from(clstr_edges)

    p = ntwx.spring_layout(Clstr)
    ntwx.draw_networkx_edges(Clstr, p)
    ntwx.draw_networkx_labels(Clstr, p)
    ntwx.draw_networkx_nodes(Clstr, p)

    matplt.axis('off')
    matplt.show()

# Task - 5: Remove random edges and perform all the the previous tasks.
def rem_EdgeFunc(amt, delEdges):
    
    for i,j in delEdges:
        amt[i][j] = 0
        amt[j][i] = 0
        
        get_nodes(amt)
        genGraph(amt)
        
        amt[i][j] = 1
        amt[j][i] = 1

        
if __name__ == '__main__':
    
    ID = "2021594665"
    Matrix = genAdjacencyMatrix(ID)
    
    get_nodes(Matrix)
    genGraph(Matrix)
    
    delEdges = [(2, 15), (8, 19), (18, 23), (24, 26)]
    rem_EdgeFunc(Matrix, delEdges)
