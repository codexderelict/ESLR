import re
from .rules import rules
class Word:
    def __init__(self, lemma, position):
        self.lemma = lemma 
        self.position = position
        self.readings = self.get_readings(lemma)
        if not self.readings: # If no regexes match the word
            raise ValueError("Morphological check failure")
        self.pfeats = self.get_potential() # Potential features
        self.dfeats = self.get_definite() # Definite features
    def get_readings(self, lemma): 
        for k, v in rules.items(): 
            if re.search(k, lemma):
                return v
    @property 
    def ambiguous(self): 
        return len(self.readings) > 1 # If there's only one reading, then it is not ambiguous. 
    def get_potential(self): 
        potential_dict = {'head': None, 'dep': None} # The constraint list starts with head and dependent definitions before constraining features.
        for reading in self.readings:
            for k, v in reading.items():
                values = set(v) if isinstance(v, list) else {v} 
                # I'm using sets to disallow overlap between two readings. If two readings are nouns, I don't want "N N", I just want "N". 
                if k not in potential_dict: 
                    potential_dict[k] = values.copy() # Put key in if it is not in there 
                else:
                    potential_dict[k].update(values) # Add it to the set if it is 
        return potential_dict
    def get_definite(self):
        if not self.ambiguous:
            return self.readings
        else:
            return {} # Empty dict for partial readings. 
    def make_assertion(self, k, v):
        if isinstance(v, (list, set)): # If the value of the assertion made is a list or set, it's a set (same reason, lack of duplicates and ease of use)
            value = set(v)
        elif isinstance(v, str):
            value = {v}
        else:
            value = v 
        self.dfeats[k] = value 
        
    def check(self, k, v):
        if k not in self.pfeats:
            return False 
        domain = self.pfeats[k]
        if isinstance(v, (set, list)):
            return bool(domain & set(v)) # If they intersect (i.e. there's a common element between the two)
        else:
            return v in domain # If it's just one string to be checked, it checks if it's in the set at hand. This is so that I can do something like:
            # Word.check("case", "acc"). Easy. 
    def intersect(self):
        for key, value in self.pfeats.items():
            if key in self.dfeats:
                self.pfeats[key] &= self.dfeats[key] # This is also why I used a set. Intersection logic is easy.
        self.dfeats = {k: v.copy() for k, v in self.pfeats.items()} # I forgot about dict comprehensions.
    def prune(self):
        if self.ambiguous: 
            self.intersect() 
            bad_readings = []
            good_readings = []
            for reading in self.readings:
                unifiable = True 
                for key, value in reading.items():
                    if key in self.dfeats and value not in self.dfeats[key]:
                        unifiable = False # It's not unifiable, so it's immediately appended to bad readings instead of much later. 
                        break 
                if unifiable: # Only called if it survives the rest 
                    good_readings.append(reading)
                else:
                    bad_readings.append(reading)
            self.readings = good_readings # We separate those that make the cut first and that becomes the new one 
            return bad_readings 
            # Bad readings are stored. Not sure what I'd need them for at this moment but it's good to have it around
            # if I want to add a new fun feature.

