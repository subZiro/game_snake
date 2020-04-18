# -*- coding: utf-8 -*-


from random import randint
import time
import sys


import pygame


class Game():
    """отрисовка поля для игры, проверка на ошибка, обработка нажатий пользователя"""
    def __init__(self, w=500, h=500):
        """инит игры"""
        # задаем размеры экрана
        self.screen_width = w
        self.screen_height = h
        # цвета
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)
        # обновление экрана, количество кадров в секунду
        self.fps = pygame.time.Clock()
        # результат, скор съеденых яблок
        self.score = 0

    def check_errors(self):
        """функция проверки ошибок при запуске pygame"""
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('No error. GL, HF')

    def refresh_screen(self):
        """обновляем экран и задаем фпс"""
        pygame.display.flip()
        self.fps.tick(23)

    def user_actions(self, change_to):
        """обработка действий пользователя"""
        for action in pygame.event.get():
            # если пользователь нажал клавишу
            if action.type == pygame.KEYDOWN:
                # обработка клавиш передвижения змеи ['right', 'left', 'up', 'down']
                if action.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                elif action.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                elif action.key == pygame.K_UP:
                    change_to = 'UP'
                elif action.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                elif action.key == pygame.K_ESCAPE:
                    # если нажали клавишу 'ESC', выход из игры
                    pygame.quit()
                    sys.exit()
        return change_to

    def title_playwindow(self):
        """Задаем загаловок игрового окна,
        Задаем play_surface (игроое поле, поверх которого будут отривовываться все элементы)"""
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('SnakeGame')

    def show_score(self, mode=True):
        """отображение результата"""
        #pygame.font.init()
        #str_font = pygame.font.SysFont('serif', 20)
        score_font = pygame.font.Font('Roboto-Bold.ttf', 20)
        score_surf = score_font.render(f'Your score: {self.score}', True, self.black)
        score_rect = score_surf.get_rect()

        if mode:
            # режим отображения счета 1 - результат в левом верхнем углу
            score_rect.midtop = (80, 10)
        else:
            # при конце игры 0 - результат по центру
            score_rect.midtop = (360, 120)

        # рисуем прямоугольник поверх surface
        self.play_surface.blit(score_surf, score_rect)

    def end_game(self):
        """обработка событий завержения игры
        вывод сообщения о завершении и достигнутого результата"""
        #end_font = pygame.font.SysFont('serif', 70)
        end_font = pygame.font.Font('Roboto-Bold.ttf', 70)
        end_surf = end_font.render('Game Over', True, self.red)
        end_rect = end_surf.get_rect()
        # вывод сообщения о конце игры и финального счета
        end_rect.midtop = (360, 15)
        self.play_surface.blit(end_surf, end_rect)
        self.show_score(mode=False)
        # пауза
        pygame.display.flip()
        time.sleep(3)
        # выход
        pygame.quit()
        sys.exit()



class Apple():
    """еда змейки"""
    def __init__(self, screen_width, screen_height, color):
        """Инит еды"""
        self.size_x = 10
        self.size_y = 10
        self.color = color
        self.position = [randint(1, screen_width/10)*10, randint(1, screen_height/10)*10]

    def draw(self, play_surface):
        """Отображение еды"""
        pygame.draw.rect(play_surface,
                         self.color,
                         pygame.Rect(self.position[0], self.position[1],
                                     self.size_x, self.size_y)
                         )


class Snake():
    """класс змеи"""
    def __init__(self, color=(255, 0, 0)):
        """инит змеи"""
        self.head = [100, 10]  # [x, y]
        # начальное тело змеи состоит из трех сегментов
        # голова змеи - первый элемент, хвост - последний
        self.body = [[100, 10], [90, 10], [80, 10]]
        self.color = color  # цвет змейки
        self.direction = "RIGHT"  # начальное движение змеи
        self.change_to = self.direction

    def change_head_position(self):
        """Изменение положение головы змеи"""
        if self.direction == "RIGHT":
            self.head[0] += 10
        elif self.direction == "DOWN":
            self.head[1] += 10
        elif self.direction == "LEFT":
            self.head[0] -= 10
        elif self.direction == "UP":
            self.head[1] -= 10

    def change_body_position(self, apple_position, screen_width, screen_height, score):
        """изменение положения тела змеи, увеличение счетчика съеденых яблок"""
        self.body.insert(0, list(self.head))

        # если змейка съела яблоко
        if self.head[0] == apple_position[0] and self.head[1] == apple_position[1]:
            # если съели еду увеличиваем скор съеденых яблок
            # и задаем новое положение еды случайным
            score += 1
            apple_position = [randint(1, screen_width/10)*10, randint(1, screen_height/10)*10]
        else:
            # иначе убираем последний сегмент ()
            self.body.pop()

        return apple_position, score


    def draw(self, play_surface, surface_color):
        """Отображаем всю змею"""
        play_surface.fill(surface_color)
        for pos in self.body:
            pygame.draw.rect(play_surface, self.color, pygame.Rect(pos[0], pos[1], 10, 10))

    def check_endgame(self, end_game, screen_width, screen_height):
        """Проверка завершения игры (end_game)
        а - врезались в стену
        б - врезались в свое тело"""
        if any((self.head[0] > screen_width-10 or self.head[0] < 0,
               self.head[1] > screen_height-10 or self.head[1] < 0)):
            end_game()

        for elem in self.body[1:]:
            # проверка на то, что первый элемент(голова) врезался в
            # любой другой элемент змеи (закольцевались)
            if elem[0] == self.head[0] and elem[1] == self.head[1]:
                end_game()

    def validate_change_to(self):
        """Проверка изменения напрввления движения змей,
        не допустимо противоположное текущему"""
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to


def game_loop(game, snake, apple):
    """петля игры"""
    while True:
        try:
            snake.change_to = game.user_actions(snake.change_to)
            snake.validate_change_to()

            snake.change_head_position()

            apple.position, game.score = snake.change_body_position(apple.position, 
                                                                    game.screen_width,
                                                                    game.screen_height,
                                                                    game.score)

            #отрисовка змеи и яблока
            snake.draw(game.play_surface, game.green)
            apple.draw(game.play_surface)
            # проверка не закончилась ли игра
            snake.check_endgame(game.end_game, game.screen_width, game.screen_height)
            # отображение результата
            game.show_score()
            # обновление игрового поля
            game.refresh_screen()
                
        except Exception as e:
            print(f'Error, {e}')
            pygame.quit()
            sys.exit()


def main():
    """главная программа"""
    # now use display and fonts
    pygame.init()
    pygame.font.init()
    print('start')

    #инит классов
    game = Game(w=720, h=460)
    snake = Snake(color=game.white)
    apple = Apple(screen_width=game.screen_width, screen_height=game.screen_height, color=game.brown)

    #пауза
    time.sleep(3)

    # проверка ошибок
    game.check_errors()
    # отрисовка игровой области
    game.title_playwindow()
    #игровая петля
    game_loop(game, snake, apple)

    time.sleep(15)


if __name__ == '__main__':
    main()