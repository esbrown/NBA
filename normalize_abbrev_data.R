data = read.csv(file.choose())
column_names = c('Name', 'GP', 'FG', 'Reb', 'Ast', 'Points', 'Weight', 'Height')
scale_vals = c(0, 1, 5, 5, 5, 5, 2, 2)
colnames(data) = column_names
for(i in 2:length(column_names)){
  col_name = column_names[i]
  data[,col_name] = (data[,col_name] - mean(data[,col_name]))/sd(data[,col_name])
  scale_factor = scale_vals[i]
  data[,col_name] = data[,col_name] * scale_factor
}
output = write.csv(data, './normalized_abbrev_data.csv', row.names = FALSE)
