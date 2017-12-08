import Tkinter as tk
import glob
import id3reader

root = tk.Tk()
root.geometry("320x240")
selector = tk.Frame(root)
selector.grid(row=0, column=0)

bands = tuple([(i.split('/'))[-1] for i in glob.glob('/home/ryan/Music/*')])
bnames = tk.StringVar(value=bands)

yScroll = tk.Scrollbar(orient=tk.VERTICAL)
yScroll.grid(row=0,column=1, sticky=tk.N+tk.S)

def select_album(evt):
	bPlay.config(state=tk.NORMAL)

lAlbums = tk.Listbox(selector, height=8, exportselection=False)
lAlbums.grid(column=1, row=0)
lAlbums.bind('<<ListboxSelect>>', select_album)

def select_band(evt):
	w = evt.widget
	index = int(w.curselection()[0])
	value = w.get(index)
	albums = tuple([(i.split('/'))[-1] for i in glob.glob('/home/ryan/Music/' + value + '/*')])
	lAlbums.delete(0, 100)
	for i in albums:
		lAlbums.insert(tk.END, i) #tk.StringVar(value=songs))

lBands = tk.Listbox(selector, yscrollcommand=yScroll.set, listvariable=bnames, height=8, selectmode=tk.SINGLE, exportselection=False)
lBands.bind('<<ListboxSelect>>', select_band)
lBands.grid(column=0, row=0)
yScroll['command']=lBands.yview

def play():
	bandIndex = lBands.curselection()[0]
	bandValue = lBands.get(bandIndex)
	albumIndex = lAlbums.curselection()[0]
	albumValue = lAlbums.get(albumIndex)
	songs = tuple([(i.split('/'))[-1] for i in sorted(glob.glob('/home/ryan/Music/' + bandValue + '/' + albumValue + '/*.mp3'),key=lambda i:int(id3reader.Reader(i).getValue('track').split('/')[0]))])
	for i in songs:
		print(i)


bPlay = tk.Button(root, text='Play album', state=tk.DISABLED, command=play)
bPlay.grid(column=0, row=1)

controller = tk.Frame(root)
controller.grid(column=0, row=2)

bPrev = tk.Button(controller, text='|<')
bPrev.grid(column=0, row=0)
bPlayPause = tk.Button(controller, text='|| / >')
bPlayPause.grid(column=1, row=0)
bNext = tk.Button(controller, text='>|')
bNext.grid(column=2, row=0)

tk.mainloop()
