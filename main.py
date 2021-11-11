import pygame
import random
import json
from datetime import date
from operator import itemgetter

display = None


class LoadConfig:
    def __init__(self):
        with open('cfg/settings.json') as f:
            config = json.load(f)
        self.dis_width = config.get("display_width")
        self.dis_height = config.get("display_height")
        self.score_row_height = config.get("score_height")
        self.snake_block = config.get("snake_block")
        self.speed = config.get("speed")

    white = (255, 255, 255)
    grey = (150, 150, 150)
    black = (0, 0, 0)
    red = (213, 50, 80)
    orange = (255, 215, 0)
    blue = (0, 0, 255)
    dark_green = (0, 100, 0)


class Snake:
    def __init__(self, snake_color=LoadConfig.dark_green, score=0, length=1, snake_list=None, snake_head=None,
                 speed=0, incremental_game=False, last_increase=0):
        if snake_list is None:
            snake_list = []
        self.snake_color = snake_color
        self.score = score
        self.length = length
        self.snake_list = snake_list
        self.snake_head = snake_head
        self.speed = speed
        self.score_modifier = speed
        self.last_increase = last_increase
        self.incremental_game = incremental_game

    def set_speed(self, diff=1):
        """
        alter snake speed and adjust modifier (self)
        """
        self.speed += diff
        if diff > 0:
            self.score_modifier = self.speed

    def set_length(self, diff=1):
        """
        alter snake length (self)
        """
        self.length += diff

    def add_score(self):
        """
        calculates score based on the movement speed and calculated modifier
        """
        self.score += self.speed * self.score_modifier
        if self.incremental_game:
            self.last_increase += 1
            if self.last_increase >= 5:
                self.last_increase = 0
                self.set_speed()

    def draw_snake(self, d=None, block_size=10):
        """
        :param d: what display to execute om
        :param block_size: used scale for each block
        :return: drawing of snake on the game screen
        """
        for x in self.snake_list:
            pygame.draw.rect(d, self.snake_color, [x[0], x[1], block_size, block_size])

    def random_food(self):
        """
        :return: choice of food for the incremental game, with some limitations based on snake status
        """
        if self.score == 500:
            options = [LoadConfig.orange, LoadConfig.blue]
            r = random.randrange(1, 20)
            print(r)
            r = 1
            if r == 1 or r == 20:
                if self.length <= 5:
                    options.remove(LoadConfig.blue)
                if self.speed <= 5:
                    options.remove(LoadConfig.orange)
                if not options == []:
                    return random.choice(options)
            return None

    def print_scoreboard(self, d=None, c=None):
        """
        :param d: what display to execute om
        :param c: loaded configuration from file and preset
        :return: draws score panel on the bottom of the screen
        """
        pygame.draw.rect(d, LoadConfig.grey, (0, c.dis_height, c.dis_width, c.score_row_height))
        value = pygame.font.SysFont("bahnschrift", 25).render("Score: " + str(self.score), True, LoadConfig.blue)
        return d.blit(value, [10, c.dis_height + c.score_row_height / 4])


def print_high_scores(config=None, d=None):
    """
    :param config: loaded configuration from file and preset
    :param d: what display to execute om
    :return: high scores read and diaplayed on screen
    """
    d.fill(config.grey)
    with open('cfg/scores.json') as score_file:
        scores = json.load(score_file)
    for j, c in enumerate(scores):
        item = pygame.font.SysFont("bahnschrift", 25).render(
            str(j + 1) + "." + " " * (6 - len(str(j + 1))) + str(scores[j][0])
            + " - " + scores[j][1], True, config.black)
        d.blit(item, [config.dis_height / 10, (j + 4) * 30])
    value = pygame.font.SysFont("bahnschrift", 25).render("Press 'up' or 'down' to return to menu", True, config.blue)
    d.blit(value, [10, config.dis_height + config.score_row_height / 4])
    pygame.display.update()


def save_score(new_score, score_date):
    """
    loads score file, checks if the score is higher than any of the saved
    :return: true if a new high score is accomplished, false if not
    """
    with open('cfg/scores.json') as score_file:
        h_scores = json.load(score_file)
    h_scores.append([new_score, score_date])
    h_scores = sorted(h_scores, key=itemgetter(0), reverse=True)
    h_scores.remove(h_scores[-1])
    with open('cfg/scores.json', 'w') as output:
        output.write(json.dumps(h_scores))
    return True if h_scores.__contains__([new_score, score_date]) else False


def game_loop(disp, config=None, incremental=False):
    """
    :param disp: what display to run the game on
    :param config: loaded game config from file
    :param incremental: set to true to run incremental speed game mode
    :return: returns to navigation menu, calls function to save score
    """
    game_close = False
    x1_change = 0
    y1_change = 0
    x1 = config.dis_width / 2
    y1 = config.dis_height / 2

    clock = pygame.time.Clock()
    player1 = Snake()
    player1.set_speed(config.speed)
    player1.incremental_game = incremental
    foodx = round(random.randrange(0, config.dis_width - config.snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, config.dis_height - config.snake_block) / 10.0) * 10.0
    foodx_inc = 0
    foody_inc = 0
    locked_key = 0
    food_type = None

    while not game_close:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not locked_key == pygame.K_LEFT:
                    x1_change = -config.snake_block
                    y1_change = 0
                    locked_key = pygame.K_RIGHT
                elif event.key == pygame.K_RIGHT and not locked_key == pygame.K_RIGHT:
                    x1_change = config.snake_block
                    y1_change = 0
                    locked_key = pygame.K_LEFT
                elif event.key == pygame.K_UP and not locked_key == pygame.K_UP:
                    y1_change = -config.snake_block
                    x1_change = 0
                    locked_key = pygame.K_DOWN
                elif event.key == pygame.K_DOWN and not locked_key == pygame.K_DOWN:
                    y1_change = config.snake_block
                    x1_change = 0
                    locked_key = pygame.K_UP

        if x1 >= config.dis_width or x1 < 0 or y1 >= config.dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        disp.fill(config.white)
        pygame.draw.rect(disp, config.red, [foodx, foody, config.snake_block, config.snake_block])
        snake_head = [x1, y1]
        player1.snake_list.append(snake_head)
        if len(player1.snake_list) > player1.length:
            del player1.snake_list[0]

        for x in player1.snake_list[:-1]:
            if x == snake_head:
                game_close = True

        player1.draw_snake(d=disp, block_size=config.snake_block)
        player1.print_scoreboard(c=config, d=disp)
        if food_type is not None:
            pygame.draw.rect(disp, food_type, [foodx_inc, foody_inc, config.snake_block, config.snake_block])
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, config.dis_width - config.snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, config.dis_height - config.snake_block) / 10.0) * 10.0
            player1.set_length()
            player1.add_score()

        if incremental and player1.score == 500 and food_type is None:
            foodx_inc = round(random.randrange(0, config.dis_width - config.snake_block) / 10.0) * 10.0
            foody_inc = round(random.randrange(0, config.dis_height - config.snake_block) / 10.0) * 10.0
            food_type = player1.random_food()

        if incremental and x1 == foodx_inc and y1 == foody_inc and food_type is not None:
            if food_type == config.orange:
                player1.set_speed(diff=-2)
                player1.add_score()
            if food_type == config.blue:
                player1.set_length(diff=-2)

            while True:
                foodx_inc = round(random.randrange(0, config.dis_width - config.snake_block) / 10.0) * 10.0
                foody_inc = round(random.randrange(0, config.dis_height - config.snake_block) / 10.0) * 10.0
                if not (foodx_inc == foodx and foody_inc == foody):
                    break
            food_type = player1.random_food()

        clock.tick(player1.speed)
    new_hs = save_score(player1.score, str(date.today()))
    navigate_menu(disp=disp, config=config, last_score=player1.score, new_highscore=new_hs)


def print_menu(config=None, disp=None, text_lines=None, s=0, i=1, new_highscore=False):
    """
    config = settings loaded from file
    text_lines - menu option to print\n
    i - active menu selection; set to 1 by default
    s - score to display as message
    """

    disp.fill(config.grey)
    if text_lines is None:
        text_lines = []

    if s != 0 and new_highscore is True:
        item = pygame.font.SysFont("bahnschrift", 25).render("New high score: " + str(s), True, config.orange)
        text_width = item.get_width()
        disp.blit(item, [config.dis_width - text_width - config.dis_width / 10, config.dis_height / 20])
    if s != 0 and new_highscore is False:
        item = pygame.font.SysFont("bahnschrift", 25).render("Last score: " + str(s), True, config.blue)
        text_width = item.get_width()
        disp.blit(item, [config.dis_width - text_width - config.dis_width / 10, config.dis_height / 20])

    for j, c in enumerate(text_lines):
        l_color = config.red if i == j else config.black
        item = pygame.font.SysFont("bahnschrift", 25).render(c, True, l_color)
        disp.blit(item, [config.dis_height / 10, (j + 3) * config.dis_height / 20])


def navigate_menu(config=None, disp=None, last_score=0, new_highscore=False):
    """
    processes keyboard input
    """
    play_game = True
    menu_text = [
        "Start normal game",
        "Start incremental game",
        "High scores",
        "Quit"]
    menu_opt_count = len(menu_text) - 1
    i = 0

    disp.fill(config.grey)
    print_menu(config=config, disp=disp, text_lines=menu_text, i=i, s=last_score, new_highscore=new_highscore)
    pygame.display.update()

    while play_game:
        for selection in pygame.event.get():
            if selection.type == pygame.KEYDOWN:
                if selection.key == pygame.K_q:
                    print("Quit")
                    play_game = False
                elif selection.key == pygame.K_UP:
                    i = i - 1 if i > 0 else menu_opt_count
                    print_menu(config=config, disp=disp, text_lines=menu_text, s=last_score, i=i,
                               new_highscore=new_highscore)
                    pygame.display.update()
                elif selection.key == pygame.K_DOWN:
                    i = i + 1 if i < menu_opt_count else 0
                    print_menu(config=config, disp=disp, text_lines=menu_text, s=last_score, i=i,
                               new_highscore=new_highscore)
                    pygame.display.update()
                elif selection.key == pygame.K_RETURN:
                    if menu_text[i] == "Start normal game":
                        game_loop(disp=disp, config=config, incremental=False)
                    elif menu_text[i] == "High scores":
                        print_high_scores(config=config, d=disp)
                    elif menu_text[i] == "Start incremental game":
                        game_loop(disp=disp, config=config, incremental=True)
                    elif menu_text[i] == "Quit":
                        play_game = False

    pygame.quit()
    quit()


def main():
    global display
    pygame.init()
    pygame.display.set_caption("Python the Game")
    config = LoadConfig()
    display = pygame.display.set_mode((config.dis_width, config.dis_height + config.score_row_height))
    navigate_menu(config, disp=display)


if __name__ == "__main__":
    main()
