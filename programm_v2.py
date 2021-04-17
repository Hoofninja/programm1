import matplotlib.pyplot as plt
import os
import pygame
import sys


class Field:

    # Init variables, X and Y lists
    def __init__(self, x, y, file_name):
        self.x = x
        self.y = y
        self.file_name = file_name

    # Plot X Y graphic
    def graph(self):
        plt.plot(self.x, self.y)
        plt.title(self.file_name)
        plt.show()

    # Detects the presence of a peak
    def peak(self, left_x, right_x, min_max) -> bool:
        x_temp = []
        y_temp = []
        for i in range(len(self.x)):
            if left_x < self.x[i] < right_x:
                x_temp.append(self.x[i])
                y_temp.append(self.y[i])
        multiplier = min_max[0]
        min_max = float(min_max.replace(min_max[0], ""))
        if multiplier == "*":
            peak_value = min(y_temp) * min_max
        if multiplier == "+":
            peak_value = min(y_temp) + min_max
        if multiplier == "-":
            peak_value = min(y_temp) - min_max
        if multiplier == "/":
            peak_value = min(y_temp) / min_max

        # tg = False
        # if max(y_temp) != y_temp[0] and max(y_temp) != y_temp[-1]:
        #     tg = True
        #
        # if (max(y_temp) >= peak_value) and (tg is True):
        #     return True
        # else:
        #     return False
        if max(y_temp) >= peak_value:
            return True
        else:
            return False


# Open all fails in directory by rotation,
# create Field object for each file and create list of Fields
def fields_list(directory):
    list_of_fields = []
    folder_list = os.listdir(directory)
    for folder in folder_list:
        file_list = os.listdir(directory + "//" + folder)
        for file in file_list:
            file_name = directory + "//" + folder + "//" + file
            f = open(file_name, "r")
            xy = f.readlines()
            x = []
            y = []
            for i in range(46, len(xy), 1):
                temp = xy[i]
                x.append(float(temp.split()[0]))
                y.append(float(temp.split()[1]))
            list_of_fields.append(Field(x, y, file))
    return list_of_fields


# Return list of 2 numbers. 0 element is number of folders
#                           1 element - number of files
def width_height(directory):
    folder_list = os.listdir(directory)
    file_list = os.listdir(directory + "//" + folder_list[0])
    return [len(file_list), len(folder_list)]


# Draw final picture
def picture(left_x, right_x, min_max, f_list):

    green = (0, 255, 0)
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    tile = 20

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((22*tile, 42*tile))
    pygame.display.set_caption('program_v2')
    clock = pygame.time.Clock()
    i = 1
    j = 1
    screen.fill(white)

    w_h = width_height(directory)

    for element in f_list:

        if element.peak(left_x, right_x, min_max) is True:
            pygame.draw.rect(screen, green, (i*tile, j*tile, tile, tile))
            # pygame.draw.rect(screen, black, (i*20, j*20, 20, 20), 1)
        else:
            pygame.draw.rect(screen, red, (i*tile, j*tile, tile, tile))
            # pygame.draw.rect(screen, black, (i * 20, j * 20, 20, 20), 1)
        if j == 41:
            j = 1
            i += 1
        else:
            j += 1

    for i in range(w_h[1]+1):
        pygame.draw.line(screen, black, (i * tile, 0), (i * tile, (w_h[0]+1) * tile))
    for j in range(w_h[0]+1):
        pygame.draw.line(screen, black, (0, j * tile), ((w_h[1]+1) * tile, j * tile))

    my_font = pygame.font.SysFont('timesnewroman', 16)
    text_surface = my_font.render('0   1   2   3   4   5   6   7   8   9  10 11 12 13 14 15 16 17 18 19 20 21',
                                  True, black)
    screen.blit(text_surface, (8, 0))

    numbers = []
    for i in range(41):
        numbers.append(str(i+1))

    for i in range(41):

        my_font = pygame.font.SysFont('timesnewroman', 16)
        text_surface = my_font.render(numbers[i], True, black)
        if int(numbers[i]) / 10 < 1:
            screen.blit(text_surface, (8, i*20+20))
        elif int(numbers[i]) / 10 >= 1:
            screen.blit(text_surface, (2, i * 20 + 20))

    while True:
        clock.tick(30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                i = pos[0]//tile - 1
                j = pos[1]//tile - 1
                if pygame.mouse.get_pressed() == (True, False, False):
                    f_list[i*41 + j].graph()
                if pygame.mouse.get_pressed() == (False, False, True):
                    if screen.get_at(pygame.mouse.get_pos()) == (0, 255, 0, 255):
                        pygame.draw.rect(screen, red, ((i+1) * tile, (j+1) * tile, tile, tile))
                        pygame.draw.rect(screen, black, ((i+1) * tile, (j+1) * tile, 21, 21), 1)
                    elif screen.get_at(pygame.mouse.get_pos()) == (255, 0, 0, 255):
                        pygame.draw.rect(screen, green, ((i+1) * tile, (j+1) * tile, tile, tile))
                        pygame.draw.rect(screen, black, ((i+1) * tile, (j+1) * tile, 21, 21), 1)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            save_name = input('имя сохраняемого файла \n')
            pygame.image.save(screen, save_name + '.PNG')


def menu_1(final_list):
    print("Выберите что хотите сделать и нажмите соответствующую цифру \n"
          "1 - построить график конкретного файла \n"
          "2 - построить карту пиков \n")
    pressed_key = input()
    if pressed_key == "1":
        width = int(input("\nВведите столбец файла, график которого хотите построить: "))
        height = int(input("\nВведите строку файла, график которого хотите построить: "))
        final_list[(width - 1)*41+(height-1)].graph()
        os.system('cls' if os.name == 'nt' else 'clear')
    elif pressed_key == "2":
        print("В какой области искать пик?")
        x_1_1 = float(input("Координата левой точки по Х: ").replace(',', '.'))
        x_1_2 = float(input("Координата правой точки по Х: ").replace(',', '.'))
        min_max = input("Что считать пиокм? ")
        picture(left_x=x_1_1, right_x=x_1_2, min_max=min_max, f_list=final_list)
        os.system('cls' if os.name == 'nt' else 'clear')


os.system('cls' if os.name == 'nt' else 'clear')
directory = input("Введите месторасположение файлов (можно просто перетащить папку в строку): ")
os.system('cls' if os.name == 'nt' else 'clear')
final_list = fields_list(directory=directory)
while True:
    menu_1(final_list=final_list)