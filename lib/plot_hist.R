# Rscript ~/EPAV_fsy/final_code/plot_hist.R /lustre/home/acct-clswcc/clswcc-fsy/EPAV/test/0.95.pav 1 0.95 ./plot_hist.pdf 5 7

args <- commandArgs()
opt <- list(
  pav = args[6],
  core = as.numeric(args[7]),
  softcore = as.numeric(args[8]),
  output = args[9],
  height = as.numeric(args[10]),
  width = as.numeric(args[11])
)

if(!(opt$core > 0 & opt$core <= 1)){
  stop("")
}

if(!(opt$softcore > 0 & opt$softcore < opt$core)){
  stop("")
}

require(ggplot2)

pav_table <- read.table(opt$pav, header = T, check.names = F, sep = "\t")
rownames(pav_table) <- pav_table[,1]
pav_table <- pav_table[,-1]
samplen <- ncol(pav_table)

pdata <- as.data.frame(table(rowSums(pav_table)))
pdata$Var1 <- as.numeric(as.vector(pdata$Var1))
pdata$group <-
  ifelse(pdata$Var1 == 0, NA,
         ifelse(pdata$Var1 == 1, "Unique",
                ifelse(pdata$Var1 >= samplen*opt$core, "Core",
                       ifelse(pdata$Var1 >= samplen*opt$softcore, "Soft Core", "Cloud"))))


pdata$group <- factor(pdata$group, levels = c("Core", "Soft Core", "Cloud", "Unique"))

pdf(opt$output, height = opt$height, width = opt$width)
ggplot(pdata) +
  geom_bar(aes(x = Var1, y = Freq, fill = group),stat = "identity", width = 1) +
  labs(x = "Sample Number", y = "Count", fill = " ") +
  scale_x_continuous(expand = expansion(mult=0.01)) +
  scale_y_continuous(expand = expansion(mult=c(0,0)), trans = "log10" ) +
  scale_fill_brewer(palette = "Set1", na.value = "grey50") +
  theme_classic() +
  theme(legend.position = "top")
dev.off()

