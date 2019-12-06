library(igraph)    # for network data structures and tools
library(ggraph)    # for network visualization
library(ggthemes)
# install.packages('ggraph')
setwd("~/CMU/1920_fall/05839/ids-project/plotting")

year=2017
nodes <- read.csv("../data/processed/seasons_stats_2017_0.88_with_group.csv")
adj_mat = read.table("../data/similarity_matrix/matrix_2017_0.88.txt", sep="", header=FALSE)
adj_mat = data.matrix(adj_mat)
g = graph_from_adjacency_matrix(adj_mat, mode = "undirected", weighted = NULL,
                            diag = FALSE)
V(g)$name = nodes$Player
V(g)$group = nodes$Merged_Group
# igraph_layouts <- c('star', 'circle', 'gem', 'dh', 'graphopt', 'grid', 'mds', 
#                     'randomly', 'fr', 'kk', 'drl', 'lgl')
igraph_layouts <- c('mds',
                    'fr', 'drl', 'lgl','dh')
# igraph_layout = 'graphopt'
# cool: graphopt, dh
# ok: kk
for (igraph_layout in igraph_layouts){
  p <- ggraph(g, layout=igraph_layout)+
    geom_edge_link(colour = "grey")+
    geom_node_point(aes(color = as.factor(group)), size = 2)+
    theme_graph()+
    theme(legend.position = "bottom")+
    ggtitle(paste0('Layout: ', igraph_layout))+
    ggthemes::scale_colour_ptol() 
  ggsave(sprintf("%s_%s.png", igraph_layout, year), plot=p)
}

