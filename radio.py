import Tkinter as tk
import glob
import id3reader
import pygame
import time
import threading

music_folder = '/home/ryan/Music/'

playing = False
track = 0
paused = False
tracks = ()

pygame.mixer.init()
player = pygame.mixer.music

def watcher():
	global playing
	global track
	global paused
	global tracks
	global player
	while True:
		time.sleep(0.25)
		if playing:
			if not(player.get_busy()):
				if track < (len(tracks)-1):
					track += 1
					player.load(tracks[track])
					player.play()
				else:
					track = 0
					playing = False

w = threading.Thread(target=watcher)
w.setDaemon(True)

w.start()

root = tk.Tk()
root.geometry("320x240")
selector = tk.Frame(root)
selector.grid(row=0, column=0)

bands = tuple(sorted([(i.split('/'))[-1] for i in glob.glob(music_folder + '*')]))
bnames = tk.StringVar(value=bands)

yScroll = tk.Scrollbar(selector, orient=tk.VERTICAL)
yScroll.grid(row=1,column=1, sticky=tk.N+tk.S)

def select_album(evt):
	bPlay.config(state=tk.NORMAL)

lAlbums = tk.Listbox(selector, height=6, exportselection=False)
lAlbums.grid(column=2, row=1)
lAlbums.bind('<<ListboxSelect>>', select_album)

def select_band(evt):
	w = evt.widget
	index = int(w.curselection()[0])
	value = w.get(index)
	albums = tuple([(i.split('/'))[-1] for i in glob.glob(music_folder + value + '/*')])
	lAlbums.delete(0, 100)
	for i in albums:
		lAlbums.insert(tk.END, i) #tk.StringVar(value=songs))
	bPlay.config(state=tk.DISABLED)

lBands = tk.Listbox(selector, yscrollcommand=yScroll.set, listvariable=bnames, height=6, selectmode=tk.SINGLE, exportselection=False)
lBands.bind('<<ListboxSelect>>', select_band)
lBands.grid(column=0, row=1)
yScroll['command']=lBands.yview

def play_album():
	global playing
	playing = True
	global track
	track = 0
	global paused
	paused = False
	bandIndex = lBands.curselection()[0]
	bandValue = lBands.get(bandIndex)
	albumIndex = lAlbums.curselection()[0]
	albumValue = lAlbums.get(albumIndex)
	global tracks
	tracks = tuple([sorted(glob.glob(music_folder + bandValue + '/' + albumValue + '/*.mp3'),key=lambda i:int(id3reader.Reader(i).getValue('track').split('/')[0]))])[0]
	player.load(tracks[track])
	player.play()

bPlay = tk.Button(root, text='Play album', state=tk.DISABLED, command=play_album)
bPlay.grid(column=0, row=1)

controller = tk.Frame(root)
controller.grid(column=0, row=2)

def prev():
	global track
	global tracks
	if track > 0:
		track -=1
		player.load(tracks[track])
		player.play()

bPrev = tk.Button(controller, text='|<', command=prev)
bPrev.grid(column=0, row=0)

def play_pause():
	global track
	global tracks
	global playing
	global paused
	global player
	if playing:
		if paused:
			player.unpause()
		else:
			player.pause()
		paused = not(paused)
	else:
		track = 0
		playing = True
		player.load(tracks[track])
		player.play()

bPlayPause = tk.Button(controller, text='|| / >', command=play_pause)
bPlayPause.grid(column=1, row=0)

def next():
	global track
	global tracks
	if track < len(tracks):
		track += 1
		player.load(tracks[track])
		player.play()

bNext = tk.Button(controller, text='>|', command=next)
bNext.grid(column=2, row=0)

tk.mainloop()
