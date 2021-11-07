import pygame
import random
import json
from datetime import date
from operator import itemgetter

pygame.init()

white = (255, 255, 255)
grey = (128, 128, 128)
black = (0, 0, 0)
red = (213, 50, 80)
orange = (255, 215, 0)
blue = (0, 0, 255)

with open('cfg/settings.json') as f:
    config = json.load(f)

snake_speed = config.get("speed")
dis_width = config.get("display_width")
dis_height = config.get("display_height")
score_row_height = config.get("score_height")
snake_block = config.get("snake_block")

x_center = dis_width / 2
y_center = dis_height / 2

dis = pygame.display.set_mode((dis_width, dis_height + score_row_height))

clock = pygame.time.Clock()

game_msg_font = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("bahnschrift", 30)


class Snake:
    def __init__(self, snake_color=black, score=0, length=1, snake_list=None, snake_head=None, speed=snake_speed * 10,
                 score_modifier=1):
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
        self.score_modifier = score_modifier

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
        pygame.draw.rect(dis, grey, (0, dis_height, dis_width, score_row_height))
        value = score_font.render("Score: " + str(self.score), True, blue)
        return dis.blit(value, [10, dis_height + score_row_height / 4])


def print_menu(text_lines=None, s=0, i=1, new_highscore=False):
    """
    text_lines - menu optiona to print\n
    i - active menu selection; set to 1 by default
    s - score to display as message
    """
    # pygame.draw.rect(dis, gray, (dis_width/10, dis_height/10, dis_width*0.8, score_row_height*0.8))
    dis.fill(grey)
    if text_lines is None:
        text_lines = []

    if s != 0 and new_highscore is True:
        item = game_msg_font.render("New high score: " + str(s), True, orange)
        text_width = item.get_width()
        dis.blit(item, [dis_width - text_width - dis_width/10, dis_height / 20])
    if s != 0 and new_highscore is False:
        item = game_msg_font.render("Last score: " + str(s), True, blue)
        text_width = item.get_width()
        dis.blit(item, [dis_width - text_width - dis_width/10, dis_height / 20])

    for j, c in enumerate(text_lines):
        l_color = red if i == j else black
        item = game_msg_font.render(c, True, l_color)
        dis.blit(item, [dis_height / 10, (j + 3) * dis_height / 20])


def print_highscore():
    dis.fill(grey)
    with open('cfg/scores.json') as score_file:
        scores = json.load(score_file)
    for j, c in enumerate(scores):
        # l_color = red if i == j else black
        item = game_msg_font.render(str(j + 1) + ".    " + str(scores[j][0]) + " - " + scores[j][1], True, black)
        dis.blit(item, [dis_height / 10, (j + 4) * 30])
    pygame.display.update()


def save_highscore(new_score, score_date):
    with open('cfg/scores.json') as score_file:
        h_scores = json.load(score_file)
    h_scores.append([new_score, score_date])
    h_scores = sorted(h_scores, key=itemgetter(0), reverse=True)
    h_scores.remove(h_scores[-1])

    with open('cfg/scores.json', 'w') as output:
        output.write(json.dumps(h_scores))

    return True if h_scores.__contains__([new_score, score_date]) else False


def game_loop():
    game_close = False

    x1_change = 0
    y1_change = 0

    x1 = x_center
    y1 = y_center

    player1 = Snake()

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    locked_key = 0

    while not game_close:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not locked_key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                    locked_key = pygame.K_RIGHT
                elif event.key == pygame.K_RIGHT and not locked_key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                    locked_key = pygame.K_LEFT
                elif event.key == pygame.K_UP and not locked_key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                    locked_key = pygame.K_DOWN
                elif event.key == pygame.K_DOWN and not locked_key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                    locked_key = pygame.K_UP

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
            player1.score += 1 * player1.score_modifier

        clock.tick(snake_speed)
    new_hs = save_highscore(player1.score, str(date.today()))
    main(last_score=player1.score, new_highscore=new_hs)


def main(last_score=0, new_highscore=False):
    play_game = True
    menu_text = [
        "Start normal game",
        "Start incremental game",
        "High scores",
        "Quit"]
    menu_opt_count = len(menu_text) - 1
    i = 0

    dis.fill(grey)
    print_menu(text_lines=menu_text, i=i, s=last_score, new_highscore=new_highscore)
    pygame.display.update()

    while play_game:
        for selection in pygame.event.get():
            if selection.type == pygame.KEYDOWN:
                if selection.key == pygame.K_q:
                    print("Quit")
                    play_game = False
                elif selection.key == pygame.K_UP:
                    i = i - 1 if i > 0 else menu_opt_count
                    print_menu(text_lines=menu_text, s=last_score, i=i, new_highscore=new_highscore)
                    pygame.display.update()
                elif selection.key == pygame.K_DOWN:
                    i = i + 1 if i < menu_opt_count else 0
                    print_menu(text_lines=menu_text, s=last_score, i=i, new_highscore=new_highscore)
                    pygame.display.update()
                elif selection.key == pygame.K_RETURN:
                    if menu_text[i] == "Start normal game":
                        game_loop()
                    elif menu_text[i] == "High scores":
                        print_highscore()
                    elif menu_text[i] == "Start incremental game":
                        print("2 - TODO")
                    # elif menu_text[i] == "Settings":
                    #     settings()
                    elif menu_text[i] == "Quit":
                        play_game = False

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
