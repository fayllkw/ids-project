library(igraph)    # for network data structures and tools
library(ggraph)    # for network visualization
library(ggthemes)
# install.packages('ggraph')
setwd("~/CMU/1920_fall/05839/ids-project/plotting")

year=2017
threshold=0.88
drop='True'
nodes <- read.csv(sprintf("../data/processed/seasons_stats_%d_%.2f_drop%s_with_group.csv", 
                          year, threshold, drop))
adj_mat = read.table(sprintf("../data/similarity_matrix/matrix_%d_%.2f_drop%s.txt", 
                             year, threshold, drop), sep="", header=FALSE)
adj_mat = data.matrix(adj_mat)
g = graph_from_adjacency_matrix(adj_mat, mode = "undirected", weighted = NULL,
                            diag = FALSE)
V(g)$name = nodes$Player
V(g)$group = nodes$Merged_Group
# igraph_layouts <- c('star', 'circle', 'gem', 'dh', 'graphopt', 'grid', 'mds', 
#                     'randomly', 'fr', 'kk', 'drl', 'lgl')
# cool: fr, graphopt, dh (but slow)
# ok: kk
igraph_layout = 'fr'
p <- ggraph(g, layout=igraph_layout)+
    geom_edge_link(colour = "grey")+
    geom_node_point(aes(color = as.factor(group)), size = 2)+
    theme_graph()+
    theme(legend.position = "bottom")+
    ggtitle(paste0('Layout: ', igraph_layout))+
    ggthemes::scale_colour_ptol() 
ggsave(sprintf("%s_%s.png", igraph_layout, year), plot=p)


