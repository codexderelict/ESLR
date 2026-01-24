from .pair import Pair
class Sentence: 
    def __init__(self, word_list):
        self.word_list = word_list # Passing in the sentence as an array of Word objects 
        self.pairs = self.make_pairs(word_list) # Creates nC2 combinations 
    @staticmethod
    def make_pairs(word_list):
        pairs = [] 
        for i, word1 in enumerate(word_list): # For each word in the list 
            for word2 in word_list[i+1:]: # For each word after it 
                    pairs.append(Pair(word1, word2)) # Appends both combinations as order matters
                    pairs.append(Pair(word2, word1))
        return sorted(pairs, key=lambda pair: abs(pair.difference))
    def pair_apply(self):
        for pair in self.pairs: 
            pair.apply_constraints()
    def prune(self):
        for word in self.word_list:
            word.prune()
    def run(self):
        self.pair_apply()
        self.prune()