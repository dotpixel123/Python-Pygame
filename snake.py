import pygame
import random

pygame.init()

width, height = 750, 600
win = pygame.display.set_mode((width, height))
fps = 75

bg = pygame.image.load("Assets\\bg.jpg")
bg2 = pygame.image.load("Assets\\top.jpg")
bigbg = pygame.transform.scale(bg, (width, height - 100))
bigbg2 = pygame.transform.scale(bg2, (width, 103))

snake_height = snake_width = 30
snake_vel = 3

colors = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "darkgreen": (50, 100, 50),
    "fruit": (230, 40, 0),
    "snake": (0, 200, 0),
    "snake_head": (0, 155, 30)
}


def snake_movement(snake, gameover, key):
    if key == 'up':
        if snake.y > 155:
            snake.y -= snake_vel
        else:
            gameover.append(True)

    elif key == 'down':
        if snake.y < height - snake_height - 45:
            snake.y += snake_vel
        else:
            gameover.append(True)

    elif key == 'right':
        if snake.x < width - snake_width - 20:
            snake.x += snake_vel
        else:
            gameover.append(True)

    elif key == 'left':
        if snake.x > 15:
            snake.x -= snake_vel
        else:
            gameover.append(True)


def fruit_placement(snake, score, fruitpos):
    fruit = fruitpos[-1]

    if (snake.x - snake_width < fruit.x < snake.x + snake_width and
            snake.y - snake_height < fruit.y < snake.y + snake_height):

        new_fruit = pygame.Rect(
            random.randint(20, width - snake_width - 25),
            random.randint(155, height - snake_height - 40),
            snake_height, snake_width
        )
        fruitpos.append(new_fruit)
        score.append(score[-1] + 1)

    pygame.draw.rect(win, colors["fruit"], fruitpos[-1])


def snake_body_movement(gameover, pos, fruit, bodypos):
    if not pos:
        return

    if not gameover[-1]:
        for i in range(1, len(fruit)):
            x, y = pos[-(11 * i)]
            snake_x, snake_y = pos[-1]

            pygame.draw.rect(win, colors["snake"],
                             pygame.Rect(x, y, snake_height, snake_width))
            bodypos.append((x, y))

            if i > 1:
                for j in range(2, 11 * i):
                    if (snake_x, snake_y) == pos[-j]:
                        gameover.append(True)
                        break
    else:
        for i in range(1, len(fruit)):
            x, y = pos[-(11 * i)]
            pygame.draw.rect(win, colors["snake"],
                             pygame.Rect(x, y, snake_height, snake_width))


def title_score(font, titlefont, score, highscore):
    win.blit(font.render(f'Score : {score[-1]}', True, colors["darkgreen"]), (600, 60))
    win.blit(font.render(f'High Score : {highscore}', True, colors["darkgreen"]), (50, 60))
    win.blit(titlefont.render('SNAKE', True, colors["darkgreen"]), (320, 50))

    if score[-1] > int(highscore):
        with open("Highscore.txt", 'w') as file:
            file.write(str(score[-1]))


def over_screen(font, font2, snake):
    win.blit(font.render('GAME OVER', True, colors["darkgreen"]),
             (width / 2 - 150, height / 2 - 80))
    win.blit(font2.render('Press enter to play again!', True, colors["darkgreen"]),
             (width / 2 - 100, height / 2))
    pygame.draw.rect(win, colors["red"], snake)


with open("Highscore.txt", 'r') as file:
    high_score = file.read()


def main_loop():
    snake = pygame.Rect(width // 2 - 20, height // 2 + 30, snake_height, snake_width)
    fruit = pygame.Rect(random.randint(20, width - snake_width - 25),
                        random.randint(155, height - snake_height - 40),
                        snake_height, snake_width)

    fruit_pos = [fruit]
    snake_pos = []
    body_pos = []
    key = None
    score = [0]
    game_over = [False]

    font = pygame.font.SysFont('arial', 25)
    title_font = pygame.font.SysFont('arial', 40, True, True)
    gameover_font = pygame.font.SysFont('arial', 60, True)
    rerun_font = pygame.font.SysFont('arial', 20, False, True)

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and key not in ['up', 'down']:
                    key = 'up'
                elif event.key == pygame.K_DOWN and key not in ['up', 'down']:
                    key = 'down'
                elif event.key == pygame.K_RIGHT and key not in ['left', 'right']:
                    key = 'right'
                elif event.key == pygame.K_LEFT and key not in ['left', 'right']:
                    key = 'left'
                elif event.key == pygame.K_RETURN:
                    key = 'enter'

        win.blit(bigbg, (0, 100))
        win.blit(bigbg2, (0, 0))

        pygame.draw.rect(win, colors["snake_head"], snake)

        fruit_placement(snake, score, fruit_pos)
        snake_body_movement(game_over, snake_pos, fruit_pos, body_pos)

        if not game_over[-1]:
            snake_pos.append((snake.x, snake.y))
            snake_movement(snake, game_over, key)
        else:
            over_screen(gameover_font, rerun_font, snake)

            if key == 'enter':
                game_over[:] = [False]
                snake_pos.clear()
                fruit_pos[:] = [fruit]
                body_pos.clear()
                score[:] = [0]
                snake = pygame.Rect(width // 2 - 20, height // 2 + 30,
                                    snake_height, snake_width)

        title_score(font, title_font, score, high_score)
        pygame.display.update()

    pygame.quit()


main_loop()