# CS4389-Project

Bank Simulation

**************Folder Authentication*******************
[Categorization of files
app.py: main python file
bankuser.html, close.html, deposit.html, dfsdf.html, index.html, transfer.html, withdraw.html, profile.html: front-end html files for webpage
config.py: python file that contains passwords for database and system's email address that sends email for two factor authentication.
create_table.sql: MySQL file for creating necessary table for authentication
style.css, main.css, main.js, main2.js : CSS and JS files for supporting html pages]

Name of the file: app.py

Install Python if you don't have it 
$ sudo apt-get update
$ sudo apt-get install python3.6

Install flask :
python -m pip install flask

Install Flask-SQL extension to access MySQL database
pip install flask-mysql

Please update the username and password in config.py with your SQL accout (line 29 and 30)

Run the create_table.sql

How to run: python '.\Login Page\app.py'

follow the link obtained on the Terminal (Google chrome should work fine)


******* LOGIN PAGE ************

(1) to load login page go to Login/index.html to get the login page
(2) to get to accounts page click continue on the login page.
(3) to get to deposit select deposit button and cancel if don't want to deposit

Languages : HTML5, CSS3, JS and Frameworks (Bootstrap).


******* SIGNATURE ************

(1) to generate the public and private keys, run 'generateKeys.py'
(2) to sign a given file with the owner's private key and verifying the signature using owner's public key, run 'hashing.py'
(3) to verify if the owner's signature is valid or not, run 'verifySignature.py'
   - If you ever modify 'messageData' file, you need to perform step 2 and 3 again to verify owner's signature otherwise it will give you an exception message saying that the signature cannot be verified when you run 'verifySignature.py'

Languages : Python3
