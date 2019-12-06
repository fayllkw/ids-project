# Load package
# install.package('networkD3')
library(networkD3)
print(getwd())
setwd("~/CMU/1920_fall/05839/ids-project/plotting")

links <- read.csv("../data/similarity_graph/network_2017_0.88.graph", header=FALSE)
colnames(links) <- c('Source', 'Target', 'Value')
nodes <- read.csv("../data/processed/seasons_stats_2017_0.88_with_group.csv")

nw <- forceNetwork(Links = links, Nodes=nodes, Source="Source", Target="Target", Value="Value",
             NodeID="Player", Group="Group", zoom=TRUE)
saveNetwork(network=nw, file = 'test.html')
