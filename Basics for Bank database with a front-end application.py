import sqlite3


def main():
# Connect to SQLite database
    conn = sqlite3.connect('bank.db')
    cur = conn.cursor()


    # Create users table, if it does not exist already
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                balance REAL)''')


    # Create transactions table, if it does not exist already
    cur.execute('''CREATE TABLE IF NOT EXISTS transactions
                (id INTEGER PRIMARY KEY,
                user_id INTEGER,
                type TEXT,
                amount REAL)''')


    # Users in system
    cur.execute("INSERT OR IGNORE INTO users (username, password, balance) VALUES ('Shanon', '1234', 2000)")
    cur.execute("INSERT OR IGNORE INTO users (username, password, balance) VALUES ('Jake', '5678', 2000)")


    # Commit changes
    conn.commit()


    # Authenticating user
    def authenticate(username, password):
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        return user


    # Checking balance and transactions
    def check_balance_and_transactions(user_id):
        cur.execute("SELECT * FROM transactions WHERE user_id=?", (user_id,))
        transactions = cur.fetchall()
        return transactions


    # Depositing money
    def deposit(user_id, amount):
        cur.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount, user_id))
        cur.execute("INSERT INTO transactions (user_id, type, amount) VALUES (?, 'deposit', ?)", (user_id, amount))
        conn.commit()
        return True


    # Withdrawing money
    def withdraw(user_id, amount):
        cur.execute("SELECT balance FROM users WHERE id=?", (user_id,))
        balance = cur.fetchone()[0]
        if balance >= amount:
            cur.execute("UPDATE users SET balance = balance - ? WHERE id=?", (amount, user_id))
            cur.execute("INSERT INTO transactions (user_id, type, amount) VALUES (?, 'withdrawal', ?)", (user_id, amount))
            conn.commit()
            return True
        else:
            return False


    # Find branches in a city
    def find_branches(city):
        # Branches
        branches = {
            'New York': ['210 ST', '59 Jackson Avenue'],
            'Boston': ['12 RedSocks Avenue', '90 ST'],
            'Atlanta': ['97 HipHop Avenue']
        }
        return branches.get(city, [])


    #User options
    while True:
        print("\nWelcome. Please enter your username and password")
        username = input("Enter username: ")
        password = input("Enter password: ")


        user = authenticate(username, password)
        if user:
            user_id = user[0]
            print("Welcome", username)
            while True:
                print("\nWhat would you like to do today?")
                print("1. Check balance and transactions")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Find a branch")
                print("5. Logout")


                choice = int(input("Option: "))


                if choice == 1:
                    transactions = check_balance_and_transactions(user_id)
                    print("Balance:", user[3])
                    print("Transaction History:")
                    for transaction in transactions:
                        print(transaction[4], "-", transaction[2], "-", transaction[3])


                elif choice == 2:
                    amount = float(input("Enter amount to deposit: "))
                    deposit(user_id, amount)
                    print("Deposit successful")


                elif choice == 3:
                    amount = float(input("Enter amount to withdraw: "))
                    if withdraw(user_id, amount):
                        print("Withdrawal successful")
                    else:
                        print("Insufficient funds")


                elif choice == 4:
                    city = input("Enter the city name: ")
                    branches = find_branches(city)
                    if branches:
                        print("Branches in", city + ":")
                        for branch in branches:
                            print(branch)
                    else:
                        print("No branches found in", city + ".")


                elif choice == 5:
                    print("Logout successful!")
                    break


                else:
                    print("Invalid choice. Please try again.")


            break


        else:
            print("Invalid username or password. Please try again.")


    # Close connection
        conn.close()


if __name__ == '__main__':


    main()
