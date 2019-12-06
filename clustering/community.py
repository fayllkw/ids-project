import networkit as nk
import pandas as pd
import numpy as np
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
subsetSizes = {k: v for k,v in plp_communities.subsetSizeMap().items() if v > 10}
standalon = {k: v for k,v in plp_communities.subsetSizeMap().items() if v == 1}
print("{} threshold, {} communities, of which {} have more than 10 members, "
      "and of which {} only have 1 member".format(
    threshold, len(plp_communities.getSubsetIds()),
    len(subsetSizes), len(standalon)
    ))

# Output for visualization
stats = pd.read_csv("../data/processed/seasons_stats_{}.csv".format(year))
plp_communities.compact()  # change subset IDs to be consecutive, starting at 0
stats["Group"] = plp_communities.getVector()
stats["Merged_Group"] = stats["Group"]  # merge small clusters!!!
few_index = stats.groupby('Group').filter(lambda x: x['Player'].count() < 10).index  # player in small clusters
stats.loc[few_index, "Merged_Group"] = "placeholder"
unique_groups = stats["Merged_Group"].unique()
unique_groups = np.delete(unique_groups, np.argwhere(unique_groups=="placeholder"))
mapping = {group: idx+1 for idx, group in enumerate(unique_groups)}
mapping["placeholder"] = 0
stats["Merged_Group"] = stats["Merged_Group"].apply(lambda x: mapping[x])

clusters = stats.groupby('Group')['Player'].aggregate(lambda x: ",".join(x)).reset_index()
clusters.to_csv("../data/clusters/cluster_{}_{}.csv".format(year, threshold), index=False)
stats.to_csv("../data/processed/seasons_stats_{}_{}_with_group.csv".format(year, threshold), index=False)
