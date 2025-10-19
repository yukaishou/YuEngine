import pygame
import sys

# 初始化Pygame
pygame.init()

# 窗口设置
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("lobby")

# 颜色定义
COLORS = {
    "background": (18, 18, 18),
    "primary": (255, 204, 0),
    "secondary": (45, 45, 45),
    "text": (240, 240, 240),
    "highlight": (255, 100, 0)
}

# 字体加载
font_title = pygame.font.Font("D:\YuEngine\Resource/font\Mojangles.ttf", 36)
font_normal = pygame.font.Font("D:\YuEngine\Resource/font\Mojangles.ttf", 18)
snd = pygame.mixer.Sound("D:\YuEngine\Resource\sound\Looby_B.mp3")
snd.play()
class TacticalButton:
    """战术风格按钮组件"""
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hover = False
        self.clicked = False

    def draw(self, surface):
        # 按钮渐变效果
        if self.hover:
            pygame.draw.rect(surface, COLORS["highlight"], self.rect, border_radius=4)
            pygame.draw.rect(surface, COLORS["primary"], self.rect.inflate(-4, -4), border_radius=4)
        else:
            pygame.draw.rect(surface, COLORS["secondary"], self.rect, border_radius=4)

        # 文字渲染
        text_surf = font_normal.render(self.text, True, COLORS["text"])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                self.callback()

def draw_status_bar(surface):
    """顶部状态栏"""
    status_bg = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
    pygame.draw.rect(surface, COLORS["secondary"], status_bg)

    # 玩家信息
    avatar = pygame.image.load("Resource/image/Logo.png").convert_alpha()
    surface.blit(avatar, (20, 5))

    # 资源显示
    resources = [
        ("$ 23500", "D:\YuEngine\Resource\image\editor\Bar\Play.png"),
        ("♦ 150", "D:\YuEngine\Resource\image\editor\Bar/rotation.png"),
        ("⚡ 3/5", "D:\YuEngine\Resource\image\editor\Bar\Scall.png")
    ]

    x_pos = SCREEN_WIDTH - 400
    for text, icon in resources:
        img = pygame.image.load(icon).convert_alpha()
        surface.blit(img, (x_pos, 10))
        text_surf = font_normal.render(text, True, COLORS["text"])
        surface.blit(text_surf, (x_pos + 40, 15))
        x_pos += 150

def main_menu():
    # 游戏主循环
    running = True

    # 创建按钮
    buttons = [
        TacticalButton(100, 150, 200, 50, "Start Game", lambda: print("进入匹配系统")),
        TacticalButton(100, 220, 200, 50, "Open Editor", lambda: print("打开装备界面")),
        TacticalButton(100, 290, 200, 50, "Task panel", lambda: print("打开任务面板"))
    ]

    while running:
        screen.fill(COLORS["background"])

        # 绘制状态栏
        draw_status_bar(screen)

        # 绘制3D角色预览（需要3D库支持或使用预渲染图片）
        #character_preview = pygame.image.load("assets/character_showcase.png")
        #screen.blit(character_preview, (SCREEN_WIDTH-450, 100))

        # 处理按钮
        for button in buttons:
            button.draw(screen)

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            for button in buttons:
                button.handle_event(event)

        pygame.display.update()

if __name__ == "__main__":
    main_menu()

