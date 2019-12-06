import networkit as nk
import pandas as pd
pd.set_option('display.width', 320)
pd.set_option('display.max_columns', None)

import warnings
warnings.simplefilter("ignore", UserWarning)

""" Community Detection for a single year """
year = 2017
threshold = 0.88
G = nk.graphio.readGraph(
    "../data/similarity_graph/network_{}_{}.graph".format(year, threshold),
    nk.Format.EdgeList, separator=",", firstNode=0, continuous=True)
plp_communities = nk.community.PLP(G).run().getPartition()
subsetSizes = {k: v for k,v in plp_communities.subsetSizeMap().items() if v > 5}
standalon = {k: v for k,v in plp_communities.subsetSizeMap().items() if v == 1}
print("%f threshold, %d communities, of which %d have more than 5 members, "
      "and of which %d only have 1 member" % (
    threshold, len(plp_communities.getSubsetIds()),
    len(subsetSizes), len(standalon)
    ))

# Output for visualization
stats = pd.read_csv("../data/processed/seasons_stats_{}.csv".format(year))
stats["Group"] = plp_communities.getVector()
clusters = stats.groupby('Group')['Player'].aggregate(lambda x: ",".join(x)).reset_index()
clusters.to_csv("../data/clusters/cluster_{}_{}.csv".format(year, threshold), index=False)
stats.to_csv("../data/processed/seasons_stats_{}_{}_with_group.csv".format(year, threshold), index=False)

# output_nodes = []
# node_id_map = dict()
# file = open("../data/R_links.csv", 'w')
# file.write("{},{},{}\n".format("source", "target", "value"))
# for i in range(X.shape[0]):
#     for j in range(i + 1, X.shape[0]):
#         if sim_mat[i][j] > 0.9997:
#             if i not in output_nodes:
#                 node_id_map[i] = len(output_nodes)
#                 output_nodes.append(i)
#             if j not in output_nodes:
#                 node_id_map[j] = len(output_nodes)
#                 output_nodes.append(j)
#             file.write("{},{},{}\n".format(node_id_map[i], node_id_map[j], 10000 * (1 - sim_mat[i][j])))
# file.close()
#
# sorted_nodes = sorted(node_id_map.items(), key=lambda x: x[1])
# file = open("../data/R_nodes.csv", "w")
# file.write("{},{},{}\n".format("name", "group", "3P%"))
# for item in sorted_nodes:
#     node = item[0]
#     file.write("{},{},{}\n".format(subdf.loc[node]["Player"], subdf.loc[node]["Group"], subdf.loc[node]["3P%"]))
# file.close()
