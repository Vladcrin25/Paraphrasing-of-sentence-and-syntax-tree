from main import paraphrase_sentence
from main import print_syntax_tree
from main import paraphrase_syntax_tree

sentence = input('Enter your sentence to paraphrase: \n')
print("Your sentence: \n", sentence)
original_tree = print_syntax_tree(sentence)
print("Syntax tree of your sentence:\n", original_tree)
paraphrased_sentence = paraphrase_sentence(sentence)
paraphrased_tree = paraphrase_syntax_tree(original_tree)
print("Paraphrased sentence:\n", paraphrased_sentence)
print("Paraphrased syntax tree: \n", paraphrased_tree)



