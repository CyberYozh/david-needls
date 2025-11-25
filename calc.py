import ctypes
import sys
import os

def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

def calculator():
    print("Простой Калькулятор")
    print("--------------------")
    a = float(input("Введите первое число: "))
    b = float(input("Введите второе число: "))

    print("Выберите операцию:")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")

    op = input("Введите номер операции: ")

    if op == "1":
        print("Результат:", a + b)
    elif op == "2":
        print("Результат:", a - b)
    elif op == "3":
        print("Результат:", a * b)
    elif op == "4":
        if b != 0:
            print("Результат:", a / b)
        else:
            print("Ошибка: Деление на ноль невозможно.")
    else:
        print("Неверный выбор.")

if __name__ == "__main__":
    run_as_admin()
    calculator()
