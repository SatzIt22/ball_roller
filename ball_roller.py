import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Roller")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game parameters
BALL_RADIUS = 20
BALL_SPEED = 5
TIMER_DURATION = 60  # seconds
INITIAL_LIVES = 3

class Level:
    def __init__(self, start_pos, goal_pos, obstacles):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.obstacles = obstacles

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
        
    def reset_game(self):
        self.lives = INITIAL_LIVES
        self.score = 0
        self.current_level = 0
        self.create_levels()
        self.reset_level()
        
    def create_levels(self):
        # Create 10 levels with increasing complexity
        self.levels = [
            Level((100, 500), (700, 100), [(300, 400), (500, 200)]),
            Level((50, 550), (750, 50), [(200, 300), (400, 100), (600, 500)]),
            Level((100, 100), (700, 500), [(250, 250), (550, 350), (400, 450)]),
            Level((50, 550), (750, 50), [(100, 300), (300, 100), (500, 400), (700, 200)]),
            Level((400, 550), (400, 50), [(200, 200), (600, 400), (300, 300), (500, 100)]),
            Level((100, 500), (700, 100), [(250, 250), (500, 400), (350, 150), (600, 300)]),
            Level((50, 50), (750, 550), [(200, 400), (400, 200), (600, 300), (300, 500)]),
            Level((400, 550), (400, 50), [(100, 300), (700, 300), (250, 200), (550, 400)]),
            Level((100, 100), (700, 500), [(200, 400), (400, 200), (600, 300), (300, 500), (500, 100)]),
            Level((50, 550), (750, 50), [(100, 100), (300, 500), (500, 200), (700, 400), (200, 300)])
        ]
        
    def reset_level(self):
        level = self.levels[self.current_level]
        self.ball_pos = list(level.start_pos)
        self.timer = TIMER_DURATION * 1000  # convert to milliseconds
        
    def draw_level(self):
        SCREEN.fill(WHITE)
        
        # Draw current level details
        level_text = self.font.render(f"Level {self.current_level + 1}", True, BLACK)
        lives_text = self.font.render(f"Lives: {self.lives}", True, BLACK)
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        timer_text = self.font.render(f"Time: {self.timer // 1000}", True, BLACK)
        
        SCREEN.blit(level_text, (10, 10))
        SCREEN.blit(lives_text, (10, 50))
        SCREEN.blit(score_text, (10, 90))
        SCREEN.blit(timer_text, (10, 130))
        
        # Draw current level
        level = self.levels[self.current_level]
        
        # Draw goal
        pygame.draw.circle(SCREEN, GREEN, level.goal_pos, BALL_RADIUS * 1.5)
        
        # Draw obstacles
        for obstacle in level.obstacles:
            pygame.draw.circle(SCREEN, RED, obstacle, BALL_RADIUS)
        
        # Draw ball
        pygame.draw.circle(SCREEN, BLUE, self.ball_pos, BALL_RADIUS)
        
    def move_ball(self, keys):
        # Ball movement
        if keys[pygame.K_LEFT]:
            self.ball_pos[0] -= BALL_SPEED
        if keys[pygame.K_RIGHT]:
            self.ball_pos[0] += BALL_SPEED
        if keys[pygame.K_UP]:
            self.ball_pos[1] -= BALL_SPEED
        if keys[pygame.K_DOWN]:
            self.ball_pos[1] += BALL_SPEED
        
    def check_collision(self):
        level = self.levels[self.current_level]
        
        # Check goal
        if ((self.ball_pos[0] - level.goal_pos[0])**2 + 
            (self.ball_pos[1] - level.goal_pos[1])**2) <= (BALL_RADIUS * 2.5)**2:
            # Level complete
            self.score += max(0, self.timer // 1000)  # Points based on remaining time
            self.current_level += 1
            
            # Check if all levels completed
            if self.current_level >= len(self.levels):
                self.game_won()
                return
            
            self.reset_level()
            return
        
        # Check obstacles
        for obstacle in level.obstacles:
            if ((self.ball_pos[0] - obstacle[0])**2 + 
                (self.ball_pos[1] - obstacle[1])**2) <= (BALL_RADIUS * 2)**2:
                self.lose_life()
                return
        
        # Check out of bounds
        if (self.ball_pos[0] < 0 or self.ball_pos[0] > SCREEN_WIDTH or 
            self.ball_pos[1] < 0 or self.ball_pos[1] > SCREEN_HEIGHT):
            self.lose_life()
    
    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over()
        else:
            self.reset_level()
    
    def game_over(self):
        while True:
            SCREEN.fill(WHITE)
            game_over_text = self.font.render("Game Over!", True, RED)
            score_text = self.font.render(f"Final Score: {self.score}", True, BLACK)
            retry_text = self.font.render("Press R to Retry", True, BLACK)
            quit_text = self.font.render("Press Q to Quit", True, BLACK)
            
            SCREEN.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 100))
            SCREEN.blit(score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
            SCREEN.blit(retry_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            SCREEN.blit(quit_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
    
    def game_won(self):
        while True:
            SCREEN.fill(WHITE)
            win_text = self.font.render("Congratulations! You Won!", True, GREEN)
            score_text = self.font.render(f"Final Score: {self.score}", True, BLACK)
            retry_text = self.font.render("Press R to Play Again", True, BLACK)
            quit_text = self.font.render("Press Q to Quit", True, BLACK)
            
            SCREEN.blit(win_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100))
            SCREEN.blit(score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
            SCREEN.blit(retry_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            SCREEN.blit(quit_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
    
    def run(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Get pressed keys
            keys = pygame.key.get_pressed()
            
            # Move ball
            self.move_ball(keys)
            
            # Check collisions
            self.check_collision()
            
            # Update timer
            self.timer -= self.clock.get_time()
            if self.timer <= 0:
                self.lose_life()
            
            # Draw everything
            self.draw_level()
            
            # Update display
            pygame.display.flip()
            
            # Control game speed
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
