# write your code here
msg_0 = "Enter an equation"
msg_1 = "Do you even know what numbers are? Stay focused!"
msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
msg_3 = "Yeah... division by zero. Smart move..."
msg_4 = "Do you want to store the result? (y / n):"
msg_5 = "Do you want to continue calculations? (y / n):"
msg_6 = " ... lazy"
msg_7 = " ... very lazy"
msg_8 = " ... very, very lazy"
msg_9 = "You are"
msg_silly = ["Are you sure? It is only one digit! (y / n)",
             "Don't be silly! It's just one number! Add to the memory? (y / n)",
             "Last chance! Do you really want to embarrass yourself? (y / n)"]
divider = ' '


def check_part(x: str):
    return all(elem.isnumeric() for elem in x.split('.')) or x.lower() == 'm'


def is_one_digit(x):
    return 10 > x > -10 and float(x).is_integer()


def check_laziness(a, b, oper):
    msg = ''
    if is_one_digit(a) and is_one_digit(b):
        msg += msg_6
    if a == 1 or b == 1:
        msg += msg_7
    if (a == 0 or b == 0) and oper in ['+', '-', '*']:
        msg += msg_8
    if msg != '':
        print(msg_9 + msg)


def read_exact(msg=''):
    ch = input(msg)
    while ch.lower() != 'y' and ch.lower() != 'n':
        ch = input(msg)
    return ch.lower()


def calc():
    memory = 0
    while True:
        inp = input(msg_0)
        x, oper, y = inp.split(divider)
        if not check_part(x) or not check_part(y):
            print(msg_1)
        else:
            a, b = float(x) if x.lower() != 'm' else memory, float(y) if y.lower() != 'm' else memory
            check_laziness(a, b, oper)
            if oper not in ['+', '-', '*', '/']:
                print(msg_2)
            else:
                if oper == '/' and b == 0:
                    print(msg_3)
                else:
                    result = None
                    match oper:
                        case '+':
                            result = a + b
                        case '-':
                            result = a - b
                        case '/':
                            result = a / b
                        case '*':
                            result = a * b
                    print(result)
                    ch = read_exact(msg_4)
                    if ch == 'y':
                        if is_one_digit(result):
                            calls = 0
                            while True:
                                ch = read_exact(msg_silly[calls])
                                if ch == 'y':
                                    if calls < 2:
                                        calls += 1
                                    else:
                                        memory = result
                                        break
                                else:
                                    break
                        else:
                            memory = result
                    ch = read_exact(msg_5)
                    if ch == 'n':
                        break


if __name__ == '__main__':
    calc()
