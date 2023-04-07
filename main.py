import mysql.connector 
import os


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql123",
    database="bank"
)

mycursor = db.cursor()
running = True
def main():
    while(running):
            print("1. Create Customer Account")
            print("2. Login with Existing Accont")
            print("3. Login as an ADMINISTRATOR")
            print("4. Exit Banking System")
            num = int(input("Input a number that marks your choice: "))
            if(num == 1):
                os.system('cls')
                createAccount()
            elif(num == 2):
                customer()
            elif(num==3):
                admin()
mycursor.execute("CREATE TABLE Admin (adminID int UNSIGNED PRIMARY KEY, pin int UNSIGNED NOT NULL, name VARCHAR(50) NOT NULL")
def createAccount():
    name = input("Name: ")
    pin = int(input("New Pin: "))
    mycursor.execute("INSERT INTO Customer (pin, name, balance) VALUES(%s,%s,%s)",(pin,name,1002))
    db.commit()
    mycursor.execute("select accountID from Customer ORDER BY accountID DESC LIMIT 1;")
    for x in mycursor:
        print("Hello " + name + " your \"randomly\" generated account ID is:  " + str(x))
    print("\nStarting Balance: $100\n")
    print("Would you like to perform operations using this account(Y/N)")

# THIS IS FOR CUSTOMER STUFF
def customer():
    accNum = login("c")
    while(True):
        os.system('cls')
        print("What would you like to do?")
        print("1. Withdraw Money")
        print("2. Deposit Money")
        print("3. Transfer Money")
        print("4. View Current Balance")
        print("5. Log Out")
        choice = int(input("Pick an number to continue..."))
        os.system('cls')
        if(choice == 1):
            withdraw(accNum)
        elif(choice == 2):
            deposit(accNum)
        elif(choice == 3):
            transfer(accNum)
        elif(choice == 4):
            view(accNum)
            hello = input("Enter something to continue..")
        elif(choice == 5):
            break
        db.commit()

def login(type):
    if(type.equals("c")):
        while(True):
            os.system('cls')
            print("Login to your customer account.")
            accountID = int(input("AccountID: "))
            pin = int(input("PIN: "))
            mycursor = db.cursor()
            mycursor.execute("SELECT accountID FROM Customer WHERE accountID = %s AND pin = %s", (accountID, pin))
            account = mycursor.fetchall()
            for row in account:
                if row[0] == None:
                    print("Incorrect AccountID or PIN. Please Try again.")
                    con = input("Do you want to try again(y/n)?")
                    if con == 'y':
                        continue
                    else:
                        break
                else:
                    return row[0]
    else:
        while(True):
            os.system('cls')
            print("Login to your admin account.")
            accountID = int(input("Admin ID: "))
            pin = int(input("PIN: "))
            mycursor = db.cursor()
            mycursor.execute("SELECT accountID FROM Admin WHERE adminID = %s AND pin = %s", (accountID, pin))
            account = mycursor.fetchall()
            for row in account:
                if row[0] == None:
                    print("Incorrect AdminID or PIN. Please Try again.")
                    con = input("Do you want to try again(y/n)?")
                    if con == 'y':
                        continue
                    else:
                        break
                else:
                    return row[0]
    
def view(acc):
    mycursor.execute("SELECT balance FROM Customer WHERE accountId = %s", [acc]
                     )
    balance = mycursor.fetchall()
    for row in balance:
        print("Current Balance:  " + str(row[0]))
        print()
        return row[0]
def withdraw(acc):
    curbal = view(acc)
    while(True):
        withdraw =int(input("How much do you want to withdraw?"))
        if curbal < withdraw:
            print("Withdrawl is more than curent balance. Select another amount.")
        else:
            break
    
    mycursor.execute("UPDATE Customer SET balance = %s WHERE accountId = %s", (curbal-withdraw, acc))
def deposit(acc):
    curbal = view(acc)
    deposit =int(input("How much do you want to deposit?"))
    mycursor.execute("UPDATE Customer SET balance = %s WHERE accountId = %s", (curbal+deposit, acc))
def transfer(acc):
    curbal = view(acc)
    while(True):
        transfer =int(input("How much do you want to transfer?"))
        if curbal < transfer:
            print("Withdrawl is more than curent balance. Select another amount.")
        else:
            break
    otherAcc = int(input("What account do you want to send money too(accountNumber)?"))
    mycursor.execute("UPDATE Customer SET balance = %s WHERE accountId = %s", ((curbal-transfer), acc))
    mycursor.execute("SELECT balance FROM Customer WHERE accountID = %s", [otherAcc])
    for row in mycursor.fetchall():
        otherBal = row[0]
    mycursor.execute("UPDATE Customer SET balance = %s WHERE accountId = %s", ((otherBal+transfer), otherAcc))
# Deletion of account for Customers
def custDelete(acc):

    return
# --------------------------
#THIS IS FOR ADMIN FUNCTIONS
# --------------------------
def admin():
    acc = login("a")
    os.system('cls')
    print("What would you like to do?\n")
    print("1. Create an Account")
    print("2. Delete an Account")
    print("3. Change a Customer's Account Values")
    print("4. Change Your Account Values\n")
    print("5. Log Out")
    choice = int(input("Enter in your choice number: "))

    if (choice == 1):
        createAccount("a", acc)
    elif (choice == 2):
        deleteAccount("a",acc)
    elif (choice == 3):
        changeCustInfo()
    elif(choice == 4):
        changeOwnInfo()
    elif(choice== 5):
        return
    

def deleteAccount():
    return
def changeCustInfo(cust):
    return
def changeOwnInfo(acc):
    return\
    



if __name__ == "__main__":
    main()
    
