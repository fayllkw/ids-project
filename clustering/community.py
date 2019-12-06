import networkit as nk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.width', 320)
pd.set_option('display.max_columns', None)

import warnings
warnings.simplefilter("ignore", UserWarning)

""" Community Detection for a single year """
def get_communities(year, threshold, drop):
    # detect community
    G = nk.graphio.readGraph(
        "../data/similarity_graph/network_{}_{:.2f}_drop{}.graph".format(year, threshold, drop),
        nk.Format.EdgeList, separator=",", firstNode=0)
    G.removeSelfLoops()
    plp_communities = nk.community.PLP(G).run().getPartition()
    subsetSizes = {k: v for k,v in plp_communities.subsetSizeMap().items() if v > 10}
    standalone = {k: v for k,v in plp_communities.subsetSizeMap().items() if v == 1}
    print("{} threshold, {} communities, of which {} have more than 10 members, "
          "and of which {} only have 1 member".format(
        threshold, len(plp_communities.getSubsetIds()), len(subsetSizes),
        len(standalone)))

    # Output for visualization
    stats = pd.read_csv("../data/processed/seasons_stats_{}.csv".format(year))
    plp_communities.compact()  # change subset IDs to be consecutive, starting at 0
    stats["Group"] = plp_communities.getVector()
    stats["Merged_Group"] = stats["Group"]  # merge small clusters!!!
    few_index = stats.groupby('Group').filter(lambda x: x['Player'].count() <= 10).index  # player in small clusters
    stats.loc[few_index, "Merged_Group"] = "placeholder"
    unique_groups = stats["Merged_Group"].unique()
    unique_groups = np.delete(unique_groups, np.argwhere(unique_groups=="placeholder"))
    mapping = {group: idx+1 for idx, group in enumerate(unique_groups)}
    mapping["placeholder"] = 0
    stats["Merged_Group"] = stats["Merged_Group"].apply(lambda x: mapping[x])

    clusters = stats.groupby('Group')['Player'].aggregate(lambda x: ",".join(x)).reset_index()
    clusters.to_csv("../data/clusters/cluster_{}_{:.2f}_drop{}.csv".format(year, threshold, drop), index=False)
    stats.to_csv("../data/processed/seasons_stats_{}_{:.2f}_drop{}_with_group.csv".format(year, threshold, drop), index=False)

    return len(plp_communities.getSubsetIds()), len(subsetSizes), len(standalone)

threshold = 0.9
drop = True
community_nums = []
large_community_nums = []
standalone_nums = []
for year in range(1987, 2018):
    print(year)
    a, b, c = get_communities(year, threshold, drop)
    community_nums.append(a)
    large_community_nums.append(b)
    standalone_nums.append(c)

over_years = pd.DataFrame(
    {'Year': range(1987, 2018), 'Communities': community_nums,
     'More_than_10': large_community_nums, 'Only_one':standalone_nums})
over_years.to_csv(
    "../data/community_counts_{:.2f}_drop{}.csv".format(threshold, drop),
    index=False)

plt.figure()
plt.plot(range(1987, 2018), over_years.Communities)
plt.plot(range(1987, 2018), over_years.More_than_10)
plt.title("community_counts_{:.2f}_drop{}.csv".format(threshold, drop))
plt.show()
