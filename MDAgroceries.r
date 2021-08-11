rm(list = ls())

install.packages('arules')
library(arules)

groceries <- read.transactions('/Users/danielkeane/Downloads/Data Analytics/groceries.csv', sep = ',')
typeof(groceries)
summary(groceries)

inspect(groceries[1:5])

itemFrequency(groceries[,1:15])

itemFrequencyPlot(groceries, topN = 20)

image(sample(groceries, 100))

### apriori(data, parameter = list( support = , confidence = ))

groceryrules <- apriori(groceries, parameter = list(support = .006, 
                                                    confidence = .25, 
                                                    minlen = 2))
summary(groceryrules)

d=data.frame(itemFrequency(groceries[,1:169]))
d=d%>%tibble::rownames_to_column()


inspect(groceryrules[1:5])

groceryrules_df=as(groceryrules, 'data.frame')
library(dplyr)
df=groceryrules_df%>%filter(lift>1)%>%arrange(lift)

d%>%filter(rowname == 'root vegetables')






