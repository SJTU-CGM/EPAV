if(!require("ggplot2", quietly = TRUE)) {
		install.packages("ggplot2", dependencies = TRUE)
}

if(!require("ggrepel", quietly = TRUE)) {
		install.packages("ggrepel", dependencies = TRUE)
}

if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("ComplexHeatmap")