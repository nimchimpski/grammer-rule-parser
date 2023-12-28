import nltk
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
import sys

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
S -> VP | VP NP | VP DP PP | VP PP | S Conj S | VP DP | PP | S Adv | VP PPS

DP -> Det NP
NP -> N | Adj NP | N Adj
VP -> V | NP VP | DP V | Adv V | VP NP |VP DP
PP -> P NP | P DP
PPS -> PP PPS | PP



"""
# S -> NPX | VP | PP | VP NPX | VP NPX PP | VP PP | S Conj S 

# NP -> N | Adj NP | NP PP
# NPX -> Det NP |Det NP Adv
# PP -> P NPX | P NP
# VAP -> V |Adv VAP |VAP Adv
# VP -> NP VAP | VAP NP | VAP NPX | NPX VAP

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
        np_chunk(tree)
        # for np in np_chunk(tree):
            # print(" ".join(np.flatten()))


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

    # print(f"---tree.flatten= {tree.flatten()}")
    #####         just gives me the short end  branches
    # for i in tree.subtrees(lambda tree: tree.label() == 'NP'):
        # print(f"---i.label= {i.label()}")
  
        # print(f"---i.leaves= {i}")

    # get flattened tree with labels

    # tree_str = tree.pformat()
    # print(f"---tree_str= {tree_str}")

    # define tags
    # NP_pattern = "<DT>?<JJ>*<NN.*>"
    # THIS NOT WORKING = CREATS REGEX W/EXTRA ()'s
    # regexp_pattern = tag_pattern2re_pattern(NP_pattern)
    # print(f"---regexp_pattern= {regexp_pattern}")
    # SHOULD BE THIS

    # tagged_text = "[ The/DT cat/NN ] sat/VBD on/IN [ the/DT mat/NN ] [ the/DT dog/NN ] chewed/VBD ./."
    # gold_chunked_text = tagstr2tree(tagged_text)
    # unchunked_text = gold_chunked_text.flatten()


    # regexp_pattern = r'(<DT>)(<JJ>)*(<NN.*>)'

    # print(f"---regexp_pattern= {regexp_pattern}")
    # chunk_rule = ChunkRule(r'<DT><JJ>*<NN.*>', "Chunk NPs")
    # chunk_parser = RegexpChunkParser([chunk_rule], chunk_label = "NP")
    # print(f"---unchunked_text= {unchunked_text}")
    # chunked_text= chunk_parser.parse(unchunked_text)
    # print(f"---chunked_text= {chunked_text}")
    
    
    return []


if __name__ == "__main__":
    main()
