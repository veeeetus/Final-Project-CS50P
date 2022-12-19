from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from texttable import Texttable
from hashlib import sha256
from colorama import Fore
from classes import User, Site
import sys, os, maskpass

# Start engine
engine = create_engine('sqlite:///app.db', future=True)

def main():
    os.system('clear')
    
    # user holds id of logged user
    user = None

    # Create encryption key and save it in a hidden file on machine
    try: 
        # If key was somehow deleted make new one
        if not os.stat(".key.txt").st_size > 0:
            generate_key()
        else:
            pass
    # Generate new file if there is none
    except OSError:
        generate_key()

    while True:
        # First menu
        if not user:
            print(Fore.GREEN + table("not_logged").draw())
        
            # Get valid option
            option = get_opt(3)

            # Execute user's choice
            match option:
                # Log in
                case 1:
                    username = get_username()
                    if password := get_pass("log"):
                        user = log_user(username, password)
                # Register
                case 2:
                    username = get_username()
                    password = get_pass("reg")
                    if password:
                        register(username, password)
                        os.system('clear')
                        print(Fore.GREEN + 'Account created successfully')
                # Exit
                case 3:
                    print("Thanks for usage bye! ~Vetus")
                    sys.exit(0)
        else:
            # Logged menu
            print(Fore.GREEN + table("logged").draw())
                    
            option = get_opt(6)

            match option:
                # Add new passes
                case 1:
                    # Site|Login|Password
                    site = get_site("site")
                    login = get_site("login")
                    password = get_pass("site")

                    with Session(engine) as session, session.begin():
                        # Query for passes
                        stmt = select(Site).where(Site.site == site, Site.login == login)
                        result = session.execute(stmt).first()
                        # If they are found, don't add again
                        if result:
                            os.system("clear")
                            print(Fore.RED + "Account already added")
                        # Else add
                        else:
                            stmt = insert(Site).values(site=site, login=login, password=password, user_id=user)
                            session.execute(stmt)
                            os.system("clear")
                            print("Added succesfully")

                # List Id|Site|Login
                case 2:
                    stmt = select(Site).where(Site.user_id == user)

                    with Session(engine) as session:
                        os.system("clear")
                        result = session.scalars(stmt).all()
                        if not result:
                            os.system("clear")
                            print(Fore.RED + "You don't have any password yet")
                        else:
                            for x in result:
                                id, site, login = x.site_id, x.site, x.login
                                print(f"{Fore.GREEN}Id: {id}|Site: {site}|Login: {login}")
                            print()
                            input(Fore.GREEN + "Press to continue...")
                            os.system("clear")

                # List Id|Site|Login|Password
                case 3:
                    # Get key for decryption
                    with open(".key.txt", "r") as file:
                        key = file.read()

                    fernet = Fernet(key.encode())

                    stmt = select(Site).where(Site.user_id == user)
                
                    with Session(engine) as session:
                        os.system("clear")
                        result = session.scalars(stmt).all()

                        if not result:
                            os.system("clear")
                            print(Fore.RED + "You don't have any password yet")
                        else:
                            for x in result:
                                id, site, login, password = x.site_id, x.site, x.login, x.password
                                password = fernet.decrypt(password)
                                print(f"{Fore.GREEN}Id: {id}|Site: {site}|Login: {login}|Password: {password.decode()}")
                            
                            input(Fore.GREEN + "\nPress to continue...")
                            os.system("clear")
                # Change password (works by id)
                case 4:
                    # Prompt user for id of password
                    try:
                        id = int(input("Id: "))
                    except ValueError:
                        os.system("clear")
                        print(Fore.RED + "Invalid id")
                    else:
                        # Validate if it exists and it belongs to logged user | Remake with ORM
                        with Session(engine) as session, session.begin():
                            stmt = select(Site).where(Site.site_id == id, Site.user_id == user)
                            result = session.scalars(stmt).first()
                            if not result:
                                os.system("clear")
                                print(Fore.RED + "Password of this id doesn't exist")
                            # Update password
                            else:
                                print(Fore.GREEN + "\nChanging password " + result.site)
                                password = get_pass("site")
                                stmt = update(Site).where(Site.site_id == id, Site.user_id == user).values(password=password)
                                session.execute(stmt)
                                os.system("clear")
                                print(f"{Fore.GREEN}Password for {result.site} was changed")
                case 5:
                     # Prompt user for id of password
                    try:
                        id = int(input("Id: "))
                    except ValueError:
                        os.system("clear")
                        print(Fore.RED + "Invalid id")
                    else:
                        # Validate if it exists and it belongs to logged user | Remake with ORM
                        with Session(engine) as session, session.begin():
                            stmt = select(Site).where(Site.site_id == id, Site.user_id == user)
                            result = session.scalars(stmt).first()
                            if not result:
                                os.system("clear")
                                print(Fore.RED + "Password of this id doesn't exist")
                            # Delete password
                            else:
                                print()
                                stmt = delete(Site).where(Site.site_id == id, Site.user_id == user)
                                session.execute(stmt)
                                os.system("clear")
                                print(f"{Fore.GREEN}Password {result.site} was deleted")
                case 6:
                    user = None
                    os.system('clear')
                # Exit
                case 7:
                    print("Thanks for the usage bye! ~Vetus")
                    sys.exit(0)



# Register user
def register(username, password):
    stmt = insert(User).values(username=username, password_hash=sha256(password.encode('utf-8')).hexdigest())
    with Session(engine) as session, session.begin():
        session.execute(stmt) 

# Log user in
def log_user(username, password):
    stmt = select(User).where(User.username == username)
    password_check = sha256(password.encode('utf-8')).hexdigest()
    with Session(engine) as session, session.begin():
        result = session.scalars(stmt).first()
        print(result)
        if result:
            if password_check == result.password_hash:
                os.system("clear")
                return result.user_id
        os.system("clear")
        print(Fore.RED + "Wrong password")
        


# Menu tables
def table(type):
    match type:
        case "not_logged":
            table = Texttable()
            table.add_rows([
                ['Nr', 'Option'],
                ['1', 'Login'],
                ['2', 'Register'],
                ['3', 'Exit']
                ])
            return table
        case "logged":
            table = Texttable()
            table.add_rows([
                ['Nr', 'Option'],
                ['1', 'Add (app/site|login|password)'],
                ['2', 'List sites'],
                ['3', 'List sites with passes'],
                ['4', 'Change password'],
                ['5', 'Delete any passes by id from list'],
                ['6', 'Logout'],
                ['7', 'Exit']
                ])
            return table

# Generate encrypyion key
def generate_key():
    with open(".key.txt", "w") as file:
        key = Fernet.generate_key()
        file.write(key.decode())

# Get & Validate
def get_opt(max):
    while True:

        # Get input
        while True:
            try:
                option = int(input(Fore.GREEN + "Choose option: "))
                break
            except ValueError:
                print(Fore.RED + "\nMust be an integer")
        print()

        # Validate
        try:
            if 1 <= option <= max:
                return int(option)
            else: 
                print(Fore.RED + "Must be integer between 1 and "+str(max))
        except ValueError:
            print(Fore.RED + "Must be integer between 1 and "+str(max))

# Get and validate username
def get_username():
    while True:

        # Get username
        username = input(Fore.GREEN + "Username: ").strip()
        print()

        # Validate
        if 2 <= len(username) <= 15 and username.isalnum():
            return username
        else:
            print(Fore.RED + "Invalid username 2-15 characters, only letters and numbers\n")

def get_pass(type):
    match type:
        case "log":
            while True:
                try:
                    password = maskpass.askpass(prompt=f"{Fore.GREEN}Password: ")
                except KeyboardInterrupt:
                    print
                    sys.exit(0)

                if 8 <= len(password) <= 20 and not ' ' in password:
                    return password
                else:
                    print(Fore.RED + "\nInvalid password 8-20 characters\n")
        case "reg":
            while True:
                try:
                    password = maskpass.askpass(prompt=f"{Fore.GREEN}Password: ")
                except KeyboardInterrupt:
                    print()
                    sys.exit(0)

                if 8 <= len(password) <= 20 and not ' ' in password and password.isalnum():
                    while True:
                        password_check = maskpass.askpass(prompt=f"{Fore.GREEN}\nRetype password: ")
                        if password == password_check:
                            return password
                        else:
                            os.system('clear')
                            print(Fore.RED + "\nPasswords don't match\n")
                            return None
                else:
                    print(Fore.RED + "\nInvalid password 8-20 characters & no spaces/special characters\n")
        case "site":
            while True:
                try:
                    password = maskpass.askpass(prompt=f"{Fore.GREEN}Password: ")
                except KeyboardInterrupt:
                    sys.exit(0)

                if 8 <= len(password) <= 20 and not ' ' in password:
                    with open(".key.txt", "r") as file:
                        key = file.read()
                    fernet = Fernet(key.encode())
                    return fernet.encrypt(password.encode())
                else:
                    print(Fore.RED + "\nInvalid password 8-20 characters\n") 


def get_site(field):
    match field:
        case "site":
            while True:
                site = input(Fore.GREEN + "Site/App: ")
                print()
                if 3 <= len(site) <= 30:
                    if site.isalnum():
                        return site
                print(Fore.RED + "Invalid number of characters [3-30]/special characters")
        case "login":
            while True:
                login = input(Fore.GREEN + "login: ")
                print()
                if 3 <= len(login) <= 30:
                    if login.isalnum():
                        return login
                    print(Fore.RED + "Invalid number of characters [3-30]/special characters")

if __name__ == "__main__":
    main()