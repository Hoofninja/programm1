import os
import matplotlib.pyplot as plt
import tkinter
import keyboard


class Field():
    # Класс, содержащий Х и Y координаты спектра в конкретной области

    def __init__(self, x, y, file_name):
        # Инициализируем переменные, массив Хов и массив Yов

        self.x = x
        self.y = y
        self.file_name = file_name

    def graph(self):
        #  Метод, который будет строить график

        plt.plot(self.x, self.y)
        plt.title(self.file_name)
        plt.show()

    def peak(self, x_1_1, x_1_2, min_max) -> bool:
        # Метод, который будет проверять есть ли пик или нет, возвращая True или False

        x_temp = []
        y_temp = []
        for i in range(len(self.x)):
            if x_1_1 < self.x[i] < x_1_2:
                x_temp.append(self.x[i])
                y_temp.append(self.y[i])
        multiplayer = min_max[0]
        min_max = float(min_max.replace(min_max[0], ""))
        if multiplayer == "*":
            peak_value = min(y_temp) * min_max
        if multiplayer == "+":
            peak_value = min(y_temp) + min_max
        if multiplayer == "-":
            peak_value = min(y_temp) - min_max
        if multiplayer == "/":
            peak_value = min(y_temp) / min_max

        if max(y_temp) >= peak_value:
            return True
        else:
            return False


def fields_list(dirrectory):
    # Функция открывает поочереди все файлы в указанной дерриктории,
    # создает для каждого файла объект класса Field и создает список этих объектов
    list_of_fields = []
    folder_list = os.listdir(dirrectory)
    for folder in folder_list:
        file_list = os.listdir(dirrectory + "//" + folder)
        for file in file_list:
            file_name = dirrectory + "//" + folder + "//" + file
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


def width_height(dirrectory):
    # Функция которая считает количество шагов по горизонтали и вертикали

    folder_list = os.listdir(dirrectory)
    for folder in folder_list:
        file_list = os.listdir(dirrectory + "//" + folder)
    return [len(file_list), len(folder_list)]


def pic(x_1_1, x_1_2, min_max, list):
    # Отрисовывает итоговый результат

    window = tkinter.Tk()
    window.config(width=504, height=984, background="black")
    window.geometry("504x984+0+0")
    window.title("Результат")
    canvas = tkinter.Canvas(background="lightyellow")
    canvas.pack()
    canvas.config(width=504, height=984)

    n1 = 0
    n2 = 0
    for element in list:
        if element.peak(x_1_1, x_1_2, min_max) is True:
            canvas.create_rectangle(n2 * 24, n1 * 24, (n2+1)*24, (n1+1)*24, width=1.5, fill="#008000")
        else:
            canvas.create_rectangle(n2 * 24, n1 * 24, (n2+1)*24, (n1+1)*24, width=1.5, fill="#ff0000")
        if n1 == 40:
            n1 = 0
            n2 += 1
        else:
            n1 += 1

    window.mainloop()


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
        x_1_1 = float(input("Координата левой точки по Х: "))
        x_1_2 = float(input("Координата правой точки по Х: "))
        min_max = input("Что считать пиокм? ")
        pic(x_1_1=x_1_1, x_1_2=x_1_2, min_max=min_max,list=final_list)
        os.system('cls' if os.name == 'nt' else 'clear')


dirrectory = input("Введите месторасположение файлов (можно просто перетащить папку в строку): ")
os.system('cls' if os.name == 'nt' else 'clear')
final_list = fields_list(dirrectory=dirrectory)
while True:
    menu_1(final_list=final_list)

