import pygame
import random

pygame.init()

dis_width = 800
dis_height = 600
score_row_height = 50

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


def print_menu(text_lines=None, i=1):
    # pygame.draw.rect(dis, gray, (dis_width/10, dis_height/10, dis_width*0.8, score_row_height*0.8))
    if text_lines is None:
        text_lines = []
    for j, c in enumerate(text_lines):
        l_color = red if i == j else black
        item = game_msg_font.render(c, True, l_color)
        dis.blit(item, [dis_height / 10, (j + 2) * 30])


def print_scoreboard(score):
    pygame.draw.rect(dis, gray, (0, dis_height, dis_width, score_row_height))
    value = score_font.render("Your Score: " + str(score), True, blue)
    dis.blit(value, [10, dis_height + score_row_height / 4])


def snake(snake_location, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_location, snake_location])


def message(msg, color):
    mesg = game_msg_font.render(msg, True, color)
    dis.blit(mesg, [50, dis_height / 3])


def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_close:

        # while game_close == True:
        #     dis.fill(black)
        #     message("Game over! Press C-Play Again or Q-Quit", gray)
        #     print_scoreboard(length_of_snake - 1)
        #     pygame.display.update()
        #
        #     for event in pygame.event.get():
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_q:
        #                 game_over = True
        #                 game_close = False
        #             if event.key == pygame.K_c:
        #                 gameLoop()

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
                # elif event.key == pygame.K_PAUSE:
                #     for key in pygame.event.get():
                #         if key.key == pygame.K_PAUSE:
                #             break

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_List.append(snake_head)
        if len(snake_List) > length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_head:
                game_close = True

        snake(snake_block, snake_List)
        print_scoreboard(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    # pygame.quit()
    # quit()
    main(score=length_of_snake)


def main(score=0):
    # gameLoop()

    play_game = True
    menu_text = [
        "Start normal game",
        "Start incremental game",
        "Highscores",
        "Settings",
        "Quit"]
    menu_choices = len(menu_text) - 1
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
                    i = i - 1 if i > 0 else menu_choices
                    print_menu(text_lines=menu_text, i=i)
                    pygame.display.update()
                    # print(i)
                elif selection.key == pygame.K_DOWN:
                    i = i + 1 if i < menu_choices else 0
                    print_menu(text_lines=menu_text, i=i)
                    pygame.display.update()
                elif selection.key == pygame.K_RETURN:
                    if menu_text[i] == "Start normal game":
                        gameLoop()
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
