import os, re, json
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from typing import List, Dict

def splitIntoArticles() -> List[str]: #read all files in directory, put everything into one string, split into list of articles 
    data = ""
    try:
        dir = input("Enter the directory: ")
        listOfFiles = os.listdir(dir)
    except Exception as e: 
        print(e)
        return 
    specificFile = input("Enter a specific file: ")
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

    

def makeDict(listOfArticles: List) -> Dict: #want to get all newids of articles, then add them to a list, then combine both lists into dictionary with key new id : value article
    articles = {}
    ids = []
    specificArticle = input("Enter desired articles separated by space: ")
    listArticles = specificArticle.split(" ")
    for i in range(len(listOfArticles)): 
        foundNewID = re.search('NEWID="([0-9]+)"', listOfArticles[i])
        if foundNewID is not None:
            newId = re.search('[0-9]+', foundNewID.group(0))
            if newId is not None:
                ids.append(newId.group(0))
    articles = {ids[i]: listOfArticles[i] for i in range(len(ids))}
    
    if not len(listArticles) == 0:
        tableArticles = {} 
        for articleId in listArticles:
            try:
                tableArticles[articleId] = articles[articleId]
            except Exception as e:
                print("Not a valid key", e)
                return extractText(articles)
        return extractText(tableArticles)
       
    return extractText(articles)
            
def extractText(articles: Dict) -> Dict: #get all information between the text tags for each article
    for key in articles:
        startText = articles[key].find("<TEXT>")
        endText = articles[key].find("</TEXT>")
        if startText != -1 and endText != -1:
            articles[key] = articles[key][startText:endText+7]
    with open("part1_article5.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles
     
def tokenize(articles: Dict)-> Dict: #tokenize 
    if not articles:
        print("Dictionary is empty")
        return
    for key in articles: 
        articles[key] = word_tokenize(articles[key])
    with open("part2_article5.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles

def toLowerCase(articles: Dict)-> Dict: #lower case all values in the strings
    if not articles:
        print("Dictionary is empty")
        return
    for keys in articles:
        articles[keys]=list(map(str.lower, articles[keys]))
    with open("part3_article5.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles

def porterStemmer(articles: Dict)-> Dict:
    if not articles:
        print("Dictionary is empty")
        return
    ps = PorterStemmer()
    for keys in articles:
        articles[keys] = list(map(ps.stem, articles[keys]))
    with open("part4_article5.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles

def removeStopWords(articles: Dict, stopWords:List)-> Dict:
    if not articles:
        print("Dictionary is empty")
        return
    for keys in articles:
        for token in reversed(articles[keys]):
            if token in stopWords:
                articles[keys].remove(token)
    with open("part5_article5.txt", "w") as outfile:
        json.dump(articles, outfile)
    return articles
    



def pipeline():
    articles = [] 
    articles = splitIntoArticles() 
    articles = tokenize(articles)
    articles = toLowerCase(articles)
    articles = porterStemmer(articles)
    words = input("Enter stop words separated by spaces: ")
    stopWords = words.split(" ")
    articles = removeStopWords(articles, stopWords)

pipeline()

