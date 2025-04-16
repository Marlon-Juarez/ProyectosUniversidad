import pygame
import time

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("T-Intersection Traffic Light Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

class TrafficLight:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.state = "red"
        self.timer = 0
        
    def draw(self, screen):
        # Draw traffic light housing
        pygame.draw.rect(screen, GRAY, (self.x, self.y, 60, 160))
        
        # Draw lights
        colors = [RED, YELLOW, GREEN]
        active_colors = [GRAY, GRAY, GRAY]
        
        if self.state == "red":
            active_colors[0] = RED
        elif self.state == "yellow":
            active_colors[1] = YELLOW
        elif self.state == "green":
            active_colors[2] = GREEN
            
        for i, color in enumerate(active_colors):
            pygame.draw.circle(screen, color, (self.x + 30, self.y + 30 + i * 50), 20)
            
        # Draw label
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, WHITE)
        screen.blit(text, (self.x - 10, self.y + 170))

class PetriNetSimulation:
    def __init__(self):
        self.main_light = TrafficLight(200, 200, "Main Road")
        self.secondary_light = TrafficLight(500, 200, "Secondary Road")
        self.cycle_time = {"red": 5, "yellow": 2, "green": 4}
        self.state_sequence = ["red", "green", "yellow"]
        
    def update(self):
        current_time = time.time()
        
        # Update main light
        if current_time - self.main_light.timer >= self.cycle_time[self.main_light.state]:
            self.main_light.timer = current_time
            current_index = self.state_sequence.index(self.main_light.state)
            self.main_light.state = self.state_sequence[(current_index + 1) % len(self.state_sequence)]
            
            # If main light turns red, start secondary light's cycle
            if self.main_light.state == "red":
                self.secondary_light.timer = current_time
                self.secondary_light.state = "green"
        
        # Update secondary light
        if self.secondary_light.state != "red":
            if current_time - self.secondary_light.timer >= self.cycle_time[self.secondary_light.state]:
                self.secondary_light.timer = current_time
                current_index = self.state_sequence.index(self.secondary_light.state)
                self.secondary_light.state = self.state_sequence[(current_index + 1) % len(self.state_sequence)]
    
    def draw(self, screen):
        # Draw background
        screen.fill(BLACK)
        
        # Draw road
        pygame.draw.rect(screen, GRAY, (0, 280, WIDTH, 40))  # Horizontal road
        pygame.draw.rect(screen, GRAY, (480, 0, 40, HEIGHT))  # Vertical road
        
        # Draw traffic lights
        self.main_light.draw(screen)
        self.secondary_light.draw(screen)
        
        # Draw state information
        font = pygame.font.Font(None, 36)
        main_text = font.render(f"Main: {self.main_light.state}", True, WHITE)
        secondary_text = font.render(f"Secondary: {self.secondary_light.state}", True, WHITE)
        screen.blit(main_text, (50, 50))
        screen.blit(secondary_text, (50, 100))

def main():
    clock = pygame.time.Clock()
    simulation = PetriNetSimulation()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        simulation.update()
        simulation.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main()
