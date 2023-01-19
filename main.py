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

		#Successful Connection
		homePage(cnx)



def homePage(cnx):
		loginFrame.destroy()
		window.geometry("1000x600")
		homePage = ctk.CTkFrame(master=window)
		homePage.pack(pady=20, padx=60, fill = "both", expand = True)

		welcomeLabel = ctk.CTkLabel(master = homePage, text = "Welcome!", font = ('calibre',30,'bold'))
		welcomeLabel.pack(pady=12,padx=10)
		#Successful Connection Test Actions
		# prepare a cursor object using cursor() method
		cursor = cnx.cursor()

		# execute SQL query using execute() method.
		cursor.execute("SELECT VERSION()")

		# Fetch a single row using fetchone() method.
		data = cursor.fetchone()

		testVersion = ctk.CTkLabel(master=homePage, text = "Database Version: %s " % data, font = ('calibre',10,'bold'))
		testVersion.pack(pady=12, padx=10)


		cursor.execute("SELECT * FROM gamelist")
		data = cursor.fetchone()

		testDataLabel = ctk.CTkLabel(master=homePage, text = data, font = ('calibre',10,'bold'))
		testDataLabel.pack(pady=12, padx=10)


		cnx.close()
		homePage.mainloop()


###########Login page###########

window = ctk.CTk()
window.title("Video Game Review App")
window.geometry("600x400")

loginFrame = ctk.CTkFrame(master=window)
loginFrame.pack(pady=20, padx=60, fill = "both", expand = True)


loginLabel = ctk.CTkLabel(master=loginFrame, text = "Login System", font=('calibre',30,'bold'))
loginLabel.pack(pady=12, padx=10)

accountEntry = ctk.CTkEntry(master=loginFrame, placeholder_text = "Username", font=('calibre',10,'bold'))
accountEntry.pack(pady=12, padx=10)

passwordEntry = ctk.CTkEntry(master=loginFrame, placeholder_text = "Password", font=('calibre',10,'bold'), show="*")
passwordEntry.pack(pady=12, padx=10)

loginButton = ctk.CTkButton(master=loginFrame, text = "Login", command = login)
loginButton.pack(pady=12, padx=10)


#infinite window refresh
window.mainloop()


