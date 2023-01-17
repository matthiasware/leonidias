import tkinter as tk
from tkinter import ttk
from schatz import search_schatz
import time


window = tk.Tk()

grid_size= 5
max_grid_size = 8
min_grid_size = 4
font_size = 16

frm_controll = tk.Frame(master=window, bg="red")
btn_search = ttk.Button(master=frm_controll, text="Schatzsuche")
lbl_eingabe = ttk.Label(master=frm_controll, text="Gittergröße:")
ent_size = ttk.Entry(master=frm_controll)
ent_size.insert(0, "{}".format(min_grid_size))
lbl_results = ttk.Label(master=frm_controll, text="Schritte: {}".format(0))

btn_search.pack(fill=tk.BOTH, side=tk.LEFT)
lbl_eingabe.pack(fill=tk.BOTH, side=tk.LEFT)
ent_size.pack(fill=tk.BOTH, side=tk.LEFT)
lbl_results.pack(fill=tk.BOTH, side=tk.LEFT)


frm_controll.pack()
frm_grid = None


def create_grid(frm_master, grid_size):
    grid_frames = []
    for i in range(grid_size):
        frame_row = []
        for j in range(grid_size):
            frame = tk.Frame(
                master=frm_master,
                relief=tk.RAISED,
                borderwidth=1,
                height=100,
                width=100,
                bg="blue"
            )
            frame.grid(row=i, column=j)
            frame_row.append(frame)
        grid_frames.append(frame_row)
    return grid_frames

def handle_click(event):
    global frm_grid
    # read and validate entry
    grid_size = ent_size.get()
    if not grid_size.isnumeric():
        lbl_results["text"] = "Eingabe ist nicht numerisch"
        ent_size.delete(0, tk.END)
        return
    grid_size = int(grid_size)
    if grid_size < min_grid_size or grid_size > max_grid_size:
        lbl_results["text"] = "{} <= Eingabe <= {}".format(min_grid_size, max_grid_size)
        ent_size.delete(0, tk.END)
        return
        
    # destroy old window if there
    if frm_grid:
        frm_grid.pack_forget()
        frm_grid.destroy()
    
    # create new frame
    frm_grid = tk.Frame(master=window)
    grid_frames = create_grid(frm_grid, grid_size)
    frm_grid.pack()
    
    # do schatzsuche
    path, schatz = search_schatz(grid_size)
    
    # disable button
    btn_search["state"] = "disabled"
    
    # visualize schatzsuche
    grid_frames[schatz[0]][schatz[1]].config(bg="yellow")
    previous = path[0]
    for step, (x, y) in enumerate(path):
        lbl_results["text"] = "Schritt: {:>4d} / {:<4d}".format(step + 1, len(path))
        print(previous)
        grid_frames[previous[0]][previous[1]].config(bg="blue")
        grid_frames[x][y].config(bg="red")
        previous = [x, y]
        time.sleep(0.5)
        window.update()

    # enable button
    btn_search["state"] = "normal"

btn_search.bind("<Button-1>", handle_click)


window.mainloop() 