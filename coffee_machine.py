class CoffeeMachine:
    recipes = {'1': [250, 0, 16, 1, 4], '2': [350, 75, 20, 1, 7], '3': [200, 100, 12, 1, 6]}

    def __init__(self, supplies):
        self.supplies = supplies
        self.mode = 'main_menu'
        self.turn_on = True

    def user_prompt(self):
        action = input('Write action (buy, fill, take, remaining, exit):\n')
        if action == 'buy':
            self.buy_mode()
        elif action == 'fill':
            self.fill_mode()
        elif action == 'take':
            self.take_mode()
        elif action == 'remaining':
            self.show_supplies()
        elif action == 'exit':
            self.turn_on = False

    def buy_mode(self):
        choice = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\n')
        if choice != 'back':
            self.make_coffee(choice)

    def fill_mode(self):
        self.supplies[0] += (int(input('Write how many ml of water do you want to add:\n')))
        self.supplies[1] += (int(input('Write how many ml of milk do you want to add:\n')))
        self.supplies[2] += (int(input('Write how many grams of coffee beans do you want to add:\n')))
        self.supplies[3] += (int(input('Write how many disposable cups of coffee do you want to add:\n')))

    def take_mode(self):
        print(f'I gave you ${self.supplies[4]}')
        self.supplies[4] = 0

    def make_coffee(self, choice: str):
        recipe = CoffeeMachine.recipes[choice]
        supplies_names = ['water', 'milk', 'coffee beans', 'disposable cups']
        supplies_availability = [self.supplies[i] - recipe[i] >= 0 for i in range(4)]
        if all(supplies_availability):
            print('I have enough resources, making you a coffee!')
            for i in range(4):
                self.supplies[i] -= recipe[i]
            self.supplies[4] += recipe[4]
        else:
            for i in range(len(supplies_names)):
                if not supplies_availability[i]:
                    print(f'Sorry, not enough {supplies_names[i]}')

    def show_supplies(self):
        print(f'''The coffee machine has:
    {self.supplies[0]} of water
    {self.supplies[1]} of milk
    {self.supplies[2]} of coffee beans
    {self.supplies[3]} of disposable cups
    {self.supplies[4]} of money''')


def main():
    # water, milk, coffee beans, cups, money
    supplies = [400, 540, 120, 9, 550]
    coffee_machine = CoffeeMachine(supplies)
    while coffee_machine.turn_on:
        coffee_machine.user_prompt()
        print()


if __name__ == '__main__':
    main()
