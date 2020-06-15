# Author: Matthew Baker
# GitHub: https://github.com/mbaker92

# omxplayer filename

from time import sleep
import RPi.GPIO as gpio
import datetime
import subprocess
from tkinter import *
import time

gpio.setmode(gpio.BCM)

#Buttons Connected to GPIO Pins 17 and 18
gpio.setup(18, gpio.IN, pull_up_down=gpio.PUD_UP)

# Initialize Camera and Set Exposure Mode

#Ctrl + c in Terminal to Get Out of Infinite Loop	
while not True:
	
	#Get values from button presses
	inputCamera = gpio.input(18)

	# If The Camera Button is Pressed Take a Photo and Save With Current Date and Time
	if inputCamera == False:
	    print('Camera Button Pressed')
	    subprocess.run(["raspistill", "-o", "/home/pi/Documents/Hochzeitsfotos/" +  datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S') + ".png"])


rootWindow = Tk()
rootWindow.title('Tk Timer')
rootWindow.geometry("300x250")
rootWindow.resizable(0,0)
defaultColour = rootWindow.cget("bg")
time1 = ''
prevSec = ''
mins = 0
secs = 5
hours = 0
running = False
#clock = Label(rootWindow, font=('fixed', 20, 'bold'))
clock = Label(rootWindow, font=('fixed', 20))
clock.grid(row = 1, column = 2, padx = 5, pady = (5,2))

def tick():
    global prevSec, time1, secs, mins, hours, running
    # get the current local time from the PC
#    time2 = time.strftime('%Y/%m/%d %H:%M:%S')
    if running:
        newSec = time.strftime('%S')
    else:
        newSec = ''
        prevSec = ''
    if newSec != prevSec:
        prevSec = newSec
        secs = secs - 1
        if secs < 0:
            secs = 59
            mins = mins - 1
            if mins < 0:
                mins = 59
                hours = hours - 1
                if hours < 0: 
                    hours = 0
                    mins = 0
                    secs = 0
                    clock.config(bg='dark red')
    time2 = '%02d:%02d:%02d' % (hours, mins, secs)
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)
 
tick()

def start_btn():
    global running
    clock.config(bg='green')
    btn_start.config(state='disabled',background=defaultColour)
    btn_stop.config(state='normal',bg='dark red')
    btn_reset.config(state='disabled')
    running = True

def stop_btn():
    global running 
    clock.config(bg='dark red')
    btn_start.config(state='normal',bg='green')
    btn_stop.config(state='disabled',bg=defaultColour)
    btn_reset.config(state='normal')
    running = False

def reset_btn():
    global prevSec, time1, secs, mins, hours, running 
    clock.config(bg=defaultColour)
    hours = 2
    mins = 0
    secs = 0
    prevSec = ''
    time1 = ''
    running = False
    btn_stop.config(state='disabled',bg=defaultColour)
    btn_start.config(state='normal',bg='green')
    btn_reset.config(state='disabled')

btn_reset = Button(rootWindow, state='disabled', text = 'Reset', command = reset_btn)
btn_reset.grid(sticky=EW, row = 1, column = 3, padx = 5, pady = (5,2))
btn_start = Button(rootWindow, text = 'Start', bg='green', command = start_btn)
btn_start.grid(sticky=EW, row = 2, column = 3, padx = 5, pady = 2)
btn_stop = Button(rootWindow, state='disabled', text = 'Stop', command = stop_btn)
btn_stop.grid(sticky=EW, row = 3, column = 3, padx = 5, pady = (2,5))
btn_exit = Button(rootWindow, text = 'exit', command = exit)
btn_exit.grid(row = 4, column = 1, padx = 5, pady = 5) 

rootWindow.mainloop()
