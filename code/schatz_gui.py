import tkinter as tk
from tkinter import ttk, font
import time


class SchatzGUI(object):
    def __init__(self, search_schatz):
        self.min_grid_size = 4
        self.max_grid_size = 8
        self.frame_size = 100
        self.search_schatz = search_schatz
        

    def _create_gui(self):
        self.window = tk.Tk()
        self.frm_controll = tk.Frame(master=self.window)
        self.btn_search = ttk.Button(master=self.frm_controll,text="Schatzsuche")
        self.lbl_eingabe = ttk.Label(master=self.frm_controll, text="Gittergröße:")
        self.ent_size = ttk.Entry(master=self.frm_controll)
        self.ent_size.insert(0, "{}".format(self.min_grid_size))
        self.lbl_results = ttk.Label(master=self.frm_controll, text="Schritte: {}".format(0))

        self.btn_search.pack(side=tk.LEFT)
        self.lbl_eingabe.pack(side=tk.LEFT)
        self.ent_size.pack(side=tk.LEFT)
        self.lbl_results.pack(side=tk.LEFT)


        self.frm_controll.pack()
        self.frm_grid = None


        self.btn_search.bind("<Button-1>", self._handle_click)
    

    def start(self):
        self._create_gui()
        self.window.mainloop()


    def _create_grid(self, frm_master, grid_size):
        grid_frames = []
        for i in range(grid_size):
            frame_row = []
            for j in range(grid_size):
                frame = tk.Frame(
                    master=frm_master,
                    relief=tk.RAISED,
                    borderwidth=1,
                    height=self.frame_size,
                    width=self.frame_size,
                    bg="blue"
                )
                frame.grid(row=i, column=j)
                frame_row.append(frame)
            grid_frames.append(frame_row)
        return grid_frames

    def _handle_click(self, event):
        # disable button
        self.btn_search["state"] = "disabled"
        self.window.update()
    
        # read and validate entry
        grid_size = self.ent_size.get()
        if not grid_size.isnumeric():
            self.lbl_results["text"] = "Eingabe ist nicht numerisch"
            self.ent_size.delete(0, tk.END)
            return
        grid_size = int(grid_size)
        if grid_size < self.min_grid_size or grid_size > self.max_grid_size:
            self.lbl_results["text"] = "{} <= Eingabe <= {}".format(self.min_grid_size,self.max_grid_size)
            self.ent_size.delete(0, tk.END)
            return
            
        # destroy old window if there
        if self.frm_grid:
            self.frm_grid.pack_forget()
            self.frm_grid.destroy()
        
        # create new frame
        self.frm_grid = tk.Frame(master=self.window)
        grid_frames = self._create_grid(self.frm_grid, grid_size)
        self.frm_grid.pack()
        
        # do schatzsuche
        path, schatz = self.search_schatz(grid_size)
        
        # visualize schatzsuche
        grid_frames[schatz[0]][schatz[1]].config(bg="yellow")
        previous = path[0]
        for step, (x, y) in enumerate(path):
            self.lbl_results["text"] = "Schritt: {:>4d} / {:<4d}".format(step + 1, len(path))
            print(previous)
            grid_frames[previous[0]][previous[1]].config(bg="blue")
            grid_frames[x][y].config(bg="red")
            previous = [x, y]
            time.sleep(0.5)
            self.window.update()

        # enable button
        self.btn_search["state"] = "normal"
        self.window.update()