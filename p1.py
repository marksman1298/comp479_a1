import nltk, os, re
from nltk import word_tokenize
from nltk.corpus import reuters

def splitIntoArticles(dir):
    data = ""
    for filename in os.listdir(dir):
        if filename.endswith(".sgm"):
            filepath = dir + "/" + filename
            with open(filepath, "r") as f:
                data += f.read()
    return data.split("</REUTERS>")
    #last article is empty :)

def makeDict(listOfArticles): #want to get all newids of articles, then add them to a list, then combine both lists into dictionary with key new id : value article
    articles = {}
    ids = []
    for i in range(len(listOfArticles)): 
        foundNewID = re.search('NEWID="([0-9]+)"', listOfArticles[i])
        if foundNewID is not None:
            newId = re.search('[0-9]+', foundNewID.group(0))
            if newId is not None:
                ids.append(newId.group(0))
    articles = {ids[i]: listOfArticles[i] for i in range(len(ids))}            
    return articles
            

def cleanArticles(articles):
    for value in articles.values():
        value = re.sub("<(.*?)>","" , value)
        value = re.sub("&#(.*?);", "", value)
        value = re.sub("\n\s*\n", "\n", value)
    return articles
        

def tokenize(articles):
    ad

#dir = input("Enter the directory: ")
dir = r'C:\Users\marks\OneDrive\Desktop\Fall-2021\COMP 479\reuters-21578'

articles = [] # make dictionary instead? 


articles = splitIntoArticles(dir)
# print(len(articles))
articles = makeDict(articles)

# print("Start first\n " + articles[0] + "\n end first")
# print("Start last\n " + articles[21578] + "\n end last")

articles = cleanArticles(articles)
print("Start first\n " + articles["1"] + "\n end first")
