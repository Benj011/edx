import string
import nltk
import sys
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    path = os.getcwd()
    directories = os.listdir(directory)
    files = {}

    path = os.path.join(path, directory)
    
    directories = os.listdir(path)
    for file in directories:
        if file.endswith('.txt'):
            with open(os.path.join(path, file), 'r') as f:
                files[file] = f.read()

    return files

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    text = document

    text = text.lower()
    stopWords = set(nltk.corpus.stopwords.words("english"))
    punctuation = set(string.punctuation)
    words = nltk.word_tokenize(text)
    goodWords = []
    for word in words:
        if word not in stopWords and word not in punctuation:
            goodWords.append(word)

    return goodWords


    raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    wordDict = {}

    for document in documents:
        wordFound = {}

        for word in documents[document]:
            if word in wordFound:
                continue
            wordFound[word] = True
            if word not in wordDict:
                wordDict[word] = 1
            else:
                wordDict[word] += 1

    for word in wordDict:
        wordDict[word] = len(documents) / wordDict[word]
        wordDict[word] = math.log(wordDict[word])


    return wordDict

    raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    ranking = [None] * n
    fileRanking = {}

    for file in files:
        tfidf = 0
        for word in query:
            wordTf = files[file].count(word)
            tfidf += wordTf * idfs[word]
        fileRanking[file] = tfidf

    for i in range(n):
        maxVal = max(fileRanking.values())
        for file in fileRanking:
            if fileRanking[file] == maxVal:
                ranking[i] = file
                del fileRanking[file]
                break
    return ranking

    raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    sentenceScores = [] 

    for sentence in sentences:
        qWordCount = 0
        idf = 0
        wordCount = len(sentences[sentence])
        
        for word in query:
            density = 0
            if word in sentences[sentence]:
                idf += idfs[word]
                qWordCount += 1

        if qWordCount == 0:
            continue
        else:
            density = qWordCount / wordCount
        
        
        
        sentenceScores.append((sentence, idf, density))
    
    

    ranking = [None] * n 
    currentSentence = (0, 0, 0)
    for i in range(n):
        for sentence in sentenceScores:
            if sentence[1] > currentSentence[1]:
                currentSentence = sentence
            elif sentence[1] == currentSentence[1]:
                if sentence[2] > currentSentence[2]:
                    currentSentence = sentence
        
        ranking[i] = currentSentence[0]
        sentenceScores.remove(currentSentence)
        currentSentence = (0, 0, 0)

        
       
    
        
    return ranking


    raise NotImplementedError


if __name__ == "__main__":
    main()
