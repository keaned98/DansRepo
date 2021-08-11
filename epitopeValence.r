### Objective: ###
# Using Naive Bayes algorithm to predict if antibody will be target positive (1).
library(e1071)
bcell <- read.csv('/Users/danielkeane/Downloads/Data Analytics/input_bcell.csv')
summary(bcell)

## Change column names.
colnames(bcell)[colnames(bcell) %in% c('chou_fasman', 'emini', 'kolaskar_tongaonkar', 'parker')] <- c('B_Turn', 'Relative_Surface_Access', 'Antigenicity', 'Pep_Hydrophobicity')

# Change binary to factor of 'Yes' and 'No'.
# bcell$target <- factor(ifelse(bcell$target, 'Yes', 'No'))

str(bcell$target)
table(bcell$target)
# 0 = 10485, 1 = 3902

# Create varaible peptide length to measure length of peptide chain.
bcell$peptide_length <- nchar(bcell$peptide_seq)


############################################################

# Create some simple plots to gain a better understanding of relationships.
library(ggplot)
install.packages('GGally')
library(GGally)

bcell$target <- factor(bcell$target)

# OK so most of the peptide lengths are greater than 10 (13,000+/14,387)
# Does length impact target value?
summary(bcell$peptide_length)
bins <- c(4, 8, 11, 15)
names <- c('Low_length', 'Medium_length', 'High_length')

bcell$pep_length_bins <- cut(bcell$peptide_length, breaks = bins, labels = names)
sum(is.na(bcell$pep_length_bins))

## Now we have sorted the length into bins, lets plot correlation between 
## length and RSA.
plotdata <- bcell %>%
  group_by(pep_length_bins) %>%
  summarise(mean_RSA = mean(bcell$`Relative Surface Access`))

# Peptide length versus RSA.
ggplot(bcell,
       aes(x=pep_length_bins,
           y = bcell$`Relative Surface Access`)) +
  geom_bar(stat = 'identity')
# Good depiction of correlation between length of peptide chain and RSA.
# So: Longer chain = better RSA/Greater chance of epitope attachment?

######################################
# Sunday. March 21. 2021.
bcell$target <- factor(ifelse(bcell$target, 'Yes', 'No'))

ggplot(bcell,
       aes(x=bcell$target,
           y=bcell$peptide_length)) +
  geom_boxplot()
### Good? depiction of Target versus Peptide length
### Shows median length is 12 for 'Yes' and median length of 10 for 'No'.



##################
# Naive Bayes
# First: Create test and train sets.
bcell_train <- bcell[1:10070,]
bcell_test <- bcell[10071:14387,]

# Store target variable to compare our model to later.
bcell_train_labs <- bcell[1:10070,]$target
bcell_test_labs <- bcell[10071:14387,]$target

# To see how proportion of target values was split amongst train and test sets.
prop.table(table(bcell_train_labs))
prop.table(table(bcell_test_labs))

bcell_classifier <- naiveBayes(bcell_train, as.factor(bcell_train_labs))
bcell_prediction <- predict(bcell_classifier, bcell_test)

library(gmodels)
CrossTable(bcell_prediction, bcell_test_labs,
           prop.chisq = F, prop.c = F, prop.r = F,
           dnn = c('predicted', 'actual'))

#########################


##### April 16, 2021
##### Running decision tree algorithm on data.
install.packages('C5.0')
library(C50)

table(bcell$target)
# 10,485 did not attach to epitope, 3,902 did attach.

RNGversion("3.5.2"); set.seed(123)
train_bcell <- sample(14387, 12948)
str(train_bcell)

# Create test and train sets. 90% train, 10% test.
bcell_trainDT <- bcell[train_bcell,]
bcell_testDT <- bcell[-train_bcell,]

# Check for even split.
prop.table(table(bcell_trainDT$target))
prop.table(table(bcell_testDT$target))

drops <- c("parent_protein_id","protein_seq")
bcell_trainDT <- bcell_trainDT[, -c(1:2)]
bcell_trainDT$peptide_seq <- NULL


bcellDT_model <- C5.0.default(x = bcell_trainDT[-11], y = as.factor(bcell_trainDT$target))
bcellDT_model

## Now on test data.
bcell_testDT$protein_seq <- NULL

testDT_pred <- predict(bcellDT_model, bcell_testDT)

library(gmodels)
CrossTable(bcell_testDT$target, testDT_pred,
           prop.chisq = F, prop.c = F, prop.r = F,
           dnn = c('Actual', 'Predicted'))
# 84% overall accuracy!!! - 71% of trials accurately predicted epitope attachment to paratope.

# Can boosting increase accuracy? Boosting combines weak performing learners, to create one stronger one.
# Done by using "trials =" agr. to set upper limit on how many trees to create.
bcellmodel_boost10 <- C5.0.default(x = bcell_trainDT[-11], y = as.factor(bcell_trainDT$target), trials = 10)
bcellmodel_boost10

bcellmodel_boost10_pred <- predict(bcellmodel_boost10, bcell_testDT)
CrossTable(bcell_testDT$target, bcellmodel_boost10_pred,
           prop.chisq = F, prop.c = F, prop.r = F,
           dnn = c('Actual', 'Predicted'))
# Increased overall accuracy to 86%. Increased epitope/paratope attachment accuracy to 75%!!!!!
plot(bcellmodel_boost10, subtree = 3)


### Run again using rpart() so we can visualize our tree.
bcellmodel_rpart <- rpart(bcell_trainDT$target ~ ., data = bcell_trainDT, method = 'class')
bcellmodel_rpart

install.packages("rattle")
library(rattle)
library(rpart.plot)
library(RColorBrewer)

rpart.plot(bcellmodel_rpart, type = 3, nn = T, branch = .4,
           main = 'Epitope Decision Tree', extra = 101
           )
rpart.rules(bcellmodel_rpart, extra = 9)

bcellmodel_rpart$splits
bcellmodel_rpart$splits[bcellmodel_rpart$splits[,'ncat']==1,]


#####
install.packages('ISLR')
library(ISLR)
install.packages('tree')
library(tree)

tree.bcell <- tree(bcell_trainDT$target ~ ., data = bcell_trainDT)






###################
options(java.parameters = "-Xmx8000m")
library(RWeka)
bcell_jripData <- lapply(bcell, FUN = as.factor)
bcell_jripData <- as.data.frame(bcell_jripData)

bcellClassifier_JRip <- JRip(target ~ ., data = bcell_jripData)
bcell_JRipPred <- predict(bcellClassifier_JRip, bcell_jr2)
table(actual = bcell$target, predicted = bcell_JRipPred)

options(java.parameters = "-Xmx1024m")






