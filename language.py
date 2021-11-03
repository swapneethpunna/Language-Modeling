"""
Language Modeling Project
Name:
Roll No:
"""

import language_tests as test

project = "Language" # don't edit this

### WEEK 1 ###

'''
loadBook(filename)
#1 [Check6-1]
Parameters: str
Returns: 2D list of strs
'''
def loadBook(filename):
    lst=[] 
    f=open(filename) 
    x=f.read()
    y=x.splitlines()
    # print(x)
    for line in y: 
        if len(line)!=0:
            # i=line.split(" ")
            lst.append(line.split())
            # print(eachline) 
            # lst.append(i) 
    # print(lst) 
    return lst


'''
getCorpusLength(corpus)
#2 [Check6-1]
Parameters: 2D list of strs
Returns: int
'''
def getCorpusLength(corpus):
    length=0
    for row in range (len(corpus)):
        for col in range (len(corpus[row])):
            length+=1
    return length


'''
buildVocabulary(corpus)
#3 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def buildVocabulary(corpus):
    unique=[]
    for row in corpus:
        for col in row:
            if col not in unique:
                unique.append(col)
    return unique


'''
countUnigrams(corpus)
#4 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countUnigrams(corpus):
    dict={}
    for row in corpus:
        for col in row:
            if col not in dict:
                dict[col]=1
            else:
                dict[col]+=1
    return dict


'''
getStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def getStartWords(corpus):
    newlst=[]
    for i in corpus:
        if i[0] not in newlst:
            newlst.append(i[0])    
    return newlst


'''
countStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countStartWords(corpus):
    dict_={}
    for i in corpus:
        if i[0] not in dict_:
            dict_[i[0]]=1
        else:
            dict_[i[0]]+=1
    return dict_

'''
countBigrams(corpus)
#6 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def countBigrams(corpus):
    dicti_={}
    for row in corpus:
        for col in range(len(row)-1):
            if row[col] not in dicti_:
                dicti_[row[col]]={}
            if row[col+1] not in dicti_[row[col]]:
                dicti_[row[col]][row[col+1]]=1
            else:
                dicti_[row[col]][row[col+1]]+=1
    return dicti_


### WEEK 2 ###

'''
buildUniformProbs(unigrams)
#1 [Check6-2]
Parameters: list of strs
Returns: list of floats
'''
def buildUniformProbs(unigrams):
    newlst=[]
    for i in unigrams:
            newlst.append(1/len(unigrams))
    return newlst


'''
buildUnigramProbs(unigrams, unigramCounts, totalCount)
#2 [Check6-2]
Parameters: list of strs ; dict mapping strs to ints ; int
Returns: list of floats
'''
def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    emptylist=[]
    for i in unigrams:
        if i in unigramCounts:
            count=unigramCounts[i]/totalCount
            emptylist.append(count)
    return emptylist


'''
buildBigramProbs(unigramCounts, bigramCounts)
#3 [Check6-2]
Parameters: dict mapping strs to ints ; dict mapping strs to (dicts mapping strs to ints)
Returns: dict mapping strs to (dicts mapping strs to (lists of values))
'''
def buildBigramProbs(unigramCounts, bigramCounts):
    newdict_ = {}
    for prevWord in bigramCounts:
        word = []
        prob = []
        for key,value in bigramCounts[prevWord].items():
            word.append(key)
            prob.append(value / unigramCounts[prevWord]) 
            temp = {}
            temp["words"] =word
            temp["probs"] = prob
        newdict_[prevWord] = temp
    return newdict_


'''
getTopWords(count, words, probs, ignoreList)
#4 [Check6-2]
Parameters: int ; list of strs ; list of floats ; list of strs
Returns: dict mapping strs to floats
'''
import operator
def getTopWords(count, words, probs, ignoreList):
    dictionary={}
    dictionary1={}
    for i in range(len(words)):
        if words[i] not in ignoreList:
            dictionary[words[i]]=probs[i]
    common = dict(sorted(dictionary.items(), key=lambda x:x[1], reverse=True))
    for i,j in common.items():
        if len(dictionary1) != count and i not in ignoreList:
            dictionary1[i] = j
    return dictionary1
            


'''
generateTextFromUnigrams(count, words, probs)
#5 [Check6-2]
Parameters: int ; list of strs ; list of floats
Returns: str
'''
from random import choices
def generateTextFromUnigrams(count, words, probs):
    string=""
    for i in range((count)):
        x=choices(words, weights=probs)
        string=string+x[0]+ ' '
    return string


'''
generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs)
#6 [Check6-2]
Parameters: int ; list of strs ; list of floats ; dict mapping strs to (dicts mapping strs to (lists of values))
Returns: str
'''
def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    text=""
    words = choices(startWords, weights = startWordProbs)
    text += words[0]
    lst = text
    for i in range(count-1):
        if lst != '.':
            if lst in bigramProbs:
                lst = choices(bigramProbs[lst]["words"], weights = bigramProbs[lst]["probs"])[0]
                text = text + ' ' + lst
        else:
            words = choices(startWords, weights = startWordProbs)
            text =text+' '+ words[0]
            lst = words[0]
    return text


### WEEK 3 ###

ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]

'''
graphTop50Words(corpus)
#3 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTop50Words(corpus):
    words=buildVocabulary(corpus)   
    unigramcount=countUnigrams(corpus)
    count=getCorpusLength(corpus)
    unigramprobs=buildUnigramProbs(words, unigramcount, count)
    topwords=getTopWords(50, words, unigramprobs, ignore)
    plot=barPlot(topwords, "top 50 words")
    return plot


'''
graphTopStartWords(corpus)
#4 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTopStartWords(corpus):
    return


'''
graphTopNextWords(corpus, word)
#5 [Hw6]
Parameters: 2D list of strs ; str
Returns: None
'''
def graphTopNextWords(corpus, word):
    return


'''
setupChartData(corpus1, corpus2, topWordCount)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int
Returns: dict mapping strs to (lists of values)
'''
def setupChartData(corpus1, corpus2, topWordCount):
    return


'''
graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; str ; 2D list of strs ; str ; int ; str
Returns: None
'''
def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    return


'''
graphTopWordsInScatterplot(corpus1, corpus2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int ; str
Returns: None
'''
def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    return


### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.
"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title)

    plt.show()

"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35  # the width of the bars

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    # a bit of advanced code to draw a y=x line
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek1()
    # test.testGetCorpusLength()
    # test.testGenerateTextFromBigrams()

    ## Uncomment these for Week 2 ##
# """
#     print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
#     test.week2Tests()
#     print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
#     test.runWeek2()
# """

    ## Uncomment these for Week 3 ##

    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
