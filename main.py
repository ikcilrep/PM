from app.security.password_storing import hash_digest, verify_password
from app.user import User, decrypt_user, read_encrypted_user, does_user_exist
from app.account import Account
from app.security.AES import derive_key
from app.security.password_generator import generate_password
from pyperclip import copy
from getpass import getpass

def register(username, password):
    user = User(username, derive_key(password), password, hash_digest(password))
    user.save()
    return user

def ask(question, answers_set):
    answer = None
    while answer not in answers_set:
        answer = input(question)
    return answer


print('Have you already got an account?')

is_not_registered = ask('[y/n]:\t', {'y', 'n'}) == 'n'

if is_not_registered: print('Sign in then!')
else: print('Sign up then!')


username = input('Username:\t')

password, password_repetition = '', None 

user = None
if is_not_registered:
    while password != password_repetition:
        password = getpass('Password:\t')
        password_repetition = getpass('Repeat password:\t')
    user = register(username, password)
else:
    while not does_user_exist(username):
        print("User with this name doesn't exist. Try again.")
        username = input('Username:\t')
    encrypted_user = read_encrypted_user(username)
    while True:
        password = getpass('Password:\t')
        if verify_password(password, encrypted_user['hashed_password']):
            break
    user = decrypt_user(encrypted_user, password)



try:
    while True:
        print('1) List accounts')
        print('2) Add account')
        print('3) Change password')
        print('4) Generate cryptographically secure password')
        print('5) Quit')
        answer = ask('Choose:\t', {'1', '2', '3', '4', '5'}) 
        if answer == '1':
            print('Your accounts:')
            for index, account in enumerate(user.accounts):
                print('\t' + str(index) + ')', account.service_name + ':', account.username)
            print('Do you want to check or edit details of some account?')
            answer = ask('[y/n]:\t', {'y', 'n'}) 
            if answer == 'y':
                print('Which one?')
                index = int(ask('Choose:\t', {str(index) for index in range(len(user.accounts))}))
                account = user.accounts[index] 
                print('Choosen account:')
                print('\t1) Service name:\t', account.service_name)
                print('\t2) Username:\t', account.username)
                print('\t3) Email:\t', account.email)
                print('\t4) Password:\t', account.password)
                print('Do you want to change some information?') 
                answer = ask('[y/n]:\t', {'y', 'n'}) 
                if answer == 'y':
                    print('Which one?')
                    answer = ask('Choose:\t', {'1', '2', '3', '4'}) 
                    if answer == '1':
                        account.service_name = input('New account service name:\t')
                    elif answer == '2':
                        account.username = input('New account username:\t')
                    elif answer == '3':
                        account.email = input('New account email:\t')
                    elif answer == '4':
                        account.password = getpass('New account password:\t')

        elif answer == '2':
            user.add_account(
                    Account(
                        input('Service name:\t'),
                        input('Username:\t'),
                        input('Email:\t'),
                        getpass('Password:\t')
                        )
                    )
        elif answer == '3':
            user.password = getpass('New user password:\t')
        elif answer == '4':
            length = int(input('Enter what length this password should have:\t'))
            print('Should this password have punctuation chars?')
            should_have_punctuation = ask('[y/n]:\t', {'y', 'n'}) == 'y'
            print('Should this password have digits?')
            should_have_digits = ask('[y/n]:\t', {'y', 'n'}) == 'y'
            password = generate_password(length,should_have_punctuation, should_have_digits)
            print(password)
            copy(password)
            print('Password was copied to clipboard!')
        else:
            break
except KeyboardInterrupt:
    pass
finally:
    print('Saving...')
    user.save()
