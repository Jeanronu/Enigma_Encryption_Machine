""""This file is the user interface!"""""
import csv


def data_input() -> dict:
    info = {}

    Id = 1
    with open("Data-information.csv") as f:
        reader = csv.reader(f, delimiter=',', skipinitialspace=True)
        ids = []
        for line in reader:
            if line[0] not in ids:
                ids.append(line[0])
    for number in range(len(ids[:-1])):
        ids[number + 1] = int(number + 1)
    max_id = max(ids[1::])
    Id = max_id + 1
    info['ID'] = Id

    name = ""
    while name == "":  # this part star the while loop
        name = str(input("Insert your Name \n"))
        if name == "":
            print("Sorry you have to enter your name")
    info['Name'] = name

    last_name = ""
    while last_name == "":  # this part star the while loop
        last_name = str(input("Insert your Last Name \n"))
        if last_name == "":
            print("Sorry you have to enter your Last name")
    info['Last Name'] = last_name

    # Birthdate
    print("Please insert your Birthdate")

    year = int(input('Enter a year: \n'))
    while year < 1922 or year > 2022:
        print("Sorry you could not be born in this year")
        year = int(input('Enter a valid birth year: \n'))

    month = int(input('Enter a month: \n'))
    while month < 1 or month > 12:
        print("Sorry this month does not exist")
        month = int(input('Enter a valid month: \n'))

    day = -2
    while day <= 0 or day > 31:
        day = int(input('Enter a day: \n'))
        if month == 2 and day > 29:
            print("Sorry February does not have 30 or 31 day")
        elif month == 4 or month == 6 or month == 9 or month == 11:
            if day <= 0 or day > 30:
                print("Sorry days not go after 30 in the", month, "th month")
        elif day <= 0 or day > 31:
            print("Remember days go from 1-31")

    birthdate = (year, month, day)
    info['Birthdate'] = birthdate

    # Address
    direction = ""
    while direction == "":  # this part star the while loop
        direction = str(input("Insert your direction ( eg. 370 Lancaster Ave ) \n"))
        if direction == "":
            print("Sorry you have to fill this field")
    city = ""
    while city == "":  # this part star the while loop
        city = str(input("Insert your city ( eg. Haverford ) \n"))
        if city == "":
            print("Sorry you have to fill this field")
    state = ""
    while state == "":  # this part star the while loop
        state = str(input("Insert your state ( eg. PA ) \n"))
        if state == "":
            print("Sorry you have to fill this field")
    zip_code = "1"
    while len(zip_code) != 5:  # this part star the while loop
        zip_code = int(input("Insert Zip-code ( eg. 19041 ) \n"))
        zip_code = str(zip_code)
        if len(zip_code) != 5:
            print("Sorry you have to fill this field (Zip-codes are 5 digits long)")
    address = (direction, city, state, zip_code)
    info['Address'] = address

    # LOGIN ACCOUNT
    username = ""
    while username == "":  # this part star the while loop
        username = input("Create your username \n")
        if username == "":
            print("Sorry you have to enter your name")

    exist = "a"
    with open("Data-information.csv") as f:
        reader = csv.reader(f, delimiter=',', skipinitialspace=True)
        users = []
        for row in reader:
            if row[4] not in users:
                users.append(row[4])

    while exist == "a":
        if username in users:
            print("Username already exist try other one")
            username = input("Create another username \n")
        else:
            exist = "l"

    info['User-Name'] = username

    password = "1"
    while len(password) < 5:  # this part star the while loop
        password = str(input("Insert Create Password \n"))
        if len(password) < 5:
            print("Sorry your password have to be greater than 5 long")
    info['Password'] = password

    """Encrypt the data"""

    from Enigma_Encryption import ENIGMA
    with open("Encrypt-data.csv", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        Id = str(Id) + ", "
        file_object.write(Id)
        already_in = [Id]
        to_encrypt = [name.upper(), last_name.upper(), direction.upper(), password.upper()]
        for item in to_encrypt:
            cipher_text = ""
            for letter in item:
                if letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                    cipher_text = cipher_text + ENIGMA.encipher(letter)
                else:
                    cipher_text = cipher_text + letter
            if item != password.upper():
                cipher_text = cipher_text + ", "
            if cipher_text not in already_in:
                file_object.write(cipher_text)
                already_in.append(cipher_text)
            else:
                hi = 0

    return info


def insert_info():
    from csv import DictWriter
    # list of column names
    field_names = ['ID', 'Name', 'Last Name', 'Birthdate', 'Address', 'User-Name', 'Password']
    # Dictionary that we want to add as a new row
    dicti = data_input()
    # Open CSV file in append mode
    # Create a file object for this file
    with open('Data-information.csv', 'a') as f_object:
        # Pass the file object and a list
        # of column names to DictWriter()
        # You will get an object of DictWriter
        dict_writer_object = DictWriter(f_object, fieldnames=field_names)
        # Pass the dictionary as an argument to the Writerow()
        dict_writer_object.writerow(dicti)
        # Close the file object
        f_object.close()


insert_info()
