from tkinter import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import sys
from random import *
from time import *
from threading import *

class InstaBot:

	def __init__(self):
		self.unfollowCount=0
		self.url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'

	def logIn(self):
		username = 'justtestingmybot'
		password = 'tofen15541'
		bot = self.bot = webdriver.Chrome("chromedriver.exe")
		bot.get(self.url)
		sleep(0.5)
		bot.find_element_by_name('username').send_keys(username)
		bot.find_element_by_name('password').send_keys(password)
		sleep(0.1)
		loginbuttonXpath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button'
		bot.find_element_by_xpath(loginbuttonXpath).click()
		sleep(0.5)


	def closePopUp(self):
		sleep(1)
		bot=self.bot
		try:
			popup='/html/body/div[3]/div/div/div[3]/button[2]'
			bot.find_element_by_xpath(popup).click()
		except NoSuchElementException:
			pass

	def openFollowingWindow(self):
		bot=self.bot
		sleep(1)
		profileXpath='//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[1]/a'
		try:
			profileLink = bot.find_element_by_xpath(profileXpath).get_attribute('href')
		except NoSuchElementException:
			sleep(1)
			profileLink= bot.find_element_by_xpath(profileXpath).get_attribute('href')
		
		while True:
			bot.get(profileLink)
			sleep(1)
			flollowingbutton ='//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
			bot.find_element_by_xpath(flollowingbutton).click()
			sleep(0.5)
			followingButtons=[]
			buttons=bot.find_elements_by_tag_name('button')
			print(len(buttons))
			if len(buttons)==0:
				return
			for button in buttons:
				if (button.get_attribute('textContent')=='Following'):
					followingButtons.append(button)
			for followingButton in followingButtons:
				try:
					
					followingButton.click()
					sleep(1)
					unfollow=bot.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[1]').click()
					sleep(1)
				except Exception:
					break
				self.unfollowCount+=1	
				print(self.unfollowCount)
			sleep(2)
		print('finished')
		return
			


		



immaHooman = InstaBot()
immaHooman.logIn()
immaHooman.openFollowingWindow()
