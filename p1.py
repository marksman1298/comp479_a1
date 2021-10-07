import os, re, json
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer


def splitIntoArticles(dir, specificFile=""): #read all files in directory, put everything into one string, split into list of articles 
    data = ""
    listOfFiles = os.listdir(dir)
    if specificFile in listOfFiles and specificFile.endswith(".sgm"):
        filepath = dir + "/" + specificFile
        with open(filepath, "r") as f:
            data = f.read()
        return makeDict(data.split("</REUTERS>"))
    for filename in listOfFiles:
        if filename.endswith(".sgm"):
            filepath = dir + "/" + filename
            with open(filepath, "r") as f:
                data += f.read()
    return makeDict(data.split("</REUTERS>"))

    

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
    return extractText(articles)
            
def extractText(articles): #get all information between the text tags for each article
    for key in articles:
        startText = articles[key].find("<TEXT>")
        endText = articles[key].find("</TEXT>")
        if startText != -1 and endText != -1:
            articles[key] = articles[key][startText:endText+7]
    with open("part1_reut2-004.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles
     

def tokenize(articles): #tokenize and inverse
    for key in articles:
        articles[key] = re.sub("<(.*?)>","" , articles[key])
        articles[key] = re.sub("&#(.*?);", "", articles[key])
        articles[key] = word_tokenize(articles[key])
    with open("part2_reut2-004.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles

def toLowerCase(articles): #lower case all values in the strings
    for keys in articles:
        articles[keys]=list(map(str.lower, articles[keys]))
    with open("part3_reut2-004.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles

def porterStemmer(articles):
    ps = PorterStemmer()
    for keys in articles:
        articles[keys] = list(map(ps.stem, articles[keys]))
    with open("part4_reut2-004.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles

def removeStopWords(articles):
    words = input("Enter stop words separated by spaces: ")
    listWords = words.split(" ")
    for keys in articles:
        for token in reversed(articles[keys]):
            if token in listWords:
                articles[keys].remove(token)
    with open("part5_reut2-004.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles
    



def pipeline():
    dir = input("Enter the directory: ")
    articles = [] 
    articles = splitIntoArticles(dir, "reut2-004.sgm")
    articles = tokenize(articles)
    articles = toLowerCase(articles)
    articles = porterStemmer(articles)
    articles = removeStopWords(articles)

pipeline()

