# Rscript ~/EPAV_fsy/final_code/plot_manhattan.R /lustre/home/acct-clswcc/clswcc-fsy/EPAV/test/height.ps 1e-5 1e-5 ./plot_manhattan.pdf 5 10

args <- commandArgs()
opt <- list(
  file = args[6],
  suggestiveline = as.numeric(args[7]),
  annotatePval = as.numeric(args[8]),
  output = args[9],
  height = as.numeric(args[10]),
  width = as.numeric(args[11])
)

require(ggplot2)
require(ggrepel)

pdata <- read.table(opt$file, header = T, check.names = F, sep = "\t")


chrs <- unique(pdata$chr)
lengths <- unlist(lapply(chrs, function(x){nrow(subset(pdata, chr == x))}))
ticks <- cumsum(lengths) - lengths/2

pdata$chr <- factor(pdata$chr, levels = chrs)
pdata <- pdata[order(pdata$chr, pdata$pos),]
pdata$x <- 1:nrow(pdata)

chr_col <- rep(c("black", "gray60"), ceiling(length(chrs)/2))[1:length(chrs)]

pdf(opt$output, height = opt$height, width = opt$width)
ggplot(pdata, aes(x = x, y = -log10(pval), color = chr)) +
  geom_point(size = .3) +
  geom_hline(yintercept = 5, color = "red", linetype = 2) +
  geom_point(data = subset(pdata, pval < opt$suggestiveline), color = "red") +
  geom_text_repel(data = subset(pdata, pval < opt$annotatePval), aes(label = id)) +
  scale_color_manual(values = chr_col) +
  labs(x = "Chromosome", y = "-log10(p)") +
  theme_classic() +
  scale_x_continuous(expand = expansion(mult = 0), 
                     breaks = ticks, labels = chrs) +
  scale_y_continuous(expand = expansion(mult = c(0,.05))) +
  theme(legend.position = "none",
        strip.background = element_blank(),
        axis.ticks.x = element_blank(),
        axis.line.x = element_blank(),
        axis.text.x = element_text(angle = 90, hjust = 1, vjust = .5,
                                   color = "black")
  )
dev.off()

