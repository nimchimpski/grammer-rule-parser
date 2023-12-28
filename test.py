import nltk

# Assume 'tree' is your existing parse tree
# For example:
tree_str = "(S (NP The/DT cat/NN) (VP chased/VBD (NP the/DT mouse/NN)))"
tree = nltk.Tree.fromstring(tree_str)

# Extract POS tagged words
tagged_words = tree.pos()

# If you need it in a specific string format:
tagged_sentence = ' '.join([f'{word}/{tag}' for word, tag in tagged_words])

print(tagged_sentence)