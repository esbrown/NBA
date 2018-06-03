data = read.csv(file.choose())
data[is.na(data)] = 0

for (i in 2:length(data[,])){
  data[,i] = (data[,i] - mean(data[,i]))/sd(data[,i])
}
colnames(data) = c(' ')
write.csv(data, './normalized_neural_data_2014.csv', row.names = FALSE)

