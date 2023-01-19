import customtkinter as ctk
import mysql.connector
from mysql.connector import errorcode


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
	width = 600
	height = 400
	cnx = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title("Video Game Review App")
		self.geometry(f"{self.width}x{self.height}")


		################Login Frame############
		self.loginFrame = ctk.CTkFrame(self)
		self.loginFrame.pack(pady=20, padx=60, fill = "both", expand = True)


		self.loginLabel = ctk.CTkLabel(master=self.loginFrame, text = "Login System", font=('calibre',30,'bold'))
		self.loginLabel.pack(pady=12, padx=10)

		self.accountEntry = ctk.CTkEntry(master=self.loginFrame, placeholder_text = "Username", font=('calibre',10,'bold'))
		self.accountEntry.pack(pady=12, padx=10)

		self.passwordEntry = ctk.CTkEntry(master=self.loginFrame, placeholder_text = "Password", font=('calibre',10,'bold'), show="*")
		self.passwordEntry.pack(pady=12, padx=10)

		self.loginButton = ctk.CTkButton(master=self.loginFrame, text = "Login", command = self.loginEvent)
		self.loginButton.pack(pady=12, padx=10)



	########Login Event##################
	def loginEvent(self):

		usr = self.accountEntry.get()
		pswd = self.passwordEntry.get()
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
			self.cnx = cnx
			self.loginFrame.destroy()
			self.homePage()

	#Connects to mysql database with user input login info
	def homePage(self):
		self.width = 1000
		self.height = 600
		homePage = ctk.CTkFrame(self)
		homePage.pack(pady=20, padx=60, fill = "both", expand = True)

		welcomeLabel = ctk.CTkLabel(master = homePage, text = "Welcome!", font = ('calibre',30,'bold'))
		welcomeLabel.pack(pady=12,padx=10)
		#Successful Connection Test Actions
		# prepare a cursor object using cursor() method
		cursor = self.cnx.cursor()

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


		self.cnx.close()



if __name__ == "__main__":
	app = App()
	app.mainloop()


