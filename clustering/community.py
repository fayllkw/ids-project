import networkit as nk


""" Community Detection for a single year """
G = nk.graphio.readGraph("../data/nework.graph", nk.Format.EdgeListCommaOne)
communities = nk.community.detectCommunities(G)

# Output for visualization
# reset index to have continuous index for indexing back
subdf = subdf.reset_index()
subdf["Group"] = -1
for i in range(communities.numberOfSubsets()):
    for node in communities.getMembers(i):
        subdf.at[node, "Group"] = i


output_nodes = []
node_id_map = dict()
file = open("../data/R_links.csv", 'w')
file.write("{},{},{}\n".format("source", "target", "value"))
for i in range(X.shape[0]):
    for j in range(i + 1, X.shape[0]):
        if sim_mat[i][j] > 0.9997:
            if i not in output_nodes:
                node_id_map[i] = len(output_nodes)
                output_nodes.append(i)
            if j not in output_nodes:
                node_id_map[j] = len(output_nodes)
                output_nodes.append(j)
            file.write("{},{},{}\n".format(node_id_map[i], node_id_map[j], 10000 * (1 - sim_mat[i][j])))
file.close()

sorted_nodes = sorted(node_id_map.items(), key=lambda x: x[1])
file = open("../data/R_nodes.csv", "w")
file.write("{},{},{}\n".format("name", "group", "3P%"))
for item in sorted_nodes:
    node = item[0]
    file.write("{},{},{}\n".format(subdf.loc[node]["Player"], subdf.loc[node]["Group"], subdf.loc[node]["3P%"]))
file.close()
