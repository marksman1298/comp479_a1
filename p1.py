import nltk, os, re, json
from nltk import word_tokenize
# from nltk.corpus import reuters
# from nltk.stem import porter
from nltk.stem.porter import PorterStemmer

# menu with loop?
# save outputs to file?

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
    return extractText(articles)
            
def extractText(articles):
    for key in articles:
        startText = articles[key].find("<TEXT>")
        endText = articles[key].find("</TEXT>")
        if startText != -1 and endText != -1:
            articles[key] = articles[key][startText:endText+7]
    with open("part1_reut2-004.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles

        
#remove
def cleanArticles(articles): #remove all tags and extra whitespace, maybe tokenize at same time?
    for key in articles:
        articles[key] = re.sub("<(.*?)>","" , articles[key])
        articles[key] = re.sub("&#(.*?);", "", articles[key])
        articles[key] = re.sub("\n\s*\n", "\n", articles[key])
        articles[key] = word_tokenize(articles[key])
    return articles
        

def tokenize(articles): #tokenize and inverse
    for key in articles:
        articles[key] = word_tokenize(articles[key])
    # inv_articles = {article: k for k, article in articles.items()}
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
#
dir = r'C:\Users\marks\OneDrive\Desktop\Fall-2021\COMP 479\reuters-21578'

def removeStopWords(articles):
    words = input("Enter stop words separated by spaces: ")
    listWords = words.split(" ")
    #list compressions?
    #articles2 = [word for word in articles if word not in listWords]
    for keys in articles:
        for token in articles[keys]:
            if token in listWords:
                articles[keys].remove(token)
    with open("part5_reut2-004.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles
    # for keys in articles:
    #     articles[keys] = list(map(list(filter((listWords).__ne__), articles[keys])), listWords)
    # return articles



def pipeline():
    dir = input("Enter the directory: ")
    articles = [] 
    articles = splitIntoArticles(dir, "reut2-004.sgm")
    articles = tokenize(articles)
    articles = toLowerCase(articles)
    articles = porterStemmer(articles)
    articles = removeStopWords(articles)

pipeline()
# print(len(articles))
#articles = makeDict(articles)

# print("Start first\n " + articles[0] + "\n end first")
# print("Start last\n " + articles[21578] + "\n end last")

#articles = cleanArticles(articles)
#articles = tokenize(articles)
#articles = toLowerCase(articles)
#articles = porterStemmer(articles)
#print("Start first\n ", articles["2"] , "\n end first")


# print(articles[2])
