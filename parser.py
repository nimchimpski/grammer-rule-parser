import nltk
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
import sys

from abc import ABCMeta, abstractmethod

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S ->  NP VP | VP DP |VP NP | VP PP | S Conj S | VP | NP

NP -> N | DP PP | Det N | AP N | Det AJP 
AJP -> Adj N | Adj AJP
VP -> V | NP VP | VP PP | VP AVP | NP AVP | VP NP
AVP -> Adv | Adv V
DP -> Det 
PP -> P NP | N P | PP N | P NP

"""

# DP -> Det NP | Det N
# NP -> N | Adj N | N Adj 
# VP -> V | NP VP | DP V | Adv V | VP NP |VP DP
# PP -> P NP | P DP
# PPS -> PP PPS | PP
# AP -> Adj N | Adj AP


# S -> VP | VP NP | VP DP PP | VP PP | S Conj S | VP DP | PP | S Adv | VP PPS

# DP -> Det NP
# NP -> N | Adj NP | N Adj
# VP -> V | NP VP | DP V | Adv V | VP NP |VP DP
# PP -> P NP | P DP |
# PPS -> PP PPS | PP

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    print(f"+++{s}")
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
        # print(f"---tree type= {type(trees)}")
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        # np_chunk(tree)
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Pre-process sentence by converting all characters to lowercase
    sentence = sentence.lower()

    # Convert `sentence` to a list of its words with tokenisation
    tokens = nltk.word_tokenize(sentence)
    # print(f"+++tokens= {tokens} \n{type(tokens)}")

    # remove punctuation
    toremove = []
    for word in tokens:
        # print(f"---{word}")

    # removing any word that does not contain at least one alphabetic character.
        counter = 0
        for i in word:
            if i.isalpha():
                counter += 1
        if counter == 0:
            # print(f"---counter={counter} removing= {word}")
            toremove.append(word)
        elif  counter  == 1 and word not in ["a", "i"]:
            # print(f"---removing {word}")
            toremove.append(word)
    for word in toremove:
        tokens.remove(word)

    # return a list of strings
    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
   
    def recursivechunkhunter(tree, chunklist=None):
        if chunklist is None:
            chunklist = []
        # print(f"\n\n+++recursivechunkhunter")
        # print(f"+++chunklist= {chunklist}")
        # print(f"+++tree.label()= {tree.label()}")

        ####    base case
        # print(f"---tree= {tree}")
        if tree.label() == 'NP':
            if not any(child.label() == 'NP' for child in tree if isinstance(child, Tree)):
                # print(f"\n---base case")
                chunklist.append(tree)
                # print(f"---chunklist= {chunklist}")
        ####    DO NOT RETURN ANYTHING ELSE THERE IS INSUFFICIENT BURROWING. CHUNKLIST CARRIES RESULT.
            
        ####    recursive case
        # print(f"---recursive case")
        for subtree in tree:
            if isinstance(subtree, Tree):
                recursivechunkhunter(subtree, chunklist)
        return chunklist
    
    result = recursivechunkhunter(tree)
    # print(f"---result= {result}")
    return result



if __name__ == "__main__":
    main()
