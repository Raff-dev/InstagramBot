from tkinter import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import sys
from random import *
from time import *
from threading import *



class GUI:
	def __init__(self):
		self.root = Tk()
		root = self.root
		root.iconbitmap('instabot.ico')
		root.winfo_toplevel().title("Imma Hooman")
		WIDTH = 300
		HEIGHT = 1

		minsize = Canvas(root, width=WIDTH, height=HEIGHT).pack()
		# ----------------------------------------------------
		# LOG IN FIELDS
		usernameText = Label(root, text='username').pack(side='top')
		self.usernameEntry = Entry(root, bg='grey')
		self.usernameEntry.pack(side='top')

		passwordText = Label(root, text='Password').pack(side='top')
		self.passwordEntry = Entry(root, bg='grey', show="*")
		self.passwordEntry.pack(side='top')


		# ----------------------------------------------------
		# CHOOSE IF VIA USERNAME OR FACEBOOK
		self.invalidEntyFlag = False # WAS WARNING ALREADYDISPLAYED
		self.isLoggingIn = False
		
		loginButton = Button(root, bg='#99ddff', text='Log In', command=self.createLogInThread).pack(side='top')

		loginMode = self.loginMode = StringVar()
		usernameRadio=Radiobutton(root, text="Username Login", variable=loginMode, value='username')
		usernameRadio.pack()		
		facebookRadio=Radiobutton(root, text="Facebook Login", variable=loginMode, value='facebook')
		facebookRadio.pack()
		usernameRadio.select()
		
		# ----------------------------------------------------
		# hashtags
		usernameText = Label(root, text='hashtags without #, devide by space').pack(side='top')
		self.hashtagsEntry = Entry(root, bg='grey')
		self.hashtagsEntry.pack(side='top')
		# ----------------------------------------------------
		# CHOOSE RUN MODE | l-like, o-follow
		runMode = self.runMode = StringVar()
		self.lModeRadio=Radiobutton(root, variable=runMode, command=lambda: self.toggleSpinner('l'), value="l", text="Like")
		self.lModeRadio.pack()
		self.fModeRadio=Radiobutton(root, variable=runMode, command=lambda: self.toggleSpinner('f'), value="f", text="follow").pack()
		self.lfModeRadio=Radiobutton(root, variable=runMode, command=lambda: self.toggleSpinner('lf'), value="lf", text="Like & follow").pack()
		self.lModeRadio.select()
		#followChanceEntry = Entry(root, bg='grey').pack()
		self.chanceValues = ['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%']
		self.followChanceSpinbox = Spinbox(root, state = DISABLED, value='0%')
		self.followChanceSpinbox.pack()

		# ----------------------------------------------------
		self.likesCount=0
		self.followsCount=0
		self.followingAtStart=0
		self.likesCountStringVar = StringVar()
		self.likesCountStringVar.set('Likes count: 0')	
		self.followsCountStringVar = StringVar()
		self.followsCountStringVar.set('Follows count: 0')		
		self.followingAtStartStringVar = StringVar()
		self.followingAtStartStringVar.set('Followed at start: 0')
		

		likeLabel = Label(root, textvariable=self.likesCountStringVar).pack(side='top')
		followLabel = Label(root, textvariable=self.followsCountStringVar).pack(side='top')
		followAtStartLabel = Label(root, textvariable=self.followingAtStartStringVar).pack(side='top')
		# ----------------------------------------------------
		self.isLoggedIn = False
		self.isRunning = False
		runButton = Button(root, text='Run',command=self.run).pack(side='top')
		stopButton = Button(root, text='Stop',command=self.stop).pack(side='top')
	# ----------------------------------------------------------------------------------
	# METHODS BELOW

	# ----------------------------------------------------------------------------------
	# GET INPUT VALUES | SET WAY OF LOGGING IN | RUN BOT LOGIN METHOD
	def createLogInThread(self):
		if self.isLoggingIn == False:
			if self.isLoggedIn == False:
				self.logInThread = Thread(target=self.logIn).start()
			else:
				print('Already logged in')
		else:
			print('Still logging in')

	def logIn(self):
			self.isLoggingIn = True
			# username = self.usernameEntry.get()
			# password = self.passwordEntry.get()
			username = 'justtestingmybot'
			password = 'tofen15541'
			text = 'Password or username is too short'
			invalidEntry = Label(self.root, text=text, fg='red')

			# CHECK IF INPUT IS CORRECT IF NOT PUT A RED SIGN
			if (len(password) < 6 or len(username) == 0):
				if self.invalidEntyFlag == False:			 
					invalidEntry.pack(side='top')
					self.invalidEntyFlag = True
					return
				else:
					return

			# INVOKE BOT LOGIN METHOD
			self.isLoggedIn = InstaBot.logIn(immaHooman, username, password, self.loginMode.get())
			if self.isLoggedIn == True:
				validEntry = Label(
					self.root, text='Logged in succesfully', fg='green').pack(side='top')
			else:
				invalidEntry = Label(
					self.root, text='Wrong username or password', fg='red').pack(side='top')
			self.isLoggingIn = False
			return
		
	def run(self):
		if self.isLoggedIn == True:
			if self.isRunning == False:
				print('Starting run method')
				self.isRunning = True
				self.runThread = Thread(target=InstaBot.run,args=[immaHooman,self.runMode.get()]).start()
			else:
				print('Bot is already running')		
		else:
			print('Not logged in')

	def getIsRunning(self):
		print('getIsRunning: ' +  str(self.isRunning))
		return self.isRunning

	def stop(self):
		if self.isRunning == True:
			self.isRunning = False
		else:
			print('Bot is not running')
			
	def gethashtags(self):
		# hashtags = self.hashtagsEntry.get().split()
		# if len(hashtags)==0:
		hashtags=("fitness","fit", "deadlift", "benchpress", "sbd","strong","powerliftingmotivation","wkteam","kfd" "polskadziewczyna", "polishgirl", "polishboy", "fitgirl", "fitboy", "training", "workout", "calistennics", "likeforlike", "squat", "powerlifter", "powerlifting", "weights", "warsaw", "warsawgirl","like4like")

		return hashtags

	def addCount(self, like, follow): 
		if like > 0:
			self.likesCount+=like
			self.likesCountStringVar.set('Likes count: ' + str(self.likesCount))
			print('Count of likes: '+ str(self.likesCount))
		if follow > 0:
			self.followsCount+=follow
			self.followsCountStringVar.set('Follows count: ' + str(self.followsCount))
			print('Count of newly followed: '+ str(self.followsCount))

	def setFollowingAtStart(self, count):
		self.followingAtStartStringVar.set('Followed at start: ' + str(count))
		return

	def toggleSpinner(self, mode):
		if mode == 'l':
			self.followChanceSpinbox.configure(state=DISABLED, value='0%')
		elif mode == 'f':
			self.followChanceSpinbox.configure(state=DISABLED, value='100%')
		elif mode == 'lf':
			self.followChanceSpinbox.configure(state=NORMAL,value=self.chanceValues)

	def shouldFollow(self):
		chance = self.followChanceSpinbox.get()
		chance = int(chance[:-1])
		return randint(0,100)<chance

class InstaBot:

	def __init__(self):
		self.url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'

	def logIn(self, username, password, loginMode):
		bot = self.bot = webdriver.Chrome("chromedriver.exe")
		bot.get(self.url)
		sleep(0.5)
		#FACEBOOK LOGIN
		if loginMode == 'facebook':
			facebookButton = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[6]/button'
			bot.find_element_by_xpath(facebookButton).click()
			sleep(0.5)
			bot.find_element_by_id('email').send_keys(username)
			bot.find_element_by_id('pass').send_keys(password)
			sleep(0.1)
			bot.find_element_by_name('login').click()
			sleep(0.5)
			try:
				bot.find_element_by_name('login')
			except NoSuchElementException:
				if self.checkPopUp():
					return True
			else:
				pass

		#USERNAME LOGIN
		elif loginMode == 'username':
			bot.find_element_by_name('username').send_keys(username)
			bot.find_element_by_name('password').send_keys(password)
			sleep(0.1)
			loginbuttonXpath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button'
			bot.find_element_by_xpath(loginbuttonXpath).click()
			sleep(0.5)
			try:
				bot.find_element_by_xpath('//*[@id="slfErrorAlert"]')
			except NoSuchElementException:
				if self.checkPopUp():
					return True
			else:
				pass
		else:
			print("No login mode selected")

		bot.close()
		return False

	def run(self, mode):

		while  Window.getIsRunning() == True:
			print('Bot run: ' + str(Window.getIsRunning()))

			if self.bot:
				print('Mode: \'' + mode + '\' selected')
				if mode =='f' or mode =='lf':
					self.getfollowingCount()
				sleep(1)
				bot = self.bot
				hashtags = GUI.gethashtags(Window)
				while Window.getIsRunning() == True:

					hashtag = choice(hashtags)
					links = self.getMostRecentLinks(hashtag)
					for link in links:
						if Window.getIsRunning() == True:
							bot.get(link)
							if mode == 'l':
								self.like()
							elif mode == 'f':
								self.follow()
							elif mode == 'lf':
								self.like()
								self.follow()
							else:
								print('No mode selected')
								return
						else:
							print('Stopped actions')
							return
					
			else:
				print('There is no bot')
				return
		return

	def getMostRecentLinks(self,hashtag):
		bot = self.bot
		bot.get('https://www.instagram.com/explore/tags/' + hashtag + '/')
		sleep(2)
		aElems = bot.find_elements_by_tag_name('a')
		allLinks=[]
		for aElem in aElems:
			allLink = aElem.get_attribute('href')
			if '/p/' in allLink:
				allLinks.append(allLink)
		#FILTER ONLY MOST RECENT
		mostRecentLinks=[]
		for i in range(9,len(allLinks)):
			mostRecentLinks.append(allLinks[i])

		return mostRecentLinks

	def getfollowingCount(self):
		bot=self.bot
		if bot.current_url != 'www.instagram.com':
			bot.get('https://www.instagram.com')
		sleep(1)
		profileXpath='//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[1]/a'
		try:
			self.profileLink = bot.find_element_by_xpath(profileXpath).get_attribute('href')
		except NoSuchElementException:
			try:
				sleep(1)
				self.profileLink = bot.find_element_by_xpath(profileXpath).get_attribute('href')
			except NoSuchElementException:
				print('Could not get profile link')
				return
		
		bot.get(self.profileLink)
		sleep(1)
		followingXpath = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
		try:
			followingCount = bot.find_element_by_xpath(followingXpath).get_attribute('textContent')
		except NoSuchElementException:
			try:
				sleep(1)
				followingCount = bot.find_element_by_xpath(followingXpath).get_attribute('textContent')
			except NoSuchElementException:
				print('Could not get following count')
				return
				
		followingCount = int(followingCount[:-10])
		Window.setFollowingAtStart(followingCount)
		print('Number of followed accounts: '+ str(followingCount))

	def like(self):
		bot = self.bot
		sleep(5)
		try:
			likeButtonXpath ='//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button'
			like = bot.find_element_by_xpath(likeButtonXpath)
		except NoSuchElementException:
			return
		Window.addCount(1,0)

	def follow(self):
		if Window.shouldFollow():
			bot = self.bot
			sleep(5)
			try:
				followButtonXpath = '//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[2]/button'
				follow = bot.find_element_by_xpath(followButtonXpath)
			except NoSuchElementException:
				return	
			Window.addCount(0,1)

	def checkPopUp(self):
		sleep(1)
		bot=self.bot
		try:
			popup='/html/body/div[3]/div/div/div[3]/button[2]'
			bot.find_element_by_xpath(popup).click()
		except NoSuchElementException:
			sleep(3)
			try:
				bot.find_element_by_xpath(popup).click()
			except NoSuchElementException:
				print('Connection too slow or something is wrong')
				return False
		return True

immaHooman = InstaBot()
Window = GUI()
Window.root.mainloop()
#---------TO DO----------#
# -wait time to like/follow and between functions
# -remove from followed after hiting target
# -basing on measured connection time set wait time
# -hide program to system tray
# -set follow limit
# -add comment
# -checkboxes instead of radio


