# Load package
library(networkD3)

links <- read.csv("/Users/ASD/Desktop/05839/HW/Project/ids-project/data/R_links.csv")
nodes <- read.csv("/Users/ASD/Desktop/05839/HW/Project/ids-project/data/R_nodes.csv")

forceNetwork(Links = links, Nodes=nodes, Source="source", Target="target", Value="value",
             NodeID="name", Group="group")
