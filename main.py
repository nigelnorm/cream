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
                createAccount("c")
            elif(num == 2):
                customer("c",0)
            elif(num==3):
                admin()
def createAccount(type):
    if(type == "c"):
        name = input("Name: ")
        pin = int(input("New Pin: "))
        mycursor.execute("INSERT INTO Customer (pin, name, balance) VALUES(%s,%s,%s)",(pin,name,1002))
        db.commit()
        mycursor.execute("select accountID from Customer ORDER BY accountID DESC LIMIT 1;")
        for x in mycursor:
            print("Hello " + name + " your \"randomly\" generated account ID is:  " + str(x[0]))
        print("\nStarting Balance: $100\n")
        print("Would you like to perform operations using this account(Y/N)")
    if(type == "a"):
        name = input("Name: ")
        ids = input("Unique Admin ID: ")
        pin = int(input("New Pin: "))
        mycursor.execute("INSERT INTO Admin (pin, name, adminID) VALUES(%s,%s,%s)",(pin,name,ids))
        db.commit()
        mycursor.execute("select adminID from Customer ORDER BY adminID DESC LIMIT 1;")
        for x in mycursor:
            print("Hello " + name + " your adminID is:  " + str(x[0]))
        print("Would you like to perform operations using this account(Y/N)")
        

# THIS IS FOR CUSTOMER STUFF
def customer(type, accNum):
    if(type == "c"):
        accNum = login("c")
    while(True):
        os.system('cls')
        print("What would you like to do?")
        print("1. Withdraw Money")
        print("2. Deposit Money")
        print("3. Transfer Money")
        print("4. View Current Balance")
        print("5. Modify Account")
        print("6. Log Out")
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
            changeInfo("c", accNum)
        elif(choice == 6):
            break
        db.commit()

def login(type):
    if(type =="c"):
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
            mycursor.execute("SELECT adminID FROM Admin WHERE adminID = %s AND pin = %s", (accountID, pin))
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


    return
# --------------------------
#THIS IS FOR ADMIN FUNCTIONS
# --------------------------
def admin():
    acc = login("a")
    while(True):
        os.system('cls')
        print("What would you like to do?\n")
        print("1. Create an Account")
        print("2. Delete an Account")
        print("3. Change a Customer's Account Values")
        print("4. Change Your Account Values\n")
        print("5. Log Out")
        choice = int(input("Enter in your choice number: "))
        os.system('cls')
        if (choice == 1):
            createAccount("a")
        elif (choice == 2):
            deleteAccount("", acc)
        elif (choice == 3):
            print("Changing Customer Info \n")
            changeInfo("c",int(input("Input their customerID: ")))
        elif(choice == 4):
            changeInfo("a", acc)
        elif(choice== 5):
            break
    

def deleteAccount(type, acc):
    if(type == "c"):
        sure = input("Are you sure (Y/N)")
        if(sure == 'Y'):
            mycursor.execute("DELETE FROM Customer WHERE accountID = %s" ,[acc])
            db.commit()
            print("Your account has been deleted")
            return
    else:
        print("Admin Deletion \n")
        print("1. Delete Customer Account")
        print("2. Delete Your Own Account")
        print("3. Back")
        
        choice = int(input("Enter in your choice number: "))
        if (choice == 1):
            custNum = int(input("Choose Customer Account Number: "))
            deleteAccount("c", custNum)
        elif (choice == 2):
            sure = input("Are you sure (Y/N)")
            if(sure == 'Y'):
                mycursor.execute("DELETE FROM Admin WHERE adminId = %s", [acc])
                db.commit()
                print("Your account has been deleted")
            else:
                deleteAccount(type,acc)
        elif (choice == 3):
            return
    return

def changeInfo(type, accNum):
    while(True):
        os.system('cls')
        if(type == "c"):
            print("Customer Profile Change")
        else:
            print("Admin Profile Change")
        print("1. Edit Name")
        print("2. Edit PIN")
        print("3. Back")
        choice = int(input("Please pick a number: "))

        if choice == 1:
            custName = input("/n New Name: ")
            if(type == "c"):
                mycursor.execute("UPDATE Admin SET name = %s WHERE adminID = %s", (custName, accNum))
            else:
                mycursor.execute("UPDATE Admin SET name = %s WHERE adminID = %s", (custName, accNum))
            
        elif choice == 2:
            PIN = int(input("New Pin:"))
            if(type == "c"):
                mycursor.execute("UPDATE Admin SET pin = %s WHERE adminID = %s", (PIN, accNum))
            else:
                mycursor.execute("UPDATE Admin SET pin = %s WHERE adminID = %s", (PIN, accNum))
        elif choice == 3:
            return
        db.commit()

    



if __name__ == "__main__":
    main()
    
