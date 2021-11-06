import pygame
import random

pygame.init()

dis_width = 800
dis_height = 600
score_row_height = 50

x_center = dis_width / 2
y_center = dis_height / 2

white = (255, 255, 255)
gray = (128, 128, 128)
black = (0, 0, 0)
red = (213, 50, 80)
blue = (0, 0, 255)

dis = pygame.display.set_mode((dis_width, dis_height + score_row_height))

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10

game_msg_font = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("bahnschrift", 25)


class Snake:
    def __init__(self, snake_color=black, score=0, length=1, snake_list=None, snake_head=None, speed=snake_speed*10):
        if snake_head is None:
            snake_head = [x_center, y_center]
        if snake_list is None:
            snake_list = []
        self.snake_color = snake_color
        self.score = score
        self.length = length
        self.snake_list = snake_list
        self.snake_head = snake_head
        self.speed = speed

    # def get_attribute(self, attr):
    #     if attr == "speed":
    #         return self.speed
    #     elif attr == "score":
    #         return self.score
    #     elif attr == "length":
    #         return self.score

    def draw_snake(self, snake_location=snake_block):
        for x in self.snake_list:
            pygame.draw.rect(dis, self.snake_color, [x[0], x[1], snake_location, snake_location])

    def print_scoreboard(self):
        pygame.draw.rect(dis, gray, (0, dis_height, dis_width, score_row_height))
        value = score_font.render("Score: " + str(self.score), True, blue)
        return dis.blit(value, [10, dis_height + score_row_height / 4])


def print_menu(text_lines=None, i=1):
    """
    text_lines - menu optiona to print\n
    i - active menu selection; set to 1 by default
    """
    # pygame.draw.rect(dis, gray, (dis_width/10, dis_height/10, dis_width*0.8, score_row_height*0.8))
    if text_lines is None:
        text_lines = []
    for j, c in enumerate(text_lines):
        l_color = red if i == j else black
        item = game_msg_font.render(c, True, l_color)
        dis.blit(item, [dis_height / 10, (j + 2) * 30])


def message(msg, color):
    dis.blit(game_msg_font.render(msg, True, color), [50, dis_height / 3])


def game_loop():
    game_close = False

    x1_change = 0
    y1_change = 0

    x1 = x_center
    y1 = y_center

    player1 = Snake()

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_close:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        player1.snake_list.append(snake_head)
        if len(player1.snake_list) > player1.length:
            del player1.snake_list[0]

        for x in player1.snake_list[:-1]:
            if x == snake_head:
                game_close = True

        player1.draw_snake(snake_block)
        player1.print_scoreboard()

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            player1.length += 1

        clock.tick(snake_speed)

    main()


def main():
    play_game = True
    menu_text = [
        "Start normal game",
        "Start incremental game",
        "Highscores",
        "Settings",
        "Quit"]
    menu_opt_count = len(menu_text) - 1
    i = 0

    dis.fill(gray)
    print_menu(text_lines=menu_text, i=i)
    pygame.display.update()

    while play_game:
        for selection in pygame.event.get():
            if selection.type == pygame.KEYDOWN:
                if selection.key == pygame.K_q:
                    print("Quit")
                    play_game = False
                elif selection.key == pygame.K_UP:
                    i = i - 1 if i > 0 else menu_opt_count
                    print_menu(text_lines=menu_text, i=i)
                    pygame.display.update()
                elif selection.key == pygame.K_DOWN:
                    i = i + 1 if i < menu_opt_count else 0
                    print_menu(text_lines=menu_text, i=i)
                    pygame.display.update()
                elif selection.key == pygame.K_RETURN:
                    if menu_text[i] == "Start normal game":
                        game_loop()
                    elif menu_text[i] == 1:
                        print("1 - TODO")
                    elif menu_text[i] == 2:
                        print("2 - TODO")
                    elif menu_text[i] == 3:
                        print("3 - TODO")
                    elif menu_text[i] == "Quit":
                        play_game = False

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
