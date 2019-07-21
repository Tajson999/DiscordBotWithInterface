import sys

# web library
import http.client
import ctypes
from functools import partial
from PIL import Image,ImageTk

import tkinter
import tkinter.font



def send(message):
    # your webhook URL
    webhookurl = "###"

    # compile the form data (BOUNDARY can be anything)
    formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------:::BOUNDARY:::--"

    # get the connection and make the request
    connection = http.client.HTTPSConnection("discordapp.com")
    connection.request("POST", webhookurl, formdata, {
        'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
        'cache-control': "no-cache",
    })

    # get the response
    response = connection.getresponse()
    result = response.read()

    # return back to the calling function with the result
    return result.decode("utf-8")

def close():
    send("!close")
    root.destroy()

def pause():
    send("!pause")

def resume():
    send("!resume")

def up():
    send("!up .05")

def down():
    send("!down .05")

def upHeigh():
    send("!up .30")

def downHeigh():
    send("!down .30")

def minimize():
    global window,win, is_down
    if not is_down:
        window.withdraw()
        is_down = True
    else:
        window = win
        window.wm_deiconify()
        is_down = False


#
# fix min styling DONE
# first row length at max DONE (added weird -7 att all row for some reason?)
# btn pics DONE
#
# See volume
# numer volume
#

width = [0]
rowElements = [0]
currentRow = 0
frames = []

pausePicPath = "pause_white.png"
playPicPath = "white_play.png"

root = tkinter.Tk()
root.attributes('-alpha', 0.0)
root.iconify()

background = tkinter.Toplevel(root)
background.geometry("20x28")
background.overrideredirect(1) #Remove border
background.attributes('-alpha', 1)
background.resizable(0,500)
background.configure(background='#2c2f33')
background.attributes("-topmost", True)

min = tkinter.Button(background, text = "__", command = minimize,background="#2c2f33",fg='white')
min.img = tkinter.PhotoImage()
min.config(height=23, image=min.img, compound=tkinter.LEFT)
min.pack(side=tkinter.LEFT, fill=tkinter.Y)

window = tkinter.Toplevel(root)
win = window
is_down = False

user32 = ctypes.windll.user32
screenlength = user32.GetSystemMetrics(0)
print(screenlength)
window.geometry(str(screenlength)+"x28") #Whatever size
window.overrideredirect(1) #Remove border
window.attributes('-alpha', 1)
window.configure(background='#2c2f33')
#staying at top level
window.attributes("-topmost", True)
#window.attributes('-topmost', 1)
#Whatever buttons, etc
frames.append(tkinter.Frame(window,height=1,width=screenlength,background="#2c2f33"))

min2 = tkinter.Button(frames[0], text = "__", command = minimize,background="#2c2f33",fg='white')
min2.img = tkinter.PhotoImage()
min2.config(height=20, image=min2.img, compound=tkinter.LEFT)
min2.pack(side=tkinter.LEFT,fill=tkinter.Y)

close = tkinter.Button(frames[0], text = "X", command = close, background="#2c2f33", fg='white', font='Times 14 bold')
close.img = tkinter.PhotoImage()
close.config(height=20, image=close.img, compound=tkinter.LEFT)
#close.grid(row=0,column=0,sticky="W E N S")
close.pack(side=tkinter.LEFT, fill=tkinter.Y)


pausePic = Image.open(pausePicPath)
pausePic = pausePic.resize((22,22),Image.ANTIALIAS)
pausePicTk = ImageTk.PhotoImage(pausePic)
pause = tkinter.Button(frames[0], command = pause,  background="#2c2f33",image=pausePicTk)
pause.pack(side=tkinter.LEFT, fill=tkinter.Y)

playPic = Image.open(playPicPath)
playPic = playPic.resize((22,22),Image.ANTIALIAS)
playPicTk = ImageTk.PhotoImage(playPic)
resume = tkinter.Button(frames[0], command = resume, background="#2c2f33", image=playPicTk)
resume.pack(side=tkinter.LEFT)

volFrameHeigh = tkinter.Frame(frames[0],background="#2c2f33")

volUpH = tkinter.Button(volFrameHeigh, text = "++", command = upHeigh, background="#2c2f33", fg='white', font='Times 14 bold')
volUpH.img = tkinter.PhotoImage()
volUpH.config(height=6, image=volUpH.img, compound=tkinter.LEFT)
#volUp.grid(row=0,column=4,sticky="W E N S")
volUpH.pack(side=tkinter.TOP)

volDownH = tkinter.Button(volFrameHeigh, text = "––", command = downHeigh, background="#2c2f33", fg='white', font='Times 14 bold')
volDownH.img = tkinter.PhotoImage()
volDownH.config(height=6, image=volDownH.img, compound=tkinter.LEFT)
#volDown.grid(row=0,column=3,sticky="W E N S")
volDownH.pack(side=tkinter.TOP)

volFrameHeigh.pack(side=tkinter.LEFT)
volFrameHeigh.update()


volFrameLow = tkinter.Frame(frames[0],background="#2c2f33")

volUp = tkinter.Button(volFrameLow, text = "+", command = up, background="#2c2f33", fg='white', font='Times 14 bold')
volUp.img = tkinter.PhotoImage()
volUp.config(height=6, image=volUp.img, compound=tkinter.LEFT)
#volUp.grid(row=0,column=4,sticky="W E N S")
volUp.pack(side=tkinter.TOP)

volDown = tkinter.Button(volFrameLow, text = "–", command = down, background="#2c2f33", fg='white', font='Times 14 bold')
volDown.img = tkinter.PhotoImage()
volDown.config(height=6, image=volDown.img, compound=tkinter.LEFT)
#volDown.grid(row=0,column=3,sticky="W E N S")
volDown.pack(side=tkinter.TOP)

volFrameLow.pack(side=tkinter.LEFT)
volFrameLow.update()

frames[0].grid(row=0,sticky='NW')

window.update()
width[0] += min2.winfo_width()
width[0] += close.winfo_width()
width[0] += pause.winfo_width()
width[0] += resume.winfo_width()
width[0] += volFrameHeigh.winfo_width()
width[0] += volFrameLow.winfo_width()
rowElements[0] = 6
print("util width = " +  str(width[0]))


file = open("buttons.txt", "r")
buttons = []
for line in file:
    if not line[0] == "#":
        #getting name and link
        split = line.find("|")
        name = line[:split]
        url = line[split+1:]
        if( name[0] == '2'):
            name = name[1:]
            #print("seccod")
        #print(name)
        #print(url)
        shouldFillX = 0
        #creating buton to get width
        buttons.append(tkinter.Button(frames[currentRow], text = name, command = partial(send, "!yt " + url), background="#2c2f33", fg='white', font='Times 14 bold'))
        buttons[len(buttons) - 1].img = tkinter.PhotoImage()
        buttons[len(buttons) - 1].config(height=20, image=buttons[len(buttons) - 1].img, compound=tkinter.LEFT)
        buttons[len(buttons) - 1].pack(side=tkinter.LEFT,fill=tkinter.Y)
        window.update()
        frames[currentRow].update()
        curButWidth = buttons[len(buttons) - 1].winfo_width()
        #got width removing button
        buttons[len(buttons)-1].pack_forget()
        #checking if new row is needed
        if width[currentRow] + curButWidth > screenlength:
            width.append(0)
            frames.append(tkinter.Frame(window,width=screenlength,background="#2c2f33"))
            currentRow += 1
            print("added new row. currently on row" + str(currentRow))
            frames[currentRow].grid(row=currentRow,sticky='NW')
            window.geometry(str(screenlength)+"x"+str(28+currentRow*28))
            shouldFillX = 1
        #add button to correct row
        buttons[len(buttons) - 1] = tkinter.Button(frames[currentRow], text = name, command = partial(send, "!yt " + url), background="#2c2f33", fg='white', font='Times 14 bold')
        buttons[len(buttons) - 1].img = tkinter.PhotoImage()
        buttons[len(buttons) - 1].config(height=20, image=buttons[len(buttons) - 1].img, compound=tkinter.LEFT)
        #makine last button on last row fill out the row
        if shouldFillX:
            fillSize = screenlength - width[currentRow - 1] + buttons[len(buttons) - 2].winfo_width() - 7
            buttons[len(buttons) - 2].config(width=fillSize)
            shouldFillX = 0
        #added new button and added width
        buttons[len(buttons) - 1].pack(side=tkinter.LEFT, fill=tkinter.Y)
        width[currentRow] += curButWidth


        #buttons[len(buttons)-1].pack(side=tkinter.LEFT, fill=tkinter.Y)
    #print(line)

root.mainloop()
