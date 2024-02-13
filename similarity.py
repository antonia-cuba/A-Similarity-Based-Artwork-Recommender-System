import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

# create list with all non-duplicate words from a file
def wordsArray(f):
    # access the text file
    file = open(f, 'r')
    l = []
    # iterate over each line in the text file
    for lines in file:
        # split the line at quote, each word goes into the list
        words = lines.split('"')
        for w in words:
            # take only the words, non-duplicate
            if w.isalpha() and w not in l:
                l.append(w)
    return(l)


# create two words vectors, one for each input list of words
# 1 if the word appears in the list, 0 otherwise
# number of elements of each vector is the number of non-duplicate words from the union of the two lists
def wordVectors(l1, l2):
    a1 = []
    a2 = []

    # a set of all words from the two lists, each word appears once
    global allWords
    allWords = set(l1).union(l2)
    # create vectors of word appearances of form [1, 0, ..., 0, 1, 0]
    for w in allWords:
        if w in l1:
            a1.append(1)
        else:
            a1.append(0)
        if w in l2: 
            a2.append(1)
        else:
            a2.append(0)

    return a1, a2


# compute similarity value between two word vectors of the form [1, 0, 0, ..., 1, 1] with COSINE SIMILARITY
def similarity_cos(a1, a2):

    # CLASSIC VERSION WITH MATHEMATICAL FORMULAS - norm and dot product
    normV1 = sum(i ** 2 for i in a1) ** 0.5
    normV2 = sum(i ** 2 for i in a2) ** 0.5
    dotProduct = sum(a1[k] * a2[k] for k in range(len(allWords)))

    if(normV1 == 0 or normV2 == 0):
        return ("One of the files does not have the desired 'topic-words' format. Could not extract words from topics.")
    else:
        cos = dotProduct / (normV1 * normV2)
        return cos

    # VERSION WITH sklearn LIBRARY
    # transform the vectors from 1D to 2D, in order for sklearn cosine_similarity to work
    #a1 = np.reshape(a1, (1, -1))
    #a2 = np.reshape(a2, (1, -1))
    
    #if(len(a1) == 0 or len(a2) == 0):
    #    return ("One of the files does not have the desired 'topic-words' format. Could not extract words from topics.")
    # return just the value, without brackets (the result is a 2D array)
    #else:
    #    return cosine_similarity([a1], [a2])[0][0]


# compute similarity value between two word vectors of the form [1, 0, 0, ..., 1, 1] with the JENSEN-SHANNON DISTANCE
def similarity_jensen(a1, a2):
    return distance.jensenshannon(a1,a2)


# COSINE SIMILARITY
# compute the similarity value between one specified file and all files from "Result Topics" folder using COSINE SIMILARITY
def computeSimilarity1(file1):
    global d
    d = {}
    f1 = wordsArray(file1)
    directory = "Result Topics"
    # iterate through all files in directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            f2 = wordsArray(f)
            a, b = wordVectors(f1, f2)
            # print("Cosine similarity: " + str(similarity_cos(a, b)))
            # print("Jensen similarity: " + str(similarity_jensen(a,b)))
            # print("........................")
            d[f] = similarity_cos(a, b)

    # for when using COSINE SIMILARITY - descending order (biggest similarity first) - sort dictionary
    return dict(sorted(d.items(), key = lambda item: item[1], reverse=True))

# JENSEN-SHANNON DISTANCE
# compute the similarity value between one specified file and all files from "Result Topics" folder using JENSEN-SHANNON DISTANCE
def computeSimilarity2(file1):
    global d
    d = {}
    f1 = wordsArray(file1)
    directory = "Result Topics"
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            f2 = wordsArray(f)
            a, b = wordVectors(f1, f2)
            # print("Jensen similarity: " + str(similarity_jensen(a,b)))
            # print("........................")
            d[f] = similarity_jensen(a, b)
    
    # for when using JENSEN SIMILARITY - ascending order (lowest similarity first) - sort dictionary
    return dict(sorted(d.items(), key = lambda item: item[1]))


# SBERT encodding
# compute the similarity value between one specified file and all files from "Result Topics" folder using SBERT
def computeSimilarity3(file1):
    global d
    d = {}
    f1_embedding = model.encode(file1)
    directory = "Result Topics"
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            f2_embedding = model.encode(f)
            d[f] = cosine_similarity([f1_embedding], [f2_embedding])[0][0]
            # print(cosine_similarity([f1_embedding], [f2_embedding])[0][0])

    # for when using COSINE SIMILARITY - descending order (biggest similarity first) - sort dictionary
    return dict(sorted(d.items(), key = lambda item: item[1], reverse=True))
