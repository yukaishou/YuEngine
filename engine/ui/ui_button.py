import pygame

pygame.font.init()

font_normal = pygame.font.Font("../YuEngine\Resource/font\simhei.ttf", 24)

COLORS = {
    "background": (18, 18, 18),
    "primary": (255, 204, 0),
    "secondary": (45, 45, 45),
    "text": (240, 240, 240),
    "highlight": (255, 100, 0)
}
class Button:
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