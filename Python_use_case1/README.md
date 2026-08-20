Mini Banking System :
1.Login

After login:
1.Create Customer - Name, Phone, Email, Customer Id
2.Create Account - Customer ID, Account number, Balance, Type of the account
3.Deposit money - Date, amount, Transaction Number, account number, transacton type, remarks
4.Withdraw money
5.Transfer money
6.Account Statement
7.Search Transaction
8.Save Data
9.Logout

Steps - 

1, Create models models.py - Customer, Account and Transactions
2. Storage files for JSON - storage.py
3. Function(utilize) defined for Customer, Account and Transactions along with DATE STAMP - utils.py
4. Data struture in json - cretae Data folder and json formats file for authentication, transactions, customers ad accounts
5. Create Auth file to authorize the credential basically use Data/users.json to login and map the id and password for successful login
6. Define all features (step 1 to 7)) Create Coutomer, Create Account and Deposit, Withdraw, Tranfer Money along with Account statement and Search Transaction in bank.py
7. Create app main function file and add choice stage of all the features and call respectivily. 