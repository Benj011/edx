import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def checkSum(dictionary):
    count = 0

    for page in dictionary:
        count += dictionary[page]
        
    if count == 1:
        print("Sum is 1")
    else:
        print("Sum is not 1")
        print(count)
        print(dictionary)


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    distro = {}

    # If the page has no links they all have the same rabdom chance

    if len(corpus[page]) == 0:
        for p in corpus:
            distro[p] = 1 / len(corpus)
        return distro
    
    linked = corpus[page]

    if page in linked:
        linked.remove(page)

    linked = list(set(linked))

    # i have to find all reachable pages in the corpus sio

    for p in corpus:
        if p in linked:
            distro[p] = damping_factor / len(linked)
        else:
            distro[p] = (1 - damping_factor) / (len(corpus) - len(linked))
            
    return distro

    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pageRank = {}

    randomInt = random.randint(0, len(corpus) - 1)

    for page in corpus:
        pageRank[page] = 0

    sample = list(corpus.keys())[randomInt]

    pageRank[sample] += 1

    for i in range(n):
        transition = transition_model(corpus, sample, damping_factor)
        sample = random.choices(list(transition.keys()), weights=transition.values(), k=1)[0]
        pageRank[sample] += 1

    for page in pageRank:
        pageRank[page] /= n

    return pageRank

    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pageRank = {}
    for p in corpus:
        pageRank[p] = 1 / len(corpus)


    while True:
        newPageRank = {}
        for p in corpus:
            newPageRank[p] = (1 - damping_factor) / len(corpus)
            for i in corpus:
                if len(corpus[i]) == 0:
                    newPageRank[p] += damping_factor * (pageRank[i] / len(corpus))
                if p in corpus[i]:
                    newPageRank[p] += damping_factor * (pageRank[i] / len(corpus[i]))

        if all(abs(pageRank[p] - newPageRank[p]) < 0.001 for p in corpus):
            break
        else:
            pageRank = newPageRank


    return pageRank
    raise NotImplementedError


if __name__ == "__main__":
    main()


