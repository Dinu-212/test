import pygame
import random
import sys
import asyncio

pygame.init()

# Screen setup
screen_width = 500
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Dodge Game")

# Load car image
car = pygame.image.load("car.png")
obj = pygame.image.load("car.png")

# Font
font = pygame.font.Font(None, 36)

# Menu options
options = ["Start", "Quit"]
selected_option = 0

def draw_menu(selected_option):
    screen.fill("WHITE")
    title_text = font.render("Welcome to the Game!", True, "BLACK")
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 150))

    for i, option in enumerate(options):
        color = "GREEN" if i == selected_option else "BLACK"
        text = font.render(option, True, color)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 300 + i * 60))

    pygame.display.flip()

def start_menu():
    global selected_option
    running = True
    while running:
        draw_menu(selected_option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        running = False
                    elif selected_option == 1:
                        pygame.quit()
                        sys.exit()

def draw_fireworks(fireworks):
    for i, (x, y, color) in enumerate(fireworks):
        pygame.draw.rect(screen, color, (x, y, 2, 2))
        y -= 2
        if y < 0:
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
        fireworks[i] = (x, y, color)

async def main():
    start_menu()

    # Initial positions
    car_x = screen_width // 2 - car.get_width() // 2
    car_y = screen_height - car.get_height()

    obj_x = random.randint(0, screen_width - obj.get_width())
    obj_y = 0

    score = 0
    speed = 2
    car_speed = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < screen_width - car.get_width():
            car_x += car_speed

        obj_y += speed
        if obj_y > screen_height:
            obj_y = 0
            obj_x = random.randint(0, screen_width - obj.get_width())
            score += 1
            if score % 5 == 0:
                speed += 0.5

        screen.fill("BLACK")
        for i in range(0, screen_height, 100):
            pygame.draw.line(screen, "WHITE", (screen_width // 2, i), (screen_width // 2, i + 50), 10)

        screen.blit(obj, (obj_x, obj_y))
        screen.blit(car, (car_x, car_y))

        score_text = font.render(f"Score: {score}", True, "WHITE")
        screen.blit(score_text, (10, 10))

        car_rect = pygame.Rect(car_x, car_y, car.get_width(), car.get_height())
        obj_rect = pygame.Rect(obj_x, obj_y, obj.get_width(), obj.get_height())

        if car_rect.colliderect(obj_rect):
            await end_menu(score)
            running = False

        pygame.display.flip()
        await asyncio.sleep(0)

async def end_menu(score):
    # Setup fireworks
    fireworks = [
        (random.randint(0, screen_width), random.randint(0, screen_height),
         (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        for _ in range(100)
    ]
    timer = pygame.time.get_ticks()
    show_time = 5000  # milliseconds

    running = True
    while running:
        screen.fill("WHITE")
        title = font.render("Thanks for playing the game!!!", True, "BLACK")
        final_score = font.render(f"Final Score: {score}", True, "BLACK")
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 150))
        screen.blit(final_score, (screen_width // 2 - final_score.get_width() // 2, 400))

        draw_fireworks(fireworks)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.time.get_ticks() - timer > show_time:
            running = False

        await asyncio.sleep(0)

asyncio.run(main())
