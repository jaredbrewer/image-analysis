burden <- read.csv("/Volumes/JB_SD1/JB325/1dpi/burden.csv", header = T)

burden$intden <- log10(burden$Area * burden$Mean)
burden <- burden[order(burden$intden),]

burden$triciles <- ntile(burden$intden, 5)

keepers <- subset(burden, triciles == 2 | triciles == 3 | triciles == 4)
keepers <- as.data.frame(keepers$Label)
keepers$X <- 1
plot(keepers$X, keepers$intden)


write.csv(x = keepers, file = "keepers.csv")