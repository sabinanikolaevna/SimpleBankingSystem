
import sqlite3
import random
def luhn(card_number):
    temp = list(card_number).copy()
    check_digit = temp.pop()
    index = 0
    for digit in temp:
        if (index + 1) % 2 != 0:
            temp[index] = int(digit) * 2
        index += 1
    index = 0
    for digit in temp:
        if int(digit) > 9:
            temp[index] = int(digit) - 9
        index += 1
    total = 0
    for digit in temp:
        total += int(digit)
    return int(check_digit) == ((total * 9) % 10)
existing_cards = {}
def create_table():
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS card (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            pin TEXT NOT NULL,
            balance INTEGER DEFAULT 0
            )''')
    conn.commit()
    conn.close()
def menu():
    print('1. Create an account\n2. Log into account\n0. Exit')
    command = input()
    if command =='1':
        creating()
    elif command == '2':
        loging()
    elif command =='0':
        print('Bye!')
def creating():
    card = [4, 0, 0, 0, 0, 0] + random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 9)
    temp = card.copy()
    index = 0
    for digit in temp:
        if (index + 1) % 2 != 0:
            temp[index] = digit * 2
        index += 1
    index = 0
    for digit in temp:
        if digit > 9:
            temp[index] = digit - 9
        index += 1
    total = sum(temp)
    card.append((total * 9) % 10)
    final_card = int("".join(map(str, card)))
    pin = ''.join([random.choice(list('0123456789')) for x in range(4)])
    print(f'Your card has been created\nYour card number:\n{final_card}\nYour card PIN:\n{pin}')
    existing_cards[str(final_card)] = pin
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()
    c.execute(f'''INSERT into card (number, pin, balance) VALUES ("{final_card}", "{pin}", "0")''')
    conn.commit()
    conn.close()
    menu()
def loging():
    card_number = input('Enter your card number:\n')
    pin = input('Enter your PIN:\n')
    if card_number not in existing_cards.keys() or existing_cards[card_number] != pin:
        print('Wrong card number or PIN!')
        menu()
    elif card_number in existing_cards.keys() and existing_cards[card_number] == pin:
        print('You have successfully logged in!')
        while True:
            command = input('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
            if command == '1':
                conn = sqlite3.connect('card.s3db')
                c = conn.cursor()
                balance = c.execute(f'''SELECT balance FROM card WHERE number = "{card_number}"''')
                print(f'Balance: {balance}')
                conn.commit()
                conn.close()

            elif command == '2':
                income = int(input('Enter income:\n'))
                conn = sqlite3.connect('card.s3db')
                c = conn.cursor()
                c.execute(f'''SELECT balance FROM card WHERE number = "{card_number}"''')
                current_balance = c.fetchall()
                balance = int(current_balance[0][0]) + int(income)
                print(balance)
                c.execute(f'''UPDATE card SET balance = {balance} WHERE number = {card_number}''')
                conn.commit()
                conn.close()

                print('Income was added!')
            elif command == '3':
                transfer_card = input('Enter card number:')
                if transfer_card == card_number:
                    print("You can't transfer money to the same account!")
                elif not luhn(transfer_card):
                    print('Probably you made a mistake in the card number. Please try again!')
                elif transfer_card not in existing_cards.keys():
                    print('Such a card does not exist.')
                else:
                    amount = int(input('Enter how much money you want to transfer:\n'))
                    conn = sqlite3.connect('card.s3db')
                    c = conn.cursor()
                    c.execute(f'''SELECT balance FROM card WHERE number = "{card_number}"''')
                    balance = c.fetchall()[0][0]
                    conn.commit()
                    conn.close()
                    if balance < amount:
                        print('Not enough money!')
                    else:
                        balance -= amount
                        conn = sqlite3.connect('card.s3db')
                        c = conn.cursor()
                        c.execute(f'''SELECT balance FROM card WHERE number = "{card_number}"''')
                        current_balance = c.fetchall()
                        balance = int(current_balance[0][0]) - int(amount)
                        c.execute(f'''UPDATE card SET balance = {balance} WHERE number = {card_number}''')
                        conn.commit()
                        conn.close()
                        conn = sqlite3.connect('card.s3db')
                        c = conn.cursor()
                        c.execute(f'''SELECT balance FROM card WHERE number = "{transfer_card}"''')
                        reciever_balance = c.fetchall()[0][0]
                        reciever_balance_new = int(reciever_balance) + int(amount)
                        c.execute(f'''UPDATE card SET balance = {reciever_balance_new} WHERE number = {transfer_card}''')
                        conn.commit()
                        conn.close()
                        print('Success!')
            elif command == '4':
                conn = sqlite3.connect('card.s3db')
                c = conn.cursor()
                c.execute(f'''DELETE FROM card WHERE number = {card_number}''')
                conn.commit()
                conn.close()
                print('The account has been closed!')

            elif command == '5':
                print('You have successfully logged out!')

            elif command == '0':
                print('Bye!')
                break

create_table()
menu()

