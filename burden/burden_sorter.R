burden <- read.csv("./1dpi_burden.csv", header = T)

burden$intden <- log10(burden$Area * burden$Mean)
burden <- burden[order(burden$intden),]

burden$triciles <- ntile(burden$intden, 4)

keepers <- subset(burden, triciles == 2 | triciles == 3)
keepers <- as.data.frame(keepers$Label)

write.csv(x = keepers, file = "keepers.csv")