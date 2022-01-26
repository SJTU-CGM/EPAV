# Rscript ~/EPAV_fsy/final_code/plot_pca.R /lustre/home/acct-clswcc/clswcc-fsy/EPAV/test/0.95_distributed.pav ~/EPAV_fsy/phen.txt K9_group_Admixture TRUE FALSE ./plot_pca.pdf 5 7

args <- commandArgs()
opt <- list(
  pav = args[6],
  phenotype = args[7],
  select = args[8],
  center = as.logical(args[9]),
  scale = as.logical(args[10]),
  output = args[11],
  height = as.numeric(args[12]),
  width = as.numeric(args[13])
)

require(ggplot2)

pav_table <- read.table(opt$pav, header = T, check.names = F, sep = "\t")
rownames(pav_table) <- pav_table[, 1]
pav_table <- pav_table[, -1]

phen_data <- read.table(opt$phenotype, header = TRUE, stringsAsFactors = F, sep = "\t")
rownames(phen_data) <- phen_data[, 1]
phen_data <- phen_data[, -1]

phen <- opt$select

pca_res <- prcomp(t(pav_table), center = opt$center, scale = opt$scale)
pca.var.per <- round(pca_res$sdev^2/sum(pca_res$sdev^2)*100, 2)

p_data <- data.frame(sample = rownames(pca_res$x),
                     PC1 = pca_res$x[,1],
                     PC2 = pca_res$x[,2],
                     phen = phen_data[colnames(pav_table), phen])

pdf(opt$output, height = opt$height, width = opt$width)
ggplot(p_data, aes(x = PC1, y = PC2, color = phen)) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  geom_point() + 
  labs(x = paste("PC1(",pca.var.per[1],"%",")",sep=""),
       y = paste("PC2(",pca.var.per[2],"%",")",sep=""),
       color = phen) +
  theme_bw() 
dev.off()
