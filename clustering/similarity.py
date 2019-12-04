import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
print(X_new.shape)
# calculate pair-wise similarity - express as matrix?
sim_mat = cosine_similarity(X_new)
# TODO: construct graph and run METIS?


