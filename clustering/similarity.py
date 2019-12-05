import networkit as nk
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
pd.set_option('display.width', 320)
pd.set_option('display.max_columns', None)

""" Some utility functions. """
def drop_multi_teams(df_year):
    """
    Remove the separate team record of a player who are traded during a season,
    and return a copy of the processed df.
    df_year: pandas data frame, including players stats of ONE season.
    Note: requires no different players with same name in input.
    """
    players_traded_in_season = df_year[df_year['Tm'] == 'TOT']['Player']
    drop_mask = (df_year['Player'].isin(players_traded_in_season)) & (
            df_year['Tm'] != 'TOT')
    return df_year[~drop_mask].copy().reset_index(drop=True)

""" Scripts of data processing """
# read
df = pd.read_csv("../data/seasons_stats.csv", index_col=0)
player = pd.read_csv("../data/player_data.csv")
# Drop blank rows and columns
df = df.dropna(axis=0, how="all")
df = df.drop(columns=["blanl", "blank2"])
# major_player_after_1967 = df[(df['MP']>100) & (df['Year']>1967)]

# TODO: find the players with the same name in a season
# cand = df.groupby(['Player', 'Year']).filter(lambda x: x['Tm'].count() > 1)  # players with multiple records in a year

# keep only 2016-2017 season
subdf = df[df['Year'] == 2017].copy()
# only keep TOT for players who are traded in the season
subdf = drop_multi_teams(subdf)
# keep only players playing more than 100 minutes
subdf = subdf[subdf['MP'] > 100]
# deal with NA in different cols - after 1985, for players playing more than
# 100 minutes, only 3P% and FT% have NA due to 0 attempt
subdf = subdf.fillna(0)
# feature extraction
X = subdf.drop(columns=['Year', 'Player', 'Tm', 'Pos', 'Age'])
pca = PCA(0.99)
X_new = pca.fit_transform(X)
# print(X_new.shape)
# calculate pair-wise similarity matrix
sim_mat = cosine_similarity(X_new)
# TODO: construct graph and run LPM(networkx-METIS or networkit)
# currently using networkx Louvain community detection because metis package issue
file = open("../data/nework.graph", 'w')
for i in range(X.shape[0]):
    for j in range(i + 1, X.shape[0]):
        if sim_mat[i][j] > 0:
            file.write("{},{},{}\n".format(i + 1, j + 1, sim_mat[i][j] + 1))
file.close()
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







