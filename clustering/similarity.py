import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
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

""" Calculating similarity for a single year """
# keep only 2016-2017 season
year = 1997
subdf = df[df['Year'] == year].copy()
# only keep TOT for players who are traded in the season
subdf = drop_multi_teams(subdf)
# keep only players playing more than 100 minutes
subdf = subdf[subdf['MP'] > 100]
# deal with NA in different cols - after 1985, for players playing more than
# 100 minutes, only 3P% and FT% have NA due to 0 attempt
subdf = subdf.fillna(0)
# output processed stats of the year
subdf.to_csv("../data/processed/seasons_stats_{}.csv".format(year), index=False)
# feature extraction (PCA and cosine similarity)
X = subdf.drop(columns=['Year', 'Player', 'Tm', 'Pos', 'Age'])
pca_pipeline = Pipeline([('scaling', StandardScaler()), ('pca', PCA(0.9))])
X_new = pca_pipeline.fit_transform(X)
sim_mat = cosine_similarity(X_new)
# redefine edge weight
option = 'cutoff'  # or scale
threshold = None
if option == 'cutoff':
    threshold = 0.88
    sim_mat = (sim_mat > threshold).astype(float)
elif option == 'scale':
    sim_mat = sim_mat + 1
np.fill_diagonal(sim_mat, np.nan)  # set diagonal as nan
# create and output edge list
sim_df = pd.DataFrame(sim_mat)
edge_list = sim_df.stack().reset_index()
edge_list.columns = ['src', 'dst', 'edge_weight']
if option == 'cutoff':
    edge_list = edge_list[edge_list['edge_weight'] != 0]
edge_list.to_csv("../data/similarity_graph/network_{}_{}.graph".format(year, threshold),
                 index=False, header=None)

