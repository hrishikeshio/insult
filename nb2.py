from nltk.classify import NaiveBayesClassifier
import nltk
import csv 
import time
import re
a=time.time()
X_train,y_train=[],[]

#Read bad words
with open("badwords.txt","rb") as f:
    badwords=[]
    for i in f:
        badwords.append(i.lower().strip())


posfeats,negfeats=[],[]

# Read training data
with open('train.csv','rb') as f:
    reader = csv.reader(f)
    for row in reader:
        X_train.append(row[2])
        y_train.append(row[0])
print "data processed"
print time.time()-a

#Feature extracter
def word_feats(words):
    feats={}
    words=words.strip()
    for sentense in re.split(r' *[\.\?!]["\)\]]* *', words):
        hasbadw=0
        hasyou=0
        for word in nltk.wordpunct_tokenize(sentense):
            for curse in badwords:
                if word.lower().endswith(curse.lower()) or word.lower().startswith(curse.lower()):
                    hasbadw=1
                    break
                    
                if word.lower() in ("you","u","ur","your","urs","urz","yours"):
                    hasyou=1
        if hasbadw and hasyou:

            feats["you"]=True 
    if words.upper()==words:
        feats["allcaps"]=True
    else:
        feats['allcaps']=False
    return feats 


#Extract features
for i in range(len(X_train)):
    if int(y_train[i])==0:
        posfeats.append((word_feats(X_train[i]),"0"))

		#posfeats=dict(posfeats.items()+dict([(word.lower(),True) for word in nltk.wordpunct_tokenize(X_train[i])]).items())
    else:
        negfeats.append((word_feats(X_train[i]),"1"))
		#negfeats.append(dict([(word.lower(),True) for word in nltk.wordpunct_tokenize(X_train[i])]))
#print posfeats,len(posfeats)


negcutoff = len(negfeats)*4/5
poscutoff = len(posfeats)*4/5

trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

#print trainfeats
classifier = NaiveBayesClassifier.train(trainfeats)
print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
classifier.show_most_informative_features()
ans=[]

#Classify
with open("train.csv","rb") as f:
	reader=csv.reader(f)
	for row in reader:
		ans.append([int(classifier.classify(word_feats(row[2]))) and int("you" in word_feats(row[2])),row[1],row[2]])

#Write answer
with open("nb2.csv","wb") as f:
	writer=csv.writer(f)
	for i in ans:
		writer.writerow(i)

#Cross validation
with open("nb2.csv",'rb') as f:
    with open("train.csv",'rb') as g:
        with open("nb2_results.txt",'wb') as a:
            fread=csv.reader(f)
            gread=csv.reader(g)
            awrite=csv.writer(a)
            for i in range(3946):
                fr=fread.next()
                gr=gread.next()
                if not fr[0]==gr[0]:
                    awrite.writerow((fr[0],gr[0],word_feats(fr[2]),fr[2]))
