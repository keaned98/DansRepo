### Felix Gräßer, Surya Kallumadi, Hagen Malberg, and Sebastian Zaunseder. 2018. 
### Aspect-Based Sentiment Analysis of Drug Reviews Applying Cross-Domain and Cross-Data Learning. 
### In Proceedings of the 2018 International Conference on Digital Health (DH '18). ACM, New York, NY, USA, 121-125.

library(tm, snowballc)

drugs <- read.delim(file = '/Users/danielkeane/Downloads/Data Analytics/drugsComTrain_raw.csv', sep = '\t', header = T, stringsAsFactors = T)

# Convert counts to display "Yes" for value greater than or equal to 7.
convertCounts <- function(x) {
  x <- ifelse(x >= 7, "1", "0")
}

# convert rating to a binary variable: 1 = 7 or greater.
drugs$rating <- lapply(drugs$rating, convertCounts)

drugs$rating <- factor(drugs$rating)

# create corpus to clean the "review" column
drugs_corpus <- VCorpus(VectorSource(drugs$review))
# cleaning
drugs_corpus_clean <- tm_map(drugs_corpus, content_transformer(tolower))
drugs_corpus_clean <- tm_map(drugs_corpus_clean, removeNumbers)
drugs_corpus_clean <- tm_map(drugs_corpus_clean, removePunctuation)
drugs_corpus_clean <- tm_map(drugs_corpus_clean, removeWords, stopwords())
drugs_corpus_clean <- tm_map(drugs_corpus_clean, stemDocument)
drugs_corpus_clean <- tm_map(drugs_corpus_clean, stripWhitespace)
drugs_corpus_clean <- tm_map(drugs_corpus_clean, removeNumbers)
# create dtm
drugs_dtm <- DocumentTermMatrix(drugs_corpus_clean)

drugs_dtm_train <- drugs_dtm[1:113000,]
drugs_dtm_test <- drugs_dtm[113001:161297,]

# Labels not stored in dtm, so pull from original.
drugs_train_labels <- drugs[1:113000,]$rating
drugs_test_labels <- drugs[113001:161297,]$rating

# To ensure evenly split amongst the train and test sets.
prop.table(table(drugs_train_labels))
prop.table(table(drugs_test_labels))
       
drugs_freq_terms <- findFreqTerms(drugs_dtm_train, 5)
str(drugs_freq_terms)

drugs_dtm_freq_train <- drugs_dtm_train[, drugs_freq_terms]
drugs_dtm_freq_test <- drugs_dtm_test[, drugs_freq_terms]

convert_Counts <- function(x) {
  x <- ifelse(x > 0, "Yes", "No")
}


drugs_train <- apply(drugs_dtm_freq_train, MARGIN = 2,
                   convert_Counts)

drugs_test <- apply(drugs_dtm_freq_test, MARGIN = 2,
                  convert_Counts)

library(e1071)
drugs_train <- as.data.frame(as.matrix(drugs_train))
drugs_classifier <- naiveBayes(drugs_train, drugs_train_labels)
drugs_test_pred <- predict(drugs_classifier, drugs_test)





