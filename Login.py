""""
Here start the program!!!
Once you encrypted the data all the numbers are going to be 
substitute by letter Z
"""""
import csv


def login():
    print("Welcome to the Encrypt data program!!!")
    ye_no = 1
    while ye_no == 1:
        login_ui = str(input("Already have an account? if not type 'N' (If already have one type any letter)\n"))
        if login_ui.upper() == "N":
            print("let's Create an Account! <3 "
                  "\n----------------------------------------------------------------------\n")
            from User_Interface import insert_info
            print("\nYour Account Is Ready!!! Log In to See your Info Encrypted :3\n")
            exit()
        else:
            csv_file2 = 'Data-information.csv'

            """Transform the data in dicts"""
            with open(csv_file2) as p:  # open de file to work with it
                reader2 = csv.DictReader(p)  # convert each row of the csv in a dictionary
                list_users = []

                """Put the data in a list"""
                for row in reader2:
                    list_users.append(row)  # add the dictionaries to a list

            print("Login to your Account to see your encrypt data! <3 "
                  "\n----------------------------------------------------------------------\n")

            user = input("Insert your username \n")
            this_user = []
            tries = 3
            for usernames in list_users:
                if user == "Admin01":
                    print("You are trying to log in to the Admin profile")
                    while tries != 0:
                        admin_pass = input("Insert your password \n")
                        if admin_pass == "124582":
                            print("\nHere is the original data of the users: \n")
                            print("---------------------------------------------------------------------------------\n")
                            with open(csv_file2) as p:  # open de file to work with it
                                reader2 = csv.DictReader(p)  # convert each row of the csv in a dictionary

                                """Put the data in a list"""
                                for row in reader2:
                                    print(row)
                            exit()
                        else:
                            print("Sorry the password is incorrect")
                            tries -= 1
                        if tries == 0:
                            print("You overpass your limit of tries!!! Byeeeeee")
                            exit()
                else:
                    if usernames['User-Name'] == user:
                        this_user.append(usernames)
                        ye_no = 3

                        while tries != 0:
                            user_pass = input("Insert your password \n")

                            if usernames['Password'] == user_pass:

                                csv_file2 = 'Encrypt-data.csv'

                                """Transform the data in dicts"""
                                with open(csv_file2) as p:  # open de file to work with it
                                    reader2 = csv.DictReader(p)  # convert each row of the csv in a dictionary
                                    encrypt_list = []

                                    """Put the data in a list"""
                                    for word in reader2:
                                        encrypt_list.append(word)  # add the dictionaries to a list

                                    for encrypted in encrypt_list:
                                        if encrypted['ID'] == usernames['ID']:
                                            new_dict = {key: value for (key, value) in encrypted.items() if key != "ID"}
                                            print("This is your info encrypted:\n")
                                            for item, thing in new_dict.items():
                                                print(item, ":", thing)
                                    print("\nThank you for use our service, See You Next Time!!!")
                                    exit()

                            else:
                                print("Sorry the password is incorrect")
                                tries -= 1
                        if tries == 0:
                            print("You overpass your limit of tries!!! Byeeeeee")
                            exit()
            else:
                print("Sorry this user doesn't exist\n")


login()
