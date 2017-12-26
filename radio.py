import Tkinter as tk
import glob
import id3reader
import pygame
import time
import threading
import json
import os.path

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

bandScroll = tk.Scrollbar(selector, orient=tk.VERTICAL, width=20)
bandScroll.grid(row=1,column=1, sticky=tk.N+tk.S)
albumScroll = tk.Scrollbar(selector, orient=tk.VERTICAL, width=20)
albumScroll.grid(row=1, column=3, sticky=tk.N+tk.S)

def select_album(evt):
	bPlay.config(state=tk.NORMAL)

lAlbums = tk.Listbox(selector, yscrollcommand=albumScroll.set, height=6, exportselection=False, width=17)
lAlbums.grid(column=2, row=1)
lAlbums.bind('<<ListboxSelect>>', select_album)
albumScroll['command']=lAlbums.yview

def select_band(evt):
	w = evt.widget
	index = int(w.curselection()[0])
	value = w.get(index)
	albums = tuple([(i.split('/'))[-1] for i in glob.glob(music_folder + value + '/*')])
	lAlbums.delete(0, 100)
	for i in albums:
		lAlbums.insert(tk.END, i) #tk.StringVar(value=songs))
	bPlay.config(state=tk.DISABLED)


lBands = tk.Listbox(selector, yscrollcommand=bandScroll.set, listvariable=bnames, height=6, selectmode=tk.SINGLE, exportselection=False, width=16)
lBands.bind('<<ListboxSelect>>', select_band)
lBands.grid(column=0, row=1)
bandScroll['command']=lBands.yview

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
	global root
	root.wm_title(bandValue + " - " + albumValue)

bPlay = tk.Button(root, text='Play album', state=tk.DISABLED, command=play_album)
bPlay.grid(column=0, row=1, sticky=tk.E, padx=42)

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
	global player
	if track < len(tracks):
		track += 1
		player.load(tracks[track])
		player.play()

bNext = tk.Button(controller, text='>|', command=next)
bNext.grid(column=2, row=0)

#loading state from file on startup
if os.path.isfile(music_folder + ".status.json"):
	file = open(music_folder + ".status.json", "r")
	status = json.loads(file.read())
	playing = status['playing']
	track = status['track']
	paused = status['paused']
	tracks = status['tracks']
	player.load(tracks[track])
	lBands.selection_set(lBands.get(0, tk.END).index(tracks[track].split("/")[-3]))
	albums = tuple([(i.split('/'))[-1] for i in glob.glob(music_folder + tracks[track].split("/")[-3] + '/*')])
	lAlbums.delete(0, 100)
	for i in albums:
		lAlbums.insert(tk.END, i) #tk.StringVar(value=songs))
	lAlbums.selection_set(lAlbums.get(0, tk.END).index(tracks[track].split("/")[-2]))
	root.wm_title(tracks[track].split("/")[-3] + " - " + tracks[track].split("/")[-2])
	bPlay.config(state=tk.NORMAL)
	if playing and not(paused):
		player.play(-1, (status['position'] / 1000.0))

#saving state to file on close
def on_closing():
	file = open(music_folder + ".status.json", "w")
	file.write(json.dumps({"playing": playing, "paused": paused, "tracks": tracks, "track": track, "position": player.get_pos()}))
	root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

tk.mainloop()
