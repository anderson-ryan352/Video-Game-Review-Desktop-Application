import customtkinter as ctk
import mysql.connector
from mysql.connector import errorcode


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
	width = 600
	height = 400
	cnx = None
	cursor = None
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

		self.homePage = None
		self.submitPage = None



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
			self.cursor = self.cnx.cursor()
			self.loginFrame.destroy()
			self.loadHomePage()

	#Connects to mysql database with user input login info
	def loadHomePage(self):

		self.homePage = ctk.CTkFrame(self)
		self.cursor.reset()

		self.width = 1000
		self.height = 600
		self.homePage.pack(pady=20, padx=60, fill = "both", expand = True)

		welcomeLabel = ctk.CTkLabel(master = self.homePage, text = "Welcome!", font = ('calibre',30,'bold'))
		welcomeLabel.pack(pady=12,padx=10)

		#Successful Connection Test Actions
		self.cursor.execute("SELECT VERSION()")
		data = self.cursor.fetchone()

		testVersion = ctk.CTkLabel(master=self.homePage, text = "Database Version: %s " % data, font = ('calibre',10,'bold'))
		testVersion.pack(pady=12, padx=10)

		#Displaying first game from database
		self.cursor.execute("SELECT * FROM gamelist")
		data = self.cursor.fetchone()

		testDataLabel = ctk.CTkLabel(master=self.homePage, text = data, font = ('calibre',10,'bold'))
		testDataLabel.pack(pady=12, padx=10)


		self.newGameButton = ctk.CTkButton(master=self.homePage, text = "Add Game", command = lambda:self.loadSubmitNewGame())
		self.newGameButton.pack(pady=12, padx=10)


	def loadSubmitNewGame(self):
		self.homePage.destroy()
		self.submitPage = ctk.CTkFrame(self)

		self.submitPage.pack(pady=20, padx=60, fill = "both", expand = True)

		label = ctk.CTkLabel(master = self.submitPage, text = "Add Game to Database")
		gameNameEntry = ctk.CTkEntry(master = self.submitPage, placeholder_text = "Game Name", font=('calibre',10,'bold'))
		gameNameEntry.pack(pady=12, padx=10)

		platformEntry = ctk.CTkEntry(master = self.submitPage, placeholder_text = "Platform", font=('calibre',10,'bold'))
		platformEntry.pack(pady=12, padx=10)

		releaseYearEntry = ctk.CTkEntry(master = self.submitPage, placeholder_text = "Release Year", font=('calibre',10,'bold'))
		releaseYearEntry.pack(pady=12, padx=10)

		submitButton = ctk.CTkButton(master = self.submitPage, text = "Submit", command = lambda:self.submitNewGame(gameNameEntry.get(), platformEntry.get(), releaseYearEntry.get()))
		submitButton.pack(pady=12, padx=10)


	def submitNewGame(self, name, platform, year):
			self.cursor.reset()
			gameData = (name, platform, year)
			add_Game = ("INSERT INTO gamelist "
						"(name, platform, release_year) "
						"VALUES (%s, %s, %s)")
			try:
				self.cursor.execute(add_Game, gameData)
				self.cnx.commit()

			except mysql.connector.Error as err:
				print(err)
			else:
				self.submitPage.destroy()
				self.loadHomePage()

	def clearWidgets(self, frame):
		for widget in frame.winfo_children():
			widget.destroy()


if __name__ == "__main__":
	app = App()
	app.mainloop()


