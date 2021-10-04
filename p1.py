import nltk, os, re
from nltk import word_tokenize
from nltk.corpus import reuters
from nltk.stem import porter
from nltk.stem.porter import PorterStemmer

def splitIntoArticles(dir): #read all files in directory, put everything into one string, split into list of articles 
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
            

def cleanArticles(articles): #remove all tags and extra whitespace, maybe tokenize at same time?
    for key in articles:
        articles[key] = re.sub("<(.*?)>","" , articles[key])
        articles[key] = re.sub("&#(.*?);", "", articles[key])
        articles[key] = re.sub("\n\s*\n", "\n", articles[key])
        articles[key] = word_tokenize(articles[key])
    return articles
        

def tokenize(articles): #tokenize 
    for key in articles:
        articles[key] = word_tokenize(articles[key])
    return articles

def toLowerCase(articles): #lower case all values in the strings
    for keys in articles:
        articles[keys]=list(map(str.lower, articles[keys]))
    return articles

def porterStemmer(articles):
    ps = PorterStemmer()
    for keys in articles:
        articles[keys] = list(map(ps.stem, articles[keys]))
    return articles
#dir = input("Enter the directory: ")
dir = r'C:\Users\marks\OneDrive\Desktop\Fall-2021\COMP 479\reuters-21578'

def removeStopWords(articles):
    words = input("Enter stop words separated by spaces: ")
    listWords = words.split(" ")
    #list compressions?
    articles2 = [word for word in articles if word not in listWords]
    return articles2
    # for keys in articles:
    #     articles[keys] = list(map(list(filter((listWords).__ne__), articles[keys])), listWords)
    # return articles
articles = [] 


articles = splitIntoArticles(dir)
# print(len(articles))
articles = makeDict(articles)

# print("Start first\n " + articles[0] + "\n end first")
# print("Start last\n " + articles[21578] + "\n end last")

#articles = cleanArticles(articles)
#articles = tokenize(articles)
#articles = toLowerCase(articles)
#articles = porterStemmer(articles)
#print("Start first\n ", articles["2"] , "\n end first")

articles = removeStopWords(articles)
print(articles[2])
