from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
import smtplib
import ssl


def show_popup(c, title):
    popupWindow = Popup(title=title, content=c(), size_hint=(.6, .4))
    popupWindow.open()

def ConnectServer(self):
	self.connection = MailServer(self.email, self.password)
	if not self.connection.connectServer():
		show_popup(ServerError, "Invalid Credentials")

class MailServer:
	port = 587
	
	def __init__(self, mail, password):
		self.mail = mail
		self.password = password

	def connectServer(self):
		self.smtp_server = "smtp-mail.outlook.com" if "outlook" in self.mail else "smtp.gmail.com" if "gmail" in self.mail else "smtp.libero.it" if "libero" in self.mail else "smtp.mail.yahoo.com" if "yahoo" in self.mail else ""
		self.context = ssl.create_default_context()
		self.server = smtplib.SMTP(self.smtp_server, self.port)
		if self.smtp_server:
			try:
				self.server.starttls(context=self.context)
				self.server.login(self.mail, self.password)
				return 1
			except:
				return 0
		return 0

	def sendMail(self, receiver, message, subject):
		fullmessage = "Subject: " + subject + "\n\n" + message
		try:
			self.server.sendmail(self.mail, receiver, fullmessage.encode("utf-8"))
			show_popup(Success, "Success!")
		except Exception as e:
			show_popup(SendError, "Error!")
			print(e)


class WindowManager(ScreenManager):
	pass

class LoginPanel(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def ConnectServer(self):
    	global server
    	server = MailServer(self.email.text, self.password.text)
    	if not server.connectServer():
    		show_popup(ServerError, "Invalid Credentials")
    		return 0
    	return server

class EmailPanel(Screen):
	receivermail = ObjectProperty(None)
	subject = ObjectProperty(None)
	message = ObjectProperty(None)

	def SendMail(self):
		server.sendMail(self.receivermail.text, self.message.text, self.subject.text)

class ServerError(FloatLayout):
    pass

class Success(FloatLayout):
	pass

class SendError(FloatLayout):
	pass

kv = Builder.load_file("design.kv")

class MyApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyApp().run()