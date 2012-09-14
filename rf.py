from nltk.classify import NaiveBayesClassifier
import nltk
import csv 
import time
import re
from sklearn.ensemble import RandomForestClassifier
a=time.time()
X_train,y_train,X_test=[],[],[]

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
    hasbadw=0
    hasyou=0
    sentences=0
    for sentense in re.split(r' *[\.\?!]["\)\]]* *', words):
        sentences+=1
        for word in nltk.wordpunct_tokenize(sentense):
            for curse in badwords:
                if word.lower().endswith(curse.lower()) or word.lower().startswith(curse.lower()):
                    hasbadw+=1
                    break
                    
            if word.lower() in ("you","u","ur","your","urs","urz","yours"):
                hasyou+=1
        

    feats["you"]=hasyou
    feats["badw"]=hasbadw 
    feats["length"]= len(words)
    feats["caps"]=len(re.findall('[A-Z]', words))
    feats["smalls"]=len(re.findall('[a-z]', words))
    feats["sentences"]=sentences
    feats["capsratio"]=float(feats["caps"])/len(words)
    featslist=[]
    for k,v in feats.iteritems():
        featslist.append(v)
    return featslist


#Extract features
trainfeats=[]
for i in range(len(X_train)):

    trainfeats.append(word_feats(X_train[i]))

print "features extracted"
print time.time()-a

with open("feats.csv","wb") as f:
    writer=csv.writer(f)
    for i in trainfeats:
        writer.writerow(tuple(i))
#print trainfeats
classifier = RandomForestClassifier(n_estimators=10).fit(trainfeats, y_train)
ans=[]
print "training done"
print time.time() -a
#Classify
with open("test.csv","rb") as f:
    reader=csv.reader(f)
    for row in reader:
        X_test.append(word_feats(row[1]))

ass=classifier.predict(X_test)
print "Prediction done"
print time.time() - a
#print ass
with open("ans.csv",'wb') as fans: 
    writer=csv.writer(fans)
    for i in ass:
        writer.writerow(tuple(i))
