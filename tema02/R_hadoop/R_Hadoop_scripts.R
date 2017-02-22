##
## RHadoop
##

## pag. 77 Big Data Analytics with R and Hadoop

##Loading rmr2 y rhdfs
library(rmr2)
library(rhdfs)
hdfs.init()

?to.dfs

###### Let's see one test (only a map)
ints = to.dfs(1:100)
calc = mapreduce(input = ints, map = function(k, v) cbind(v, 2*v))
test <- from.dfs(calc)
test




###### First simple script
#how many times each outcome occurred in binomial random sample?
groups = rbinom(32, n = 50, prob = 0.4)
tapply(groups, groups, length)
groups = to.dfs(groups)

from.dfs(
  mapreduce(input = groups, 
            map = function(., v) keyval(v, 1), 
            reduce = function(k, vv) keyval(k, length(vv))
  )
)


###### Let's do a wordcount
#http://blog.hsinfu.org/2015/04/01/ubuntu14-04linuxmint16-rhadoop-rmr2-plyrmr-rhdfs-rhbase-installation-on-hadoop-2-6-0/


hdfs.ls('/user/hduser')

## map function
map <- function(k,lines) {
  words.list <- strsplit(lines, '\\s') 
  words <- unlist(words.list)
  return( keyval(words, 1) )
}

## reduce function
reduce <- function(word, counts) { 
  keyval(word, sum(counts))
}

wordcount <- function (input, output=NULL) { 
  mapreduce(input=input, 
            output=output, 
            input.format="text", 
            map=map, 
            reduce=reduce)
}


## delete previous result if any
system("/usr/local/hadoop/bin/hadoop fs -mkdir inputs/input2")
system("/usr/local/hadoop/bin/hadoop fs -put texto.txt inputs/input2")
system("/usr/local/hadoop/bin/hadoop fs -rm -r output")

## Submit job
hdfs.root <- '/user/bigdata'
hdfs.data <- file.path(hdfs.root, 'inputs/input2') 
hdfs.out <- file.path(hdfs.root, 'output') 

out <- wordcount(hdfs.data, hdfs.out)

## Fetch results from HDFS
results <- from.dfs(out)



## check top 30 frequent words
results.df <- as.data.frame(results, stringsAsFactors=F) 
colnames(results.df) <- c('word', 'count') 
head(results.df[order(results.df$count, decreasing=T), ], 30)





###### Let's do a Logistic regression
lr.map =          
  function(., M) {
    Y = M[,1] 
    X = M[,-1]
    m = nrow(X)
    #keyval(1, Y * X *  g(-Y * as.numeric(X %*% t(plane))) )
    keyval(1,  (1/m) *( X * (Y-g( as.numeric(X %*% t(plane)) )) )  )
  }


lr.reduce =
  function(k, Z) 
    keyval(k, t(as.matrix(apply(Z,2,sum))) )

iterations<-3
dims<-3
alpha<-0.05

out = list()
test.size = 1000
eps = rnorm(test.size)
testdata.df<-data.frame(
  #y = 1 * (eps > 0) ,
  y = 2 * (eps > 0) - 1,
  x1 = 1:test.size, 
  x2 = 1:test.size + eps
)

testdata = to.dfs( as.matrix(testdata.df )  )


plane = t(rep(0, dims))
g = function(z) 1/(1 + exp(-z))
for (i in 1:iterations) {
  gradient = 
    values(
      from.dfs(
        mapreduce(
          input=testdata,
          map = lr.map,     
          reduce = lr.reduce,
          combine = TRUE)))
  plane = plane + alpha * gradient 
}
plane

#single command to obtain the model
glm(formula = y ~ x1 + x2, family = binomial("logit"), data = testdata.df)



###### Let's do a Linear regression
X = matrix(rnorm(2000), ncol = 10)
y = as.matrix(rnorm(200))

coef(lm(y~0+X))
solve(t(X)%*%X, t(X)%*%y)



X.index = to.dfs(cbind(1:nrow(X), X))
lr.map =          
  function(., X) {
    X = X[,-1]
    keyval(1, list(t(X) %*% X) )
  }

lr.reduce =
  function(k, Z) 
    keyval(1, list(Reduce('+', Z)))

XtX = values(
       from.dfs(
         mapreduce(
           input = X.index,
           map = lr.map,
           reduce = lr.reduce,
           combine = TRUE)
               )
           )[[1]]

lr.map =          
  function(., X) {
    y = y[X[,1],]
    X = X[,-1]
    keyval(1, list(t(X) %*% y) )
  }


Xty = values(
        from.dfs(
         mapreduce(
           input = X.index,
           map = lr.map,
           reduce = lr.reduce,
           combine = TRUE)
                  )
           )[[1]]

solve(XtX, Xty)