class Constraint:
    def __init__(self, check, actions):
        self.check = check # List of conditions that need to be met. I'm considering either making it all() instead of chaining ands. No clue which is faster. 
        # I do know what's cleaner. 
        self.actions = actions # List of assertions to be made. 
    def applies(self, pair):
        return all(check(pair) for check in self.check)
    def apply(self, pair):
        for action in self.actions:
            action(pair) 
    
