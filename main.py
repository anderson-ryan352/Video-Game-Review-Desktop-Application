import customtkinter as ctk
import mysql.connector
from mysql.connector import errorcode


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


#Connects to mysql database with user input login info
def login():

	usr = accountEntry.get()
	pswd = passwordEntry.get()
	try:
		print("Connecting to database using mysql")
		cnx = mysql.connector.connect(user=usr,
										password=pswd,
										host='localhost',
										database='videogames')

		print("Succesfully Connected to database using MySQLdb!")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Invalid username or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:

		#Successful Connection Test Actions
		# prepare a cursor object using cursor() method
		cursor = cnx.cursor()

		# execute SQL query using execute() method.
		cursor.execute("SELECT VERSION()")

		# Fetch a single row using fetchone() method.
		data = cursor.fetchone()
		print("Database version : %s " % data)

		cursor.execute("SELECT * FROM gamelist")
		data = cursor.fetchone()
		print(data)

		cnx.close()





window = ctk.CTk()
window.title("Videogame Review App")
window.geometry("600x400")

frame = ctk.CTkFrame(master=window)
frame.pack(pady=20, padx=60, fill = "both", expand = True)


###########Login page###########

loginLabel = ctk.CTkLabel(master=frame, text = 'Login System', font=('calibre',30,'bold'))
loginLabel.pack(pady=12, padx=10)

accountEntry = ctk.CTkEntry(master=frame, placeholder_text = "Username", font=('calibre',10,'bold'))
accountEntry.pack(pady=12, padx=10)

passwordEntry = ctk.CTkEntry(master=frame, placeholder_text = "Password", font=('calibre',10,'bold'), show="*")
passwordEntry.pack(pady=12, padx=10)

loginButton = ctk.CTkButton(master=frame, text = "Login", command = login)
loginButton.pack(pady=12, padx=10)



#infinite window refresh
window.mainloop()


