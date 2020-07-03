import pandas as pd 
import numpy as np
from collections import defaultdict
import time

# 导入图的邻接矩阵，其中没有边的元素为空
Vmat = pd.read_excel("./图邻接矩阵.xlsx", encoding='unicode_escape')
Vmat = Vmat.drop(["Unnamed: 0"], axis = 1)
Vmat.index += 1
for i in range(1, Vmat.shape[0]+1):
    for j in range(i+1, Vmat.shape[1]+1):
        Vmat[i][j] = Vmat[j][i]

# 转换为三元组形式存储图结构
Edge = []
for i in range(1, Vmat.shape[0]+1):
    for j in range(i+1, Vmat.shape[1]+1):
        if pd.isnull(Vmat[i][j]) == False:
            Edge.append([i, j, Vmat[i][j]])

# Graph1类中包含基础的Kruskal和Prim算法
class Graph1(object):
    def __init__(self, maps):
        self.maps = maps
        self.nodenum = self.get_nodenum()
        self.edgenum = self.get_edgenum()
 
    # 计算顶点数
    def get_nodenum(self):
        return len(self.maps)
    
    # 计算边数
    def get_edgenum(self):
        count = 0
        for i in range(self.nodenum):
            for j in range(i):
                if self.maps[i][j] > 0 and np.isnan(self.maps[i][j]) == False:
                    count += 1
        return count

    # 基础Kruskal算法实现
    def kruskal(self):
        res = []
        if self.nodenum <= 0 or self.edgenum < self.nodenum-1:
            return res
        # 将各条边定点和边的信息加入edge_list中
        edge_list = []
        for i in range(self.nodenum):
            for j in range(i,self.nodenum):
                if np.isnan(self.maps[i][j]) == False:
                    edge_list.append([i+1, j+1, self.maps[i][j]])
        # 将各条边按权重排序
        edge_list.sort(key = lambda a:a[2])
        
        group = [[i+1] for i in range(self.nodenum)]
        for edge in edge_list:
            for i in range(1, len(group)+1):
                if edge[0] in group[i-1]:
                    m = i-1
                if edge[1] in group[i-1]:
                    n = i-1
            
            # 若不构成回路则添加边，并将结点标记为已遍历
            if m != n:
                res.append(edge)
                group[m] = group[m] + group[n]
                group[n] = []
        return res
    
    # Prim算法实现
    def prim(self):
        res = []
        if self.nodenum <= 0 or self.edgenum < self.nodenum-1:
            return res
        res = []
        seleted_node = [0]
        candidate_node = [i for i in range(1, self.nodenum)]
        
        # 循环逐步查找每个状态下的最小权值边
        while len(candidate_node) > 0:
            begin, end, minweight = 0, 0, 99999
            for i in seleted_node:
                for j in candidate_node:

                    # 选择当前状态最小权值的边
                    if self.maps[i][j] < minweight:
                        minweight = self.maps[i][j]
                        begin = i
                        end = j

            res.append([begin+1, end+1, minweight]) # 将当前最小权值边添加到最小生成树中
            seleted_node.append(end) # 将该顶点标记为已遍历
            candidate_node.remove(end) # 将该顶点移出带遍历集合
        return res

# Graph2类中包含使用并查集优化的Kruskal算法
class Graph2(object):
    def __init__(self):
        self.vertex = set()
        self.edge = []

    # 逐步添加边，u,v为边起始和终止顶点
    def add_edge(self, u, v, w):
        self.vertex.add(u)
        self.vertex.add(v)
        self.edge.append([u, v, w])

    # 使用循环查找父节点
    # 用parent来表示当前索引元素的祖先
    def find_parent(self, parent, i):
        j = i 
        while parent[j] != j:
            j = parent[j]
        x = i
        while x != j:
            y = parent[x]
            parent[x] = j
            x = y
        return x

    # 集合合并算法
    def union(self, parent, rank, x, y):
        x_set_flag = self.find_parent(parent, x)
        y_set_flag = self.find_parent(parent, y)
        
        # 选择大集合的树作为祖先以提高效率
        if rank[x_set_flag] < rank[y_set_flag]:
            parent[x_set_flag] = y_set_flag
        else:
            if rank[x_set_flag] == rank[y_set_flag]:
                # 若集合大小相等，则秩+1
                rank[x_set_flag] += 1
            parent[y_set_flag] = x_set_flag            

    # kruskal求最小生成树
    def kruskal_union_find(self):
        result = []
        i = 0
        e = 0
        # 将各条边按权重排序
        self.edge = sorted(self.edge, key=lambda x: x[2])
        parent = []
        rank = []
        for v in range(len(self.vertex)):
            parent.append(v)
            rank.append(0)

        while e < len(self.vertex) - 1:
            u, v, w = self.edge[i]
            i += 1

            x = self.find_parent(parent, u)
            y = self.find_parent(parent, v)

            # 不在一个集合中说明没有回路，则添加边
            if x != y: 
                e = e + 1
                result.append([u+1, v+1, w])
                self.union(parent, rank, x, y)  # 合并集合
        return result

# 执行基础Kruskal算法和Prim算法
graph = Graph1(np.array(Vmat))
print("Kruskal算法结果:\n",graph.kruskal())
print("\nPrim算法结果:\n", graph.prim())

# 执行经并查集优化的Kruskal算法
g = Graph2()
for e in Edge:
    g.add_edge(e[0]-1, e[1]-1, e[2])
mst = g.kruskal_union_find()
print("Kruskal算法+并查集优化结果:\n", mst)

# 计算各种算法运行时间
t0 = time.time()
graph.kruskal()
t1 = time.time()
graph.prim()
t2 = time.time()
g.kruskal_union_find()
t3 = time.time()
print(" Kruskal算法时间：{:.6f}\nPrim算法时间：{:.6f}\nKruskal算法+并查集优化时间：{:.6f}".format(t1-t0, t2-t1, t3-t2))