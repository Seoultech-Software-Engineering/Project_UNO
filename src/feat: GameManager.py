class GameManager:
    def __init__(self):
        self.turn = 0 # 지금 누구 턴인지 나타내는 정수 변수
        self.turn_count_down # 유저의 해당 턴 몇초남았는지 나타낼 정수 변수
        self.game_count_down # 해당 게임 몇초 남았는지 나태닐 정수 변수
        self.attack_int # 누가 공격카드 쓰면, 그 값을 받는데 쓸 정수 변수
        self.is_attack # 턴 시작시, 공격 카드를 썼는지 판별할 불린 변수
        self.players = [] # 플레이어 객체들을 담을 배열
        self.real_player_count # 실제 플레이어 수가 몇 인지 나타낼 정수 변수
        self.player_num # 전체 플레이어 수
        self.computer_count # 컴퓨터의 수가 몇인지 나타낼 정수 변수
        self.start_cards_integer # 카드 몇장가지고 시작할건지 나타낼 정수 변수
        self.deck = [] # 덱
        self.grave = [] # 묘지, Top 부분은 플레이어들에게 색과 숫자가 보인다.
        self.grave_top # 묘지의 탑을 참조하는 Card 타입 변수
        self.is_someone_win # 누가 핸드 갯수가 0이 되서 우승한 건지 판별하는 불린변수
        self.turn_jump_num = 0 # 누가 턴 건너뛰기를 했으면 여기에 값이 설정되는 정수 변수
    
    
    # 게임 맨처음 시작시 각종 설정 초기화 해주는 함수    
    def game_start(self):
        # 추후에 다중 플레이어 게임을 고려한 코드인데, 추후 수정 가능성 있음
        # 게임 시작전에, 다중 플레이어들의 수를 받고, 미리 플레이어 객체를 생성한걸
        # 받아와서 여기다가 붙혀넣는 것
        for i in range(len(self.real_player_count)):
            self.players.append[pre_enrolled_players[i]]
        
        # 컴퓨터 수 만큼 players에 컴퓨터 객체 집어넣음
        for i in range(len(self.computer_count)):
            self.players.append[Computer(true, 10+i)]
        
        self.player_num = len(self.players)

        self.players.random.shuffle()
        
        # 덱 초기화    
        self.set_deck()
        # 덱 셔플
        self.card_shuffle()
        
        # 플레이어들에게 카드 나눠줌
        for i in range(self.start_cards_integer):
            for j in range(len(self.players)):
                self.give_card(j+1)
        
        # 덱에서 카드 한장 빼서 세팅해놓음
        self.set_card()
    
    def game_end(self):
        if self.is_someone_win == True:
            pass
        else:
            min = 100000
            minIndex = 0

            for i in range(self.player_num):
                temp = self.player_score_calculate(i)

                if temp < min:
                    min = temp
                    minIndex = i
            
    # 턴 시작 함수
    def turn_start(self):
        # 전 턴에 누가 공격 카드 썼는지 판별
        # 누가 공격 카드를 썼다면, attack_int 만큼 카드주고 6초 기다린후 턴종료
        if self.is_attack == True:
            
            for i in range(self.attack_int):
                self.give_card(self.turn)
            
            pygame.time.wait(6000)
            
            self.is_attack == False
            self.attack_int = 0
            
            self.turn_end()
        # 안 썼다면, 해당 플레이어가 컴퓨터인지 유저인지 판별한다.
        else:
            self.count_down()
            
            if self.players[self.turn].is_computer == True:
                self.players[self.turn].computer_play
            else:
                self.give_authority(self.turn)
                
    # 턴 끝 함수
    def turn_end(self):
        
        # 현재 핸드가 0인지 판별
        if self.players[self.turn].hand == 0:
            self.is_someone_win = True
            self.game_end()
        # 아니면 턴 1 증가시키고 다음 턴 스타트
        else:
            if self.players[self.turn].hand == 1 and self.players[self.turn].is_uno == False:
                self.give_card(self.turn)
            
            self.turn += 1 + self.turn_jump
            
            self.turn_jump_num = 0
            
            # 턴값이 플레이어 수를 넘어가면 와일문 돌려서 빼준다.
            while turn >= self.player_num:
                turn -= self.player_num
                
            self.players[self.turn].is_authority = False
            self.players[self.turn].is_turn_used = True
                
            pygame.time.wait(5000)
            
            
            self.turn_start()
    
    def give_card(self, a):
        # a는 해당 번호의 플레이어
        self.players[a].hand.append(self.deck.pop())
        
    def get_card(self):
        self.grave.append(self.players[self.turn].current_card)
        self.grave_top = self.grave[len(self.grave) - 1]
        
        # 이후 기술 카드면 기술카드 함수 실행
        pass

    def player_score_calculate(self, a):
        pass
    
    def give_authority(self):
        self.players[self.turn].is_authority = True
        self.players[self.turn].is_turn_used = False
        
    def turn_jump(self, jump):
        self.turn_jump_num = jump
    
    def turn_reverse(self):
        self.players.reverse()
        self.turn = (self.player_num-1) - self.turn
    
    def attack(self, a):
        self.attack_int = a
        self.is_attack = True
    
    def current_game_count_down(self):
        while self.game_count_down > 0 and self.is_someone_win == False:
            self.game_count_down -= 1
    
    def current_turn_count_down(self):
        while self.turn_count_down > 0 and self.players[self.turn].is_turn_used == False:
            self.turn_count_down -= 1
