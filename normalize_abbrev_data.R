data = read.csv(file.choose())
column_names = c('Name', 'age','GP', 'Mins', '3_pt_attempt', '3_pt_pct', '2_pt_attempt', '2_pt_pct','ft_attempt', 'ft_pct', 'off_reb','def_reb', 'assist', 'steal','blocks', 'TO', 'Fouls', 'Weight', 'net_rating', 'height')
scale_vals = c(0, 3, 1, 3, 2, 3, 3, 4, 2, 2, 3, 3, 5, 3, 3, 3, 2, 2, 6, 2)
colnames(data) = column_names
for(i in 2:length(column_names)){
  col_name = column_names[i]
  data[,col_name] = (data[,col_name] - mean(data[,col_name]))/sd(data[,col_name])
  scale_factor = scale_vals[i]
  data[,col_name] = data[,col_name] * scale_factor
}
output = write.csv(data, './normalized_full_data.csv', row.names = FALSE)
