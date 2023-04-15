import pygame, pickle, setting
from constant import *
from menu import Menu

# 몇 번 스토리에 들어가려고 하는 중인지에 대한 정보 (확인 창에서 사용)
# 덤으로 -1일 경우에는 확인 창을 치우는 역할도 합니다.
enter_story = -1

# 2차 요구사항 - '대전을 시작할 것인지 묻는 창'
class StoryConfirm(Menu):
    stage_map = ("공릉역", "철길", "쪼매떡", "미래관")
    avail_menu = ("OK", "Cancel")
    axis = "x"
    pos_formula = lambda self, i: (self.size[0] * (0.35 + 0.3 * i), self.size[1] * 0.6)
    global enter_story

    def draw(self, screen):
        super().draw(screen)
        # 확인 메시지 출력
        font = setting.get_font(70)
        text = font.render(f"{self.stage_map[enter_story]}에서 스토리 대전을 시작하시겠습니까?", True, "Black")
        pygame.draw.rect(screen, "White", text.get_rect(center=(self.size[0] / 2, self.size[1] * 0.25)))

        text_rect = text.get_rect(center=(self.size[0] / 2, self.size[1] * 0.25))
        screen.blit(text, text_rect)
    
    # 메뉴 선택 시 처리
    def select_menu(self, index):
        global enter_story
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)
        # 스토리 다음 버튼 = 돌아가기 버튼
        if self.avail_menu[index] == "OK":
            print(f"{enter_story}번 스토리 시작")
        else:
            enter_story = -1


class StoryMenu(Menu):
    # 현재 몇 개의 스토리?
    story_amount = 4

    # 스토리 진행도 (몇 번 스토리까지 클리어?)
    story_progress = 0

    # x축 정렬 메뉴? y축 정렬 메뉴?
    axis = "x"

    # 가능한 메뉴 목록
    avail_menu = ("", "", "", "", "돌아가기")

    # 버튼이 있어야 할 위치 반환
    def pos_formula(self, i):
        if i == 0:
            return (self.size[0] * 0.1, self.size[1] * 0.7)
        elif i == 1:
            return (self.size[0] * 0.4, self.size[1] * 0.25)
        elif i == 2:
            return (self.size[0] * 0.6, self.size[1] * 0.6)
        elif i == 3:
            return (self.size[0] * 0.9, self.size[1] * 0.15)
        else:
            return (self.size[0] * 0.5, self.size[1] * 0.8)
    
    
    def draw(self, screen):
        super().draw(screen)

        # 꼼수: 안 열린 버튼 shadow로 덮어씌우기
        shadow_x = 374 * 0.75 * setting.get_screen_scale()
        shadow_y = 374 * 0.75 * setting.get_screen_scale()
        shadow_image = pygame.image.load(RESOURCE_PATH / "story" / "story_shadow.png")
        shadow_image = pygame.transform.scale(shadow_image, (shadow_x, shadow_y))
        for i in range(self.story_amount):
            if i > StoryMenu.story_progress:
                screen.blit(shadow_image, 
                            (self.pos_formula(i)[0] - shadow_x / 2,
                            self.pos_formula(i)[1] - shadow_y / 2))

    # 파일에 저장된 진행도 불러오기
    def load_progress(self):
        try:
            with open(self.progress_path, "rb") as f:
                StoryMenu.story_progress = pickle.load(f)

        # 파일이 없을 시 진행도 초기화
        except FileNotFoundError:
            StoryMenu.story_progress = 0

    # 파일에 진행도 저장하기
    def save_progress(self):
        with open(self.progress_path, "wb") as f:
            pickle.dump(StoryMenu.story_progress, f)

    def __init__(self, pos=(0, 0), size=(150, 50)):
        # ############################
        # 높은 단계의 스토리를 테스트를 위해 들어가려면
        # load_progress()를 주석처리한 뒤 story_progress = 0을 높이면 됩니다.
        # ############################
        StoryMenu.story_progress = 0
        self.progress_path = RESOURCE_PATH / "story_progress.ini"
        self.load_progress()

        story_img = lambda s: tuple(
            RESOURCE_PATH / "story" / f"story_{i}.png"
            for i in range(1, s+1))
        
        super().__init__(pos, size, scale=(0.75, 0.75),
                         button_img=story_img(self.story_amount),
                         hovering_img=story_img(self.story_amount))

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)
        # 스토리 다음 버튼 = 돌아가기 버튼
        if index == self.story_amount:
            pygame.event.post(pygame.event.Event(EVENT_MAIN))
            return
        global enter_story
        # 진입 불가 스토리는 확인 창 없이 return
        if index > StoryMenu.story_progress: return
        enter_story = index

    def handle_event(self, event: pygame.event.Event):
        # 스토리 확인 창이 나오는 중에는 스토리 선택은 작동하지 않게 처리
        global enter_story
        if enter_story == -1: super().handle_event(event)


class StoryMap:
    global enter_story

    def __init__(self, pos, size):
        
        self.STORY_MENU = StoryMenu(pos, size)
        self.STORY_CONFIRM = StoryConfirm(pos, size)

    def draw(self, screen):
        self.STORY_MENU.draw(screen)
        if enter_story != -1:
            self.STORY_CONFIRM.draw(screen)

    def handle_event(self, event):
        self.STORY_MENU.handle_event(event)
        self.STORY_CONFIRM.handle_event(event)
    
    def resize(self, size):
        self.STORY_MENU.resize(size)
        self.STORY_CONFIRM.resize(size)