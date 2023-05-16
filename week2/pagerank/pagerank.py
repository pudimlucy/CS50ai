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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {}

    if corpus[page]:
        # Chance of chooosing link at random from pages in corpus
        for link in corpus:
            distribution[link] = (1 - damping_factor) / len(corpus)

        # Chance of chooosing link at random from links in page
        for link in corpus[page]:
            distribution[link] += damping_factor / len(corpus[page])
    else:
        # Chance of chooosing link at random from pages in corpus, given there's no links in page
        for link in corpus:
            distribution[link] = 1 / len(corpus)

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Sets all page's initial rankings to 0
    pagerank = {page: 0 for page in corpus}

    # Samples pages
    for _ in range(0, n):
        # If all rankings are 0, sample initial page
        if all(rank == 0 for rank in pagerank.values()):
            sample = random.choice(list(pagerank.keys()))
        else:
            # Sample page from previous page's transition model
            sample = random.choices(list(dist.keys()), list(dist.values()), k=1)[0]
        # Sets page's new ranking and gets it's transition model
        pagerank[sample] += 1 / n
        dist = transition_model(corpus, sample, damping_factor)

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    threshold = 0.001

    # Sets all page's initial rankings to 1 / N
    pagerank = {page: 1 / N for page in corpus}

    # Copies corpus, making pages with no links have links for every page
    new_corpus = {
        key: corpus[key] if corpus[key] != set() else set(corpus.keys())
        for key in corpus.keys()
    }

    # Applies pagerank formula, counting how many pages converged
    while True:
        count = 0
        # Iterates over every page
        for page in new_corpus:
            # Initial sum value
            rank = (1 - damping_factor) / N
            sigma = 0
            # Iterates over pages that link to current page
            for i in new_corpus:
                if page in new_corpus[i]:
                    # Increases sum
                    sigma += pagerank[i] / len(new_corpus[i])
            # Multiplies sum by damping factor and adds it to total value
            sigma *= damping_factor
            rank += sigma

            # Checks if page hit threshold
            if abs(pagerank[page] - rank) < threshold:
                count += 1
            
            pagerank[page] = rank

        if count == N:
            break

    return pagerank


if __name__ == "__main__":
    main()
