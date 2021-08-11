### Predicting heart failure
library(dplyr)
heart <- read.csv('/Users/danielkeane/Downloads/Data Analytics/heart_failure_clinical_records_dataset.csv', stringsAsFactors = T)
heart$DEATH_EVENT <- as.factor(heart$DEATH_EVENT)


# Creating train and test sets using sample_n() because total number of observations is low and
# distribution of death events is rights skewed.
heart_train <- sample_n(heart, 200)
heart_test <- sample_n(heart, 200)

heart_train_labs <- heart_train[1:200,]$DEATH_EVENT
heart_test_labs <- heart_test[1:200,]$DEATH_EVENT

# Using prop.table to see if deaths are evenly distributed.
prop.table(table(heart_train_labs))
prop.table(table(heart_test_labs))

library(e1071)
heart_classifier <- naiveBayes(heart_train, heart_train_labs)

heart_pred <- predict(heart_classifier, heart_test)

library(gmodels)
CrossTable(heart_pred, heart_test_labs, prop.chisq = F, prop.r = F, prop.c = F, 
           dnn = c('Predicted', 'Actual'))








###########
# Visuals
# Correlation Matrix
heart_cor <- cor(heart, method = 'pearson')
# heart must be numeric to run cor()
heart_numeric <- read.csv('/Users/danielkeane/Downloads/Data Analytics/heart_failure_clinical_records_dataset.csv')

heart_cor <- cor(heart_numeric, method = 'pearson')
corrplot(heart_cor, type = 'upper',
         order = 'hclust',
         tl.col = 'black')

install.packages('PerformanceAnalytics')
library('PerformanceAnalytics')
chart.Correlation(heart_cor, histogram = T, pch = 19)


colnames(heart_cor) <- c('Age', 'Anaemia', 'Creatinine Phos.', 'Diabetes', ' Ejection Frac.', 'High BP', 'Platelets',
                         'Serum Creatinine', 'Serum Sodium', 'Sex', 'Smoking', 'Time', 'Death Event')
corrplot(heart_cor)

















