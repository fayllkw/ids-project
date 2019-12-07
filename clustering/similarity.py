import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
stats = pd.read_csv("../data/seasons_stats.csv", index_col=0)
player = pd.read_csv("../data/player_data.csv")
# Drop blank rows and columns
stats = stats.dropna(axis=0, how="all")
stats = stats.drop(columns=["blanl", "blank2"])
# major_player_after_1967 = df[(df['MP']>100) & (df['Year']>1967)]

""" Calculating similarity for a single year """
def get_similarity(df, year, threshold, drop):
    # keep only 2016-2017 season
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
    if drop:
        X = X.drop(columns=['PER',
                            'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%',
                            'USG%', 'OWS', 'DWS', 'WS', 'WS/48',
                            'OBPM', 'DBPM', 'BPM', 'VORP'
                            ])
    pca_pipeline = Pipeline([('scaling', StandardScaler()), ('pca', PCA(0.9))])
    X_new = pca_pipeline.fit_transform(X)
    sim_mat = cosine_similarity(X_new)
    # redefine edge weight
    sim_mat = (sim_mat > threshold).astype(float)
    # np.fill_diagonal(sim_mat, np.nan)  # set diagonal as nan
    np.savetxt("../data/similarity_matrix/matrix_{}_{:.2f}_drop{}.txt".format(year, threshold, drop), sim_mat)
    # create and output edge list
    sim_df = pd.DataFrame(sim_mat)
    edge_list = sim_df.stack().reset_index()
    edge_list.columns = ['src', 'dst', 'edge_weight']
    edge_list = edge_list[edge_list['edge_weight'] != 0]
    edge_list.to_csv("../data/similarity_graph/network_{}_{:.2f}_drop{}.graph".format(year, threshold, drop),
                     index=False, header=None)

for year in range(1987, 2018):
    get_similarity(stats, year, threshold=0.9, drop=True)

