import tkinter as tk
from tkinter import colorchooser, messagebox, ttk, filedialog
from PIL import Image, ImageGrab

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("КатPaint")
        self.canvas = tk.Canvas(self.root, bg="white")

        self.root.attributes("-fullscreen", True)
        title_frame = tk.Frame(self.root, bg="#94c2ff", height=30)
        title_frame.pack(fill="x", side=tk.TOP)
        window_title = tk.Label(title_frame, text="КатPaint", bg="#94c2ff", fg="black", font=("Arial", 12))
        window_title.pack(side="left", padx=10)
        close_button = tk.Button(title_frame, text="×", command=self.close_window, bg="red", fg="white", font=("Arial", 15))
        close_button.pack(side=tk.RIGHT)

        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.setup_toolbar()

        self.color = "black"
        self.brush_size = 2
        self.current_tool = "brush"
        self.eraser_color = "white"

        self.start_x = None
        self.start_y = None

        self.setup_bindings()

    def setup_bindings(self):
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.start_x = None
        self.start_y = None

    def setup_toolbar(self):
        self.toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        brush_button = tk.Button(self.toolbar, text="Кисть", command=self.select_brush)
        brush_button.pack(side=tk.LEFT, padx=5)

        color_button = tk.Button(self.toolbar, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT, padx=5)

        eraser_button = tk.Button(self.toolbar, text="Ластик", command=self.select_eraser)
        eraser_button.pack(side=tk.LEFT, padx=5)

        fill_button = tk.Button(self.toolbar, text="Цвет фона", command=self.fill)
        fill_button.pack(side=tk.LEFT, padx=5)

        self.brush_size_slider = tk.Scale(self.toolbar, from_=1, to=30, orient=tk.HORIZONTAL, label="Размер кисти", command=self.set_brush_size)
        self.brush_size_slider.set(2)
        self.brush_size_slider.pack(side=tk.LEFT, padx=5)

        shapes_label = tk.Label(self.toolbar, text="Фигуры:")
        shapes_label.pack(side=tk.LEFT)

        self.shapes_combobox = ttk.Combobox(self.toolbar, values=["Кисть", "Линия", "Прямоугольник", "Овал"])
        self.shapes_combobox.set("Кисть")
        self.shapes_combobox.pack(side=tk.LEFT)

        draw_button = tk.Button(self.toolbar, text="Выбрать", command=self.paint_selected_shape)
        draw_button.pack(side=tk.LEFT)

        clear_button = tk.Button(self.toolbar, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.RIGHT, padx=5)

        save_button = tk.Button(self.toolbar, text="Сохранить", command=self.save)
        save_button.pack(side=tk.RIGHT, padx=5)


    def close_window(self):
        self.root.destroy()

    def choose_color(self):
        self.color = colorchooser.askcolor(color=self.color)[1]

    def set_brush_size(self, size):
        self.brush_size = int(size)

    def paint(self, event):
        x, y = event.x, event.y
        if self.start_x and self.start_y:
            if self.current_tool == "brush":
                self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.color, width=self.brush_size, capstyle=tk.ROUND, smooth=True)
            elif self.current_tool == "eraser":
                if self.canvas["bg"] == "white":
                    self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.eraser_color, width=self.brush_size, capstyle=tk.ROUND, smooth=True)
                else:
                    self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.canvas["bg"], width=self.brush_size, capstyle=tk.ROUND, smooth=True)

        self.start_x = x
        self.start_y = y

    def paintDot(self, event):
        x, y = event.x, event.y
        dot_size = self.brush_size // 2
        self.canvas.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size, fill=self.color, outline=self.color)
        if self.current_tool == "brush":
            self.canvas.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size, fill=self.color, outline=self.color)
        elif self.current_tool == "eraser":
            if self.canvas["bg"] == "white":
                self.canvas.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size, fill=self.eraser_color, outline=self.eraser_color)
            else:
                self.canvas.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size, fill=self.canvas["bg"], outline=self.canvas["bg"])

    def reset(self, event):
        if self.current_tool == "brush":
            self.paintDot(event)
        self.start_x = None
        self.start_y = None

    def clear_canvas(self):
        self.canvas.delete("all")

    def select_brush(self):
        self.current_tool = "brush"

    def select_eraser(self):
        self.current_tool = "eraser"

    def fill(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.canvas["bg"] = color
            self.color = color

    def paint_selected_shape(self):
        selected_shape = self.shapes_combobox.get()
        if selected_shape == "Кисть":
            self.current_tool = "brush"
            self.setup_bindings()
        elif selected_shape == "Линия":
            self.current_tool = "line"
            self.canvas.bind("<Button-1>", self.paint_line)
        elif selected_shape == "Прямоугольник":
            self.current_tool = "rectangle"
            self.canvas.bind("<Button-1>", self.paint_rectangle)
        elif selected_shape == "Овал":
            self.current_tool = "oval"
            self.canvas.bind("<Button-1>", self.paint_oval)

    ##################################################################################

    def paint_line(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.bind("<B1-Motion>", self.paint_line_motion)
        self.canvas.bind("<ButtonRelease-1>", self.paint_line_release)

    def paint_line_motion(self, event):
        x, y = event.x, event.y
        self.canvas.delete("temp_line")
        self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.color, width=self.brush_size, capstyle=tk.ROUND, tags="temp_line")

    def paint_line_release(self, event):
        x, y = event.x, event.y
        self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.color, capstyle=tk.ROUND, width=self.brush_size)

    ##################################################################################

    def paint_rectangle(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.bind("<B1-Motion>", self.paint_rectangle_motion)
        self.canvas.bind("<ButtonRelease-1>", self.paint_rectangle_release)

    def paint_rectangle_motion(self, event):
        x, y = event.x, event.y
        self.canvas.delete("temp_shape")
        self.canvas.create_rectangle(self.start_x, self.start_y, x, y, outline=self.color, width=self.brush_size, tags="temp_shape")

    def paint_rectangle_release(self, event):
        x, y = event.x, event.y
        self.canvas.create_rectangle(self.start_x, self.start_y, x, y, outline=self.color, width=self.brush_size)

    ##################################################################################

    def paint_oval(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.bind("<B1-Motion>", self.paint_oval_motion)
        self.canvas.bind("<ButtonRelease-1>", self.paint_oval_release)

    def paint_oval_motion(self, event):
        x, y = event.x, event.y
        self.canvas.delete("temp_shape")
        self.canvas.create_oval(self.start_x, self.start_y, x, y, outline=self.color, width=self.brush_size, tags="temp_shape")

    def paint_oval_release(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(self.start_x, self.start_y, x, y, outline=self.color, width=self.brush_size)

    ##################################################################################

    def save(self):
        fileLocation = filedialog.asksaveasfilename(defaultextension="jpg")
        x=root.winfo_rootx()
        y=root.winfo_rooty()
        img = ImageGrab.grab(bbox=(x, y+50, x+1920, y+1000))
        img.save(fileLocation)

root = tk.Tk()
app = PaintApp(root)
root.mainloop()