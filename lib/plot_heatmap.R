# Rscript ~/EPAV_fsy/final_code/plot_heatmap.R /lustre/home/acct-clswcc/clswcc-fsy/EPAV/test/0.95_distributed.pav /lustre/home/acct-clswcc/clswcc-fsy/EPAV/test/rice_phe.txt height/grain_weight/grain_length ./plot_heatmap.pdf 5 7

args <- commandArgs()
opt <- list(
  pav = args[6],
  phenotype = args[7],
  select = args[8],
  output = args[9],
  height = as.numeric(args[10]),
  width = as.numeric(args[11])
)

require(ComplexHeatmap)

pav_table <- read.table(opt$pav, header = TRUE, check.names = F, sep = "\t")
phen_data <- read.table(opt$phenotype, header = TRUE, stringsAsFactors = F, sep = "\t")
phens <- unlist(strsplit(opt$select, "/"))
phen_data <- phen_data[, c(colnames(phen_data)[1], phens)]

rownames(pav_table) <- pav_table[, 1]
pav_table <- pav_table[, -1]
pav_table <- pav_table[names(sort(rowSums(pav_table), decreasing = T)),
                       names(sort(colSums(pav_table), decreasing = F))]

phen_data <- phen_data[match(colnames(pav_table), phen_data[,1]),]
rownames(phen_data) <- phen_data[, 1]
phen_data <- phen_data[, -1, drop=F]

ht <- Heatmap(t(as.matrix(pav_table)),
              col = structure(c("#4277A1", "#B95758"), names = c("0", "1")),
              na_col = "white",
              show_heatmap_legend = FALSE,
              cluster_rows = FALSE,
              cluster_columns = FALSE,
              show_row_names = FALSE,
              show_column_names = FALSE,
              column_title = paste0("Elements (n=", nrow(pav_table), ")"),
              column_title_side = "bottom",
              row_title = paste0("Samples (n=", ncol(pav_table), ")"),
              row_title_side = "right",
              left_annotation = rowAnnotation(df = phen_data,
                                              show_annotation_name = F)
)

pdf(opt$output, height = opt$height, width = opt$width)
draw(ht,
     annotation_legend_list = Legend(
       title = " ",
       at = c(0, 1),
       labels = c("Absence", "Presence"),
       legend_gp = gpar(fill = c("#4277A1", "#B95758")),
       by_row = TRUE, ncol = 2,
       title_position = "leftcenter"
     ),
     merge_legends = FALSE,
     heatmap_legend_side = "left",
     annotation_legend_side = "top")
dev.off()

