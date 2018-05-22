setwd("~/Desktop")
data = read.csv(file.choose())
stats = read.csv(file.choose())

combined = merge(data,stats,by="Player")

output = write.csv(combined, './combined_nba_player_data', row.names = FALSE)
