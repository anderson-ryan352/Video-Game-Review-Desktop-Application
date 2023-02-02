import customtkinter as ctk
import mysql.connector
from mysql.connector import errorcode



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
	width = 600
	height = 400
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title("Video Game Review App")
		self.geometry(f"{self.width}x{self.height}")


		#SQL Connection vars
		self.cnx = None
		self.cursor = None


		#creating frame assigned to container
		container = ctk.CTkFrame(self, height = 400, width = 600)
		#frame region
		container.pack(side="top", fill="both", expand = True)

		#grid location
		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)


		#dictionary of frames
		self.frames = {}
		for F in (LoginPage, MainPage, SubmitNewGamePage, GameProfilePage):
			frame = F(container, self)

			self.frames[F] = frame
			frame.grid(row=0,column=0, sticky = "nsew")
		self.show_frame(LoginPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

	def getCnx(self):
		return self.cnx
	def setCnx(self, connection):
		self.cnx = connection
	def getCursor(self):
		return self.cursor
	def setCursor(self, crsr):
		self.cursor = crsr	


	




class LoginPage(ctk.CTkFrame):
	def __init__(self, parent, controller):
		ctk.CTkFrame.__init__(self, parent)
		self.pack(pady=20,padx=60, fill ="both", expand = True)

		self.loginLabel = ctk.CTkLabel(master=self, text = "Login System", font=('calibre',30,'bold'))
		self.loginLabel.pack(pady=12, padx=10)

		self.accountEntry = ctk.CTkEntry(master=self, placeholder_text = "Username", font=('calibre',10,'bold'))
		self.accountEntry.pack(pady=12, padx=10)

		self.passwordEntry = ctk.CTkEntry(master=self, placeholder_text = "Password", font=('calibre',10,'bold'), show="*")
		self.passwordEntry.pack(pady=12, padx=10)

		self.loginButton = ctk.CTkButton(master=self, text = "Login", command = lambda: self.loginEvent(controller, self.accountEntry.get(), self.passwordEntry.get()))
		self.loginButton.pack(pady=12, padx=10)


	def loginEvent(self,controller, account, pswd):
		try:
			print("Connecting to database using mysql")
			cnx = mysql.connector.connect(user=account,
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
			App.setCnx(controller, cnx)
			App.setCursor(controller, cnx.cursor())


			MainPage.loadMainPage(controller.frames[MainPage], controller)	








class MainPage(ctk.CTkFrame):
	def __init__(self, parent, controller):
		ctk.CTkFrame.__init__(self,parent)
		self.parent = parent
		label= ctk.CTkLabel(self,text="Main Page")
		label.grid(row = 0, column = 0)
		

		self.testVersion = ctk.CTkLabel(master = self, text = "", font = ('calibre',10,'bold'))
		self.testVersion.grid(row = 1, column = 0)

		self.gameProfileButton = ctk.CTkButton(self)



		submitNewGameButton = ctk.CTkButton(self,
										text = "Submit new game",
										command=lambda: App.show_frame(controller, SubmitNewGamePage),
										)
		submitNewGameButton.grid(row = 2, column = 0)

	def loadMainPage(self, controller):
		if App.getCnx(controller):
			
			#All game profile buttons destroyed so they can be refreshed in case any are deleted
			for widgets in self.winfo_children():
				if widgets == self.gameProfileButton:
					widgets.destroy()

			curs = App.getCursor(controller)
			curs.execute("SELECT VERSION()")

			dataVer = curs.fetchone()
			self.testVersion.configure(text= "Database Version: %s " % dataVer)

			curs.execute("SELECT * FROM gamelist")

			gameData = curs.fetchall()
			strText = []
			self.r, self.c = 0, 1
			for game in gameData:
				self.gameProfileButton = ctk.CTkButton(master = self,
												 text = game,
												 font = ('calibre',10,'bold'),
												 command= lambda game = game: GameProfilePage.loadGameProfilePage(controller.frames[GameProfilePage], controller, game))
				self.gameProfileButton.grid(row = self.r, column = self.c)

				self.r +=1
			App.show_frame(controller, MainPage)




class SubmitNewGamePage(ctk.CTkFrame):
	def __init__(self, parent, controller):
		ctk.CTkFrame.__init__(self, parent)
		self.parent = parent

		label = ctk.CTkLabel(self, text="Submit New Game")
		label.pack(padx=10, pady=10)


		self.gameNameEntry = ctk.CTkEntry(master = self, placeholder_text= "Game Name", font=('calibre',10,'bold'))
		self.gameNameEntry.pack(pady=12, padx=10)

		self.platformEntry = ctk.CTkEntry(master=self, placeholder_text="Platform",font=('calibre',10,'bold'))
		self.platformEntry.pack(pady=12,padx=10)

		self.releaseYearEntry = ctk.CTkEntry(master=self, placeholder_text="Release Year", font=('calibre',10,'bold'))
		self.releaseYearEntry.pack(pady=12,padx=10)

		submitButton = ctk.CTkButton(master = self, text = "Submit", command = lambda:self.addGameToDatabase(controller, self.gameNameEntry.get(), self.platformEntry.get(), self.releaseYearEntry.get()))
		submitButton.pack(pady=12, padx=10)

		backButton = ctk.CTkButton(
			self,
			text="Go to Main Page",
			command=lambda: App.show_frame(controller, MainPage),
		)
		backButton.pack(side="bottom", fill=ctk.X)


	def addGameToDatabase(self, controller, name, platform, releaseYear):
		if App.getCnx(controller):
			gameData = (name, platform, releaseYear)
			add_Game = ("INSERT INTO gamelist "
						"(name, platform, release_year) "
						"VALUES (%s, %s, %s)")
			try:
				curs = App.getCursor(controller)
				curs.execute(add_Game, gameData)
				controller.cnx.commit()

			except mysql.connector.Error as err:
				print(err)
			else:
				MainPage.loadMainPage(controller.frames[MainPage], controller)	
				App.show_frame(controller, MainPage)


class GameProfilePage(ctk.CTkFrame):
	def __init__(self, parent, controller):
		ctk.CTkFrame.__init__(self, parent)
		self.parent = parent

		self.gameTitleLabel = ctk.CTkLabel(master=self, text = "", font=('calibre',30,'bold'))
		self.gameTitleLabel.pack(pady=12, padx=10)

		self.platformLabel = ctk.CTkLabel(master=self, text = "", font=('calibre',30,'bold'))
		self.platformLabel.pack(pady=12, padx=10)

		self.releaseYearLabel = ctk.CTkLabel(master=self, text = "", font=('calibre',30,'bold'))
		self.releaseYearLabel.pack(pady=12, padx=10)

		self.gameIDLabel = ctk.CTkLabel(master=self, text = "", font=('calibre',30,'bold'))
		self.gameIDLabel.pack(pady=12, padx=10)


		#TODO
		#Add textbox for bio, label for review score, button for new review
		deleteGameButton = ctk.CTkButton(
			self,
			text = "DELETE",
			command=lambda: self.deleteGame(controller, self.gameIDLabel.cget("text"))
		)
		deleteGameButton.pack(side="bottom", fill = ctk.X)



		backButton = ctk.CTkButton(
			self,
			text="Go to Main Page",
			command=lambda: App.show_frame(controller, MainPage),
		)
		backButton.pack(side="bottom", fill=ctk.X)

	def deleteGame(self, controller, game):

		if App.getCnx(controller):
			remove_game = ("DELETE FROM gamelist WHERE id = %s")
			try:
				curs = App.getCursor(controller)
				curs.execute(remove_game, (game,))
				controller.cnx.commit()

			except mysql.connector.Error as err:
				print(err)
			else:
				MainPage.loadMainPage(controller.frames[MainPage], controller)
				App.show_frame(controller, MainPage)
				

	def loadGameProfilePage(self, controller, game):
		if App.getCnx(controller):
			self.gameTitleLabel.configure(text= (game[1],))
			self.platformLabel.configure(text = (game[3],))
			self.releaseYearLabel.configure(text = (game[4],))
			self.gameIDLabel.configure(text=game[0])
			#TODO
			#Fetch and configure game profile bio, reviews
			App.show_frame(controller, GameProfilePage)







if __name__ == "__main__":
	app = App()
	app.mainloop()


