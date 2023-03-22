class Player:
    def __init__(self, is_computer):
        self.is_computer = is_computer
        self.current_card
        self.hand = []
        self.possible_cards = []
        self.is_authority
        self.is_turn_used
        self.is_uno = False
    
    def press_uno(self):
        if self.is_authority == True and len(self.hand):
            self.is_uno = True
            
    def use_card(self, index):
        self.current_card = self.hand[index]
        self.hand.remove(index)
        self.is_turn_used = True
    
    def get_card(self):
        GameManager.give_card(GameManager.turn)
        self.is_turn_used = True

class User(Player):
    def __init__(self, is_computer):
        self.is_computer = is_computer
        
class Computer(Player):
    def __init__(self, is_computer):
        self.is_computer = is_computer
    
    def computer_play(self):
        for i in range(len(self.hand)):
            if GameManager.GraveTop.color == hand[i].color or GameManager.GraveTop.num == hand[i].num:
                self.possible_cards.append[ self.hand[i] ]
            
        if len(self.possible_cards) != 0:
            ran = random.randrange(len(self.possible_cards))
            self.use_card(ran)
        else:
            self.get_card()
        
        if len(self.hand) == 1:
            self.press_uno()
