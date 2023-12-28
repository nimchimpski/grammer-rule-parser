import nltk
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
S -> NP | VP | PP | VP NP | VP NP PP | VP PP | S Conj S 


NAP -> N | Adj NAP | NAP PP
NP -> Det NAP |Det NAP Adv
PP -> P NP | P NAP
VAP -> V |Adv VAP |VAP Adv
VP -> NAP VAP | VAP NAP | VAP NP | NP VAP

"""

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
    print(f"+++tree type= {type(tree)}")
    print(f"+++tree.subtrees()= {type(tree.subtrees())}")
    for i in tree.subtrees():
        if i.label() == 'NAP':
            print(f"---{i}")
    # entities = nltk.chunk.ne_chunk(NAP)
    # result = entities
    return []


if __name__ == "__main__":
    main()
