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
YELLOW = (255, 255, 0)  # Color for collectibles
PURPLE = (128, 0, 128)  # Color for moving obstacles

# Game parameters
BALL_RADIUS = 20
BALL_SPEED = 5
TIMER_DURATION = 60  # seconds
INITIAL_LIVES = 3
COLLECTIBLE_RADIUS = 10
COLLECTIBLES_FOR_EXTRA_LIFE = 10

class MovingObstacle:
    def __init__(self, start_pos, end_pos, speed):
        self.start_pos = list(start_pos)
        self.end_pos = list(end_pos)
        self.current_pos = list(start_pos)
        self.speed = speed
        self.moving_to_end = True
        
    def update(self):
        if self.moving_to_end:
            target = self.end_pos
        else:
            target = self.start_pos
            
        dx = target[0] - self.current_pos[0]
        dy = target[1] - self.current_pos[1]
        distance = (dx**2 + dy**2)**0.5
        
        if distance < self.speed:
            self.moving_to_end = not self.moving_to_end
        else:
            move_x = (dx / distance) * self.speed
            move_y = (dy / distance) * self.speed
            self.current_pos[0] += move_x
            self.current_pos[1] += move_y

class Level:
    def __init__(self, start_pos, goal_pos, obstacles, moving_obstacles, collectibles, platforms=None):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.obstacles = obstacles
        self.moving_obstacles = moving_obstacles
        self.collectibles = list(collectibles)  # Make a copy so we can remove collected ones
        self.platforms = platforms or []  # Platforms to walk on (for more distinct levels)

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.collectibles_count = 0
        self.reset_game()
        
    def reset_game(self):
        self.lives = INITIAL_LIVES
        self.score = 0
        self.current_level = 0
        self.collectibles_count = 0
        self.create_levels()
        self.reset_level()
        
    def create_levels(self):
        # Create 10 distinct levels with unique challenges
        self.levels = [
            # Level 1: Simple introduction
            Level(
                (100, 500), (700, 100),
                [(300, 400)],
                [],  # No moving obstacles
                [(200, 300), (400, 300), (600, 300)],  # Few collectibles
                [(0, 550, 800, 50)]  # Ground platform
            ),
            
            # Level 2: Moving obstacles introduction
            Level(
                (50, 550), (750, 50),
                [],
                [MovingObstacle((200, 200), (200, 400), 3)],
                [(300, 100), (400, 100), (500, 100)],
                [(0, 550, 800, 50)]
            ),
            
            # Level 3: Zigzag path with collectibles
            Level(
                (50, 550), (750, 50),
                [(200, 300), (400, 200), (600, 300)],
                [MovingObstacle((300, 100), (300, 500), 4)],
                [(150, 400), (250, 300), (350, 200), (450, 100)],
                [(0, 550, 800, 50), (200, 400, 200, 20), (400, 300, 200, 20)]
            ),
            
            # Level 4: Moving obstacle maze
            Level(
                (50, 550), (750, 50),
                [(400, 300)],
                [
                    MovingObstacle((200, 100), (200, 500), 5),
                    MovingObstacle((400, 100), (400, 500), 5),
                    MovingObstacle((600, 100), (600, 500), 5)
                ],
                [(100, 300), (300, 300), (500, 300), (700, 300)],
                [(0, 550, 800, 50)]
            ),
            
            # Level 5: Vertical challenge
            Level(
                (400, 550), (400, 50),
                [],
                [
                    MovingObstacle((100, 300), (700, 300), 6),
                    MovingObstacle((700, 200), (100, 200), 6)
                ],
                [(400, 450), (400, 350), (400, 250), (400, 150)],
                [(0, 550, 800, 50), (100, 400, 600, 20), (200, 250, 400, 20)]
            ),
            
            # Level 6: Diagonal challenge
            Level(
                (50, 550), (750, 50),
                [(300, 300), (500, 300)],
                [
                    MovingObstacle((200, 200), (600, 400), 4),
                    MovingObstacle((600, 200), (200, 400), 4)
                ],
                [(150, 450), (300, 350), (450, 250), (600, 150)],
                [(0, 550, 800, 50), (100, 450, 200, 20), (500, 250, 200, 20)]
            ),
            
            # Level 7: Circular motion
            Level(
                (400, 500), (400, 100),
                [],
                [
                    MovingObstacle((300, 200), (500, 200), 3),
                    MovingObstacle((500, 200), (500, 400), 3),
                    MovingObstacle((500, 400), (300, 400), 3),
                    MovingObstacle((300, 400), (300, 200), 3)
                ],
                [(400, 300), (350, 250), (450, 250), (400, 350)],
                [(0, 550, 800, 50)]
            ),
            
            # Level 8: Speed challenge
            Level(
                (50, 550), (750, 50),
                [(200, 300), (600, 300)],
                [
                    MovingObstacle((300, 100), (300, 500), 7),
                    MovingObstacle((500, 500), (500, 100), 7)
                ],
                [(200, 200), (400, 200), (600, 200), (200, 400), (400, 400), (600, 400)],
                [(0, 550, 800, 50)]
            ),
            
            # Level 9: Complex pattern
            Level(
                (50, 550), (750, 50),
                [(400, 300)],
                [
                    MovingObstacle((200, 200), (600, 200), 5),
                    MovingObstacle((600, 200), (600, 400), 5),
                    MovingObstacle((600, 400), (200, 400), 5),
                    MovingObstacle((200, 400), (200, 200), 5)
                ],
                [(300, 150), (500, 150), (300, 450), (500, 450), (150, 300), (650, 300)],
                [(0, 550, 800, 50), (200, 300, 400, 20)]
            ),
            
            # Level 10: Final challenge
            Level(
                (400, 550), (400, 50),
                [(200, 300), (600, 300)],
                [
                    MovingObstacle((100, 200), (700, 200), 6),
                    MovingObstacle((700, 400), (100, 400), 6),
                    MovingObstacle((300, 100), (300, 500), 5),
                    MovingObstacle((500, 500), (500, 100), 5)
                ],
                [(200, 150), (400, 150), (600, 150), (200, 450), (400, 450), (600, 450)],
                [(0, 550, 800, 50), (100, 350, 250, 20), (450, 250, 250, 20)]
            )
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
        collectibles_text = self.font.render(f"Collectibles: {self.collectibles_count}", True, BLACK)
        
        SCREEN.blit(level_text, (10, 10))
        SCREEN.blit(lives_text, (10, 50))
        SCREEN.blit(score_text, (10, 90))
        SCREEN.blit(timer_text, (10, 130))
        SCREEN.blit(collectibles_text, (10, 170))
        
        level = self.levels[self.current_level]
        
        # Draw platforms
        for platform in level.platforms:
            pygame.draw.rect(SCREEN, BLACK, platform)
        
        # Draw goal
        pygame.draw.circle(SCREEN, GREEN, level.goal_pos, BALL_RADIUS * 1.5)
        
        # Draw static obstacles
        for obstacle in level.obstacles:
            pygame.draw.circle(SCREEN, RED, obstacle, BALL_RADIUS)
            
        # Draw moving obstacles
        for obstacle in level.moving_obstacles:
            pygame.draw.circle(SCREEN, PURPLE, [int(obstacle.current_pos[0]), int(obstacle.current_pos[1])], BALL_RADIUS)
            
        # Draw collectibles
        for collectible in level.collectibles:
            pygame.draw.circle(SCREEN, YELLOW, collectible, COLLECTIBLE_RADIUS)
        
        # Draw ball
        pygame.draw.circle(SCREEN, BLUE, [int(self.ball_pos[0]), int(self.ball_pos[1])], BALL_RADIUS)

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
        
        # Check static obstacles
        for obstacle in level.obstacles:
            if ((self.ball_pos[0] - obstacle[0])**2 + 
                (self.ball_pos[1] - obstacle[1])**2) <= (BALL_RADIUS * 2)**2:
                self.lose_life()
                return
                
        # Check moving obstacles
        for obstacle in level.moving_obstacles:
            if ((self.ball_pos[0] - obstacle.current_pos[0])**2 + 
                (self.ball_pos[1] - obstacle.current_pos[1])**2) <= (BALL_RADIUS * 2)**2:
                self.lose_life()
                return
                
        # Check collectibles
        for collectible in level.collectibles[:]:  # Use slice copy to modify during iteration
            if ((self.ball_pos[0] - collectible[0])**2 + 
                (self.ball_pos[1] - collectible[1])**2) <= (BALL_RADIUS + COLLECTIBLE_RADIUS)**2:
                level.collectibles.remove(collectible)
                self.score += 100  # Points for collecting
                self.collectibles_count += 1
                if self.collectibles_count >= COLLECTIBLES_FOR_EXTRA_LIFE:
                    self.lives += 1
                    self.collectibles_count = 0
        
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
            
            # Update moving obstacles
            for obstacle in self.levels[self.current_level].moving_obstacles:
                obstacle.update()
            
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
