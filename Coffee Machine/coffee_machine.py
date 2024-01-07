class CoffeeMachine:
    water = 400
    milk = 540
    beans = 120
    dcups = 9
    money = 550

    def __str__(self):
        return f'''The coffee machine has:
{self.water} ml of water
{self.milk} ml of milk
{self.beans} g of coffee beans
{self.dcups} disposable cups
${self.money} of money'''

    def fill(self, water, milk, beans, dcups):
        self.water += water
        self.milk += milk
        self.beans += beans
        self.dcups += dcups

    def buy(self, t):
        coffees = [
            [250, 0, 16, 1, 4],
            [350, 75, 20, 1, 7],
            [200, 100, 12, 1, 6],
        ]
        c = coffees[int(t) - 1]
        if self.water < c[0]:
            return 'Sorry, not enough water!'
        elif self.milk < c[1]:
            return 'Sorry, not enough milk!'
        elif self.beans < c[2]:
            return 'Sorry, not enough coffee beans!'
        elif self.dcups < c[3]:
            return 'Sorry, not enough disposable cups!'
        else:
            self.water -= c[0]
            self.milk -= c[1]
            self.beans -= c[2]
            self.dcups -= c[3]
            self.money += c[4]
            return 'I have enough resources, making you a coffee!'


    def take(self):
        print(f'I gave you ${self.money}')
        ret = self.money
        self.money = 0
        return ret


my = 0
machine = CoffeeMachine()

while True:
    action = input('Write action (buy, fill, take, remaining, exit): ')
    match action:
        case 'buy':
            ch = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
            if ch == 'back':
                continue
            else:
                print(machine.buy(ch))
        case 'fill':
            water = int(input('Write how many ml of water you want to add: '))
            milk = int(input('Write how many ml of milk you want to add: '))
            beans = int(input('Write how many grams of coffee beans you want to add: '))
            dcups = int(input('Write how many disposable cups you want to add: '))
            machine.fill(water, milk, beans, dcups)
        case 'take':
            my += machine.take()
        case 'remaining':
            print(machine)
        case 'exit':
            break
