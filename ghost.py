import sys
import re
import random

from ghost_util import *

WORD_LIST = 'ghost_words'

class GhostAgent:

    def __init__(self, name):
        self.score = 0
        self.name = name

    def add_loss(self):
        self.score += 1

    def get_score_string(self):
        return "GHOST"[0:self.score]

    # functions that must be implemented by inheriting classes:
    def get_move(self, game_state, n_players):
        #gets the current game state
        #returns a letter, or a bluff, or a surrender, taking the loss
        raise NotImplementedError

class HumanGhostAgent(GhostAgent):

    def get_move(self, game_state, n_players):
        while True:
            x = raw_input("Enter move, "+self.name+": ")

            match_ob = re.search("([A-Z]|bluff|surrender)",x)
            if match_ob:
                return match_ob.group(1)
            else:
                print "Bad input!"

class ComputerGhostAgent(GhostAgent):
    
    def __init__(self, *args):
        GhostAgent.__init__(self, *args)
        self.init_letter_tree()
        
    def init_letter_tree(self):
        lt = LetterTree.from_file(WORD_LIST)
        
        self.letter_tree = lt
        return lt
        
    def get_move(self, string, n_players):
        
        SHOW_THOUGHTS = True

        all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if SHOW_THOUGHTS:
            print "Getting dfd for all words (checking for possibility in process)"
            
        dfd_letter_hash = {}
        legal_letters = []
        for letter in all_letters:
            try:
                if SHOW_THOUGHTS:
                    print "checking %s:" % letter,
                
                # will raise InvalidWord if this is not possible    
                dfd = self.letter_tree.check_distance_from_death(string+letter, n_players)
                
                if SHOW_THOUGHTS:
                    print "found a dfd of %d" % dfd
                    
                dfd_letter_hash.setdefault(dfd, []).append(letter)
                legal_letters.append(letter)
                                
            except InvalidWordException:
                if SHOW_THOUGHTS:
                    print "no word down that path"
        
        # CHECK FOR NO OPTIONS, CALL BLUFF
        
        if not legal_letters:
            
            if SHOW_THOUGHTS:
                print "No legal letters! must be a bluff!"
            
            return 'bluff'
        
        #you could add person targeting here, but for now, just pick the maximum dfd
        best_dfd = max(dfd_letter_hash.keys())
        
        if SHOW_THOUGHTS:
            print "ok, the best dfd available is %d" % best_dfd
        

        if best_dfd > 0: #then there is a move that guareentee i don't lose
            
            if SHOW_THOUGHTS:
                print "I can guarentee I don't lose!"
                
            best_letters = dfd_letter_hash[best_dfd]
            
            if SHOW_THOUGHTS:
                print "The letters that would allow that are %s" % str(best_letters)

            #for now, picking a random letter, though there should be some sort of logic
            #to pick a letter that will quickly trip up other people? but foo, whatever
            chosen = random.choice(best_letters)
            if SHOW_THOUGHTS:
                print "im going to randomly choose %s" % chosen
                
            return chosen
            

            
        else:
            if SHOW_THOUGHTS:
                print "shit. I can't guareentee a win."
            ########## what to do if theres not a winning answer!!!!!????
            # for now, stupidly just pick a random one
            chosen = random.choice(legal_letters)
            if SHOW_THOUGHTS:
                print "so just going to pick %s" % chosen
                
            return chosen

def play_game(*player_types):
    """
    players is the order
    h,h for human human,
    h,c for human computer
    c,h,c for computer human computer
    """
    
    players = []
    
    player_count = len(player_types)
    human_count = 0
    computer_count = 0
    
    for player_type in player_types:
        if player_type == 'h':
            players.append(HumanGhostAgent('human%d'%human_count))
            human_count += 1
        else:
            players.append(ComputerGhostAgent('computer%d'%computer_count))
            computer_count += 1
    
    print "Starting Ghost!"
    active = 0
    while True: # round loop
        print "Scores:"
        for player in players:
            print player.name+":", player.get_score_string()
            
        print "%s starts" % players[active].name
        string = players[active].get_move('', player_count)
        active = (active + 1) % player_count
        
        raw_input()
        
        alive = True
        while alive:
            print "String: %s" % string
            print "It's %s's move" % players[active].name
            move = players[active].get_move(string, player_count)
            active = (active + 1) % player_count
            
            string += move
            
            raw_input()
            
        
         
        
        

    
if __name__ == '__main__':
    import sys
    players = sys.argv[1:]
    play_game(*players)
