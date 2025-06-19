import time
import math
import random
import pygame


pygame.init()
items=['diamond', 'iron', 'gold', 'stick', 'apple', 'bread','bone',
       'emerald', 'leather', 'coal', 'arrow', 'ender_pearl']
Width,Height = 800,600
icons = {}

for i in items:
    icon = pygame.image.load(f'icons/{i}.png')
    icon = pygame.transform.scale(icon, (40, 40))
    icons[i]=icon
    
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
Win = pygame.display.set_mode((Width,Height))



class Slots:
    WidthS, HeightS = 50, 50
    def __init__(self, x, y, item= None):
        self.rect = pygame.Rect(x, y, self.WidthS, self.HeightS)
        self.item = item
        self.looted = False
    def draw(self, Win):
        pygame.draw.rect(Win, (200, 200, 200), self.rect)
        pygame.draw.rect(Win, (100, 100, 100), self.rect, 2)

        if self.item and not self.looted:
            icon = icons.get(self.item)
            if icon:
                icon_rect = icon.get_rect(center = self.rect.center)
                Win.blit(icon, icon_rect)
        
    def loot(self):
        if self.item and not self.looted:
            self.looted = True
            return True
        return False
    


def AimTrainer():
    
    run = True

    slots=[]
    Rows = 3
    Cols = 9
    Space = 5
    slot_w, slot_h = Slots.WidthS, Slots.HeightS
    total_width = Cols * slot_w + (Cols - 1) * Space
    total_height = Rows * slot_h + (Rows - 1) * Space

    X_Initial = (Width - total_width) // 2
    Y_Initial = (Height - total_height) // 2
    
    for i in range(Rows):
        for j in range(Cols):
            x = X_Initial + j*(Slots.WidthS + Space)
            y = Y_Initial + i*(Slots.HeightS + Space)
            item=None
            if random.random()<0.5:
                item = random.choice(items)
            slots.append(Slots(x, y, item))
            
    game_over = False
    start = time.time()
    correct_clicks = 0
    total_clicks = 0

    while run:
        Win.fill((50, 50, 50))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                total_clicks += 1
                pos = pygame.mouse.get_pos()
                for slot in slots:
                    if slot.rect.collidepoint(pos):
                        if slot.loot():
                            correct_clicks += 1
                        break

        for slot in slots:
            slot.draw(Win)

        if not game_over:
            time_passed = time.time() - start
        else:
            time_passed = final_time

        accuracy = (correct_clicks / total_clicks) * 100 if total_clicks > 0 else 0

        score_text = font.render(f'Correct: {correct_clicks} / Total: {total_clicks}', True, (255, 255, 255))
        accuracy_text = font.render(f'Accuracy: {accuracy:.2f}%', True, (255, 255, 255))
        time_text = font.render(f'Time: {time_passed:.2f}s', True, (255, 255, 255))
        Win.blit(score_text, (20, 20))
        Win.blit(accuracy_text, (20, 50))
        Win.blit(time_text, (20, 80))

        if all(slot.looted or slot.item is None for slot in slots):
            if not game_over:
                game_over = True
                final_time = time_passed
            

        pygame.display.update()
                            
    pygame.quit()

if __name__ == "__main__":
    AimTrainer()
            
                
