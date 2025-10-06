import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import math

class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображений - Вариант")
        self.root.geometry("1100x720")

        self.image_new = None
        self.image_src = None

        self.photo_new = None
        self.photo_src = None

        self.init_ui()

    def init_ui(self):
        main = ttk.Frame(self.root, padding=6)
        main.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(main, width=320)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)

        right = ttk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        new_frame = ttk.LabelFrame(left, text="Новое изображение", padding=6)
        new_frame.pack(fill=tk.X, pady=4)

        ttk.Label(new_frame, text="Width:").grid(row=0, column=0, sticky=tk.W)
        self.ent_width = ttk.Entry(new_frame, width=10); self.ent_width.insert(0, "400")
        self.ent_width.grid(row=0, column=1, padx=4, pady=2)

        ttk.Label(new_frame, text="Height:").grid(row=1, column=0, sticky=tk.W)
        self.ent_height = ttk.Entry(new_frame, width=10); self.ent_height.insert(0, "300")
        self.ent_height.grid(row=1, column=1, padx=4, pady=2)

        btn_create = ttk.Button(new_frame, text="Создать", command=self.create_new_image)
        btn_create.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=4)

        src_frame = ttk.LabelFrame(left, text="Исходное изображение (файл)", padding=6)
        src_frame.pack(fill=tk.X, pady=4)

        btn_open = ttk.Button(src_frame, text="Открыть изображение", command=self.open_image)
        btn_open.pack(fill=tk.X, pady=2)

        frag_frame = ttk.LabelFrame(left, text="Фрагмент (перенос по-пиксельно)", padding=6)
        frag_frame.pack(fill=tk.X, pady=4)

        ttk.Label(frag_frame, text="Форма:").grid(row=0, column=0, sticky=tk.W)
        self.shape_var = tk.StringVar(value="triangle")
        ttk.Radiobutton(frag_frame, text="Треугольник", variable=self.shape_var, value="triangle").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(frag_frame, text="Прямоугольник", variable=self.shape_var, value="rect").grid(row=0, column=2, sticky=tk.W)

        ttk.Label(frag_frame, text="Размер (side):").grid(row=1, column=0, sticky=tk.W)
        self.ent_size = ttk.Entry(frag_frame, width=8); self.ent_size.insert(0, "100")
        self.ent_size.grid(row=1, column=1, sticky=tk.W, padx=4)

        ttk.Label(frag_frame, text="src_x:").grid(row=2, column=0, sticky=tk.W)
        self.ent_src_x = ttk.Entry(frag_frame, width=8); self.ent_src_x.insert(0, "0")
        self.ent_src_x.grid(row=2, column=1, sticky=tk.W, padx=4)
        ttk.Label(frag_frame, text="src_y:").grid(row=2, column=2, sticky=tk.W)
        self.ent_src_y = ttk.Entry(frag_frame, width=8); self.ent_src_y.insert(0, "0")
        self.ent_src_y.grid(row=2, column=3, sticky=tk.W, padx=4)

        ttk.Label(frag_frame, text="dst_x:").grid(row=3, column=0, sticky=tk.W)
        self.ent_dst_x = ttk.Entry(frag_frame, width=8); self.ent_dst_x.insert(0, "0")
        self.ent_dst_x.grid(row=3, column=1, sticky=tk.W, padx=4)
        ttk.Label(frag_frame, text="dst_y:").grid(row=3, column=2, sticky=tk.W)
        self.ent_dst_y = ttk.Entry(frag_frame, width=8); self.ent_dst_y.insert(0, "0")
        self.ent_dst_y.grid(row=3, column=3, sticky=tk.W, padx=4)

        btn_transfer = ttk.Button(frag_frame, text="Перенести фрагмент", command=self.transfer_fragment)
        btn_transfer.grid(row=4, column=0, columnspan=4, sticky=tk.EW, pady=6)

        graph_frame = ttk.LabelFrame(left, text="Оси и график", padding=6)
        graph_frame.pack(fill=tk.X, pady=4)

        ttk.Label(graph_frame, text="Функция y =").grid(row=0, column=0, sticky=tk.W)
        self.ent_func = ttk.Entry(graph_frame, width=20); self.ent_func.insert(0, "1/((x-1)**2)")
        self.ent_func.grid(row=0, column=1, columnspan=2, sticky=tk.W, padx=4)

        ttk.Label(graph_frame, text="x scale:").grid(row=1, column=0, sticky=tk.W)
        self.ent_xscale = ttk.Entry(graph_frame, width=8); self.ent_xscale.insert(0, "0.1")
        self.ent_xscale.grid(row=1, column=1, sticky=tk.W, padx=4)
        ttk.Label(graph_frame, text="y scale:").grid(row=1, column=2, sticky=tk.W)
        self.ent_yscale = ttk.Entry(graph_frame, width=8); self.ent_yscale.insert(0, "100")
        self.ent_yscale.grid(row=1, column=3, sticky=tk.W, padx=4)

        btn_axes = ttk.Button(graph_frame, text="Добавить оси", command=self.draw_axes)
        btn_axes.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=4)
        btn_plot = ttk.Button(graph_frame, text="Построить график", command=self.plot_function)
        btn_plot.grid(row=2, column=2, columnspan=2, sticky=tk.EW, pady=4)

        save_frame = ttk.Frame(left)
        save_frame.pack(fill=tk.X, pady=4)
        btn_save = ttk.Button(save_frame, text="Сохранить (png/jpg/bmp)", command=self.save_image)
        btn_save.pack(fill=tk.X, pady=2)
        btn_save_ppm = ttk.Button(save_frame, text="Сохранить PPM (ASCII)", command=self.save_ppm)
        btn_save_ppm.pack(fill=tk.X, pady=2)

        display_frame = ttk.Frame(right)
        display_frame.pack(fill=tk.BOTH, expand=True)

        top_disp = ttk.LabelFrame(display_frame, text="Новое изображение", padding=4)
        top_disp.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.canvas_new = tk.Canvas(top_disp, width=700, height=380, bg="white", bd=1, relief=tk.SUNKEN)
        self.canvas_new.pack(fill=tk.BOTH, expand=True)

        bottom_disp = ttk.LabelFrame(display_frame, text="Исходное изображение", padding=4)
        bottom_disp.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.canvas_src = tk.Canvas(bottom_disp, width=700, height=240, bg="white", bd=1, relief=tk.SUNKEN)
        self.canvas_src.pack(fill=tk.BOTH, expand=True)

    def create_new_image(self):
        try:
            w = int(self.ent_width.get())
            h = int(self.ent_height.get())
            if w <= 0 or h <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные размеры нового изображения")
            return
        self.image_new = Image.new("RGB", (w, h), (255, 255, 255))
        self.update_new_display()

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")])
        if not path:
            return
        try:
            self.image_src = Image.open(path).convert("RGB")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Невозможно открыть файл: {e}")
            return
        self.update_src_display()

    def update_new_display(self):
        self.canvas_new.delete("all")
        if self.image_new is None:
            self.canvas_new.create_text(350, 190, text="Нет нового изображения", fill="gray")
            return
        img = self.image_new.copy()
        w_canvas = self.canvas_new.winfo_width() or 700
        h_canvas = self.canvas_new.winfo_height() or 380
        img.thumbnail((w_canvas, h_canvas))
        self.photo_new = ImageTk.PhotoImage(img)
        self.canvas_new.create_image(w_canvas//2, h_canvas//2, image=self.photo_new)

    def update_src_display(self):
        self.canvas_src.delete("all")
        if self.image_src is None:
            self.canvas_src.create_text(350, 120, text="Нет исходного изображения", fill="gray")
            return
        img = self.image_src.copy()
        w_canvas = self.canvas_src.winfo_width() or 700
        h_canvas = self.canvas_src.winfo_height() or 240
        img.thumbnail((w_canvas, h_canvas))
        self.photo_src = ImageTk.PhotoImage(img)
        self.canvas_src.create_image(w_canvas//2, h_canvas//2, image=self.photo_src)

    def make_triangle_vertices_at(self, anchor_x, anchor_y, side, orientation="right"):
        h = side * math.sqrt(3) / 2.0
        v1 = (anchor_x, anchor_y)
        v2 = (anchor_x, anchor_y + side)
        v3 = (anchor_x + h, anchor_y + side/2)
        return [v1, v2, v3]

    def inside_triangle_barycentric(self, px, py, verts):
        (x1,y1),(x2,y2),(x3,y3) = verts
        denom = (y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3)
        if denom == 0:
            return False, (0,0,0)
        a = ((y2 - y3)*(px - x3) + (x3 - x2)*(py - y3)) / denom
        b = ((y3 - y1)*(px - x3) + (x1 - x3)*(py - y3)) / denom
        c = 1 - a - b
        inside = (0 <= a <= 1) and (0 <= b <= 1) and (0 <= c <= 1)
        return inside, (a,b,c)

    def transfer_fragment(self):
        if self.image_new is None or self.image_src is None:
            messagebox.showerror("Ошибка", "Нужно создать новое изображение и открыть исходное")
            return
        try:
            side = int(self.ent_size.get())
            src_x = int(self.ent_src_x.get())
            src_y = int(self.ent_src_y.get())
            dst_x = int(self.ent_dst_x.get())
            dst_y = int(self.ent_dst_y.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные числовые параметры")
            return

        shape = self.shape_var.get()

        draw = ImageDraw.Draw(self.image_new)
        src_pixels = self.image_src.load()

        if shape == "rect":
            for dy in range(side):
                for dx in range(side):
                    sx = src_x + dx
                    sy = src_y + dy
                    tx = dst_x + dx
                    ty = dst_y + dy
                    if 0 <= sx < self.image_src.width and 0 <= sy < self.image_src.height and 0 <= tx < self.image_new.width and 0 <= ty < self.image_new.height:
                        draw.point((tx, ty), fill=src_pixels[sx, sy])
            draw.rectangle([dst_x, dst_y, dst_x + side - 1, dst_y + side - 1], outline=(255,0,0))

        else:
            verts_src = self.make_triangle_vertices_at(src_x, src_y, side)
            verts_dst = self.make_triangle_vertices_at(dst_x, dst_y, side)

            min_x = max(0, int(min(p[0] for p in verts_dst)))
            max_x = min(self.image_new.width-1, int(max(p[0] for p in verts_dst)))
            min_y = max(0, int(min(p[1] for p in verts_dst)))
            max_y = min(self.image_new.height-1, int(max(p[1] for p in verts_dst)))

            sx1, sy1 = verts_src[0]
            sx2, sy2 = verts_src[1]
            sx3, sy3 = verts_src[2]
            dx1, dy1 = verts_dst[0]
            dx2, dy2 = verts_dst[1]
            dx3, dy3 = verts_dst[2]

            for ty in range(min_y, max_y+1):
                for tx in range(min_x, max_x+1):
                    inside, (a,b,c) = self.inside_triangle_barycentric(tx, ty, verts_dst)
                    if not inside:
                        continue
                    src_fx = a * sx1 + b * sx2 + c * sx3
                    src_fy = a * sy1 + b * sy2 + c * sy3
                    src_ix = int(round(src_fx))
                    src_iy = int(round(src_fy))
                    if 0 <= src_ix < self.image_src.width and 0 <= src_iy < self.image_src.height:
                        draw.point((tx, ty), fill=src_pixels[src_ix, src_iy])
                    else:
                        draw.point((tx, ty), fill=(0,0,0))
            draw.polygon(verts_dst, outline=(255,0,0))

        self.update_new_display()
        messagebox.showinfo("Готово", "Фрагмент перенесён.")

    def draw_axes(self):
        if self.image_new is None:
            messagebox.showerror("Ошибка", "Создайте новое изображение")
            return
        draw = ImageDraw.Draw(self.image_new)
        w, h = self.image_new.size
        cx = w // 2
        cy = h // 2

        draw.line([(cx, h-5), (cx, 5)], fill=(0,0,0))
        draw.line([(cx-6, 12), (cx, 5), (cx+6, 12)], fill=(0,0,0))
        draw.line([(5, cy), (w-5, cy)], fill=(0,0,0))
        draw.line([(w-12, cy-6), (w-5, cy), (w-12, cy+6)], fill=(0,0,0))
        for i in range(20, w//2, 20):
            x1 = cx + i
            x2 = cx - i
            if 5 < x1 < w-5: draw.line([(x1, cy-3), (x1, cy+3)], fill=(0,0,0))
            if 5 < x2 < w-5: draw.line([(x2, cy-3), (x2, cy+3)], fill=(0,0,0))
        for j in range(20, h//2, 20):
            y1 = cy + j
            y2 = cy - j
            if 5 < y1 < h-5: draw.line([(cx-3, y1), (cx+3, y1)], fill=(0,0,0))
            if 5 < y2 < h-5: draw.line([(cx-3, y2), (cx+3, y2)], fill=(0,0,0))
        draw.text((cx+6, 6), "Y", fill=(0,0,0))
        draw.text((w-20, cy+6), "X", fill=(0,0,0))
        draw.text((cx+4, cy+4), "0", fill=(0,0,0))

        self.update_new_display()

    def safe_eval_func(self, expr, x):
        forbidden = ["__", "import", "open(", "exec(", "eval(", "os.", "sys.", "subprocess", ";"]
        for token in forbidden:
            if token in expr:
                raise ValueError("Недопустимое выражение функции")
        local_vars = {"x": x, "math": math}
        return eval(expr, {"__builtins__": {}}, local_vars)

    def plot_function(self):
        if self.image_new is None:
            messagebox.showerror("Ошибка", "Создайте новое изображение")
            return
        func_text = self.ent_func.get().strip()
        try:
            xs = float(self.ent_xscale.get())
            ys = float(self.ent_yscale.get())
            if xs == 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Неправильные масштабы")
            return

        draw = ImageDraw.Draw(self.image_new)
        w, h = self.image_new.size
        cx = w // 2
        cy = h // 2

        prev = None
        for i in range(5, w-5):
            x_val = (i - cx) * xs
            try:
                y_val = self.safe_eval_func(func_text, x_val)
            except Exception:
                prev = None
                continue
            j = cy - int(round(y_val * ys))
            if 0 <= j < h:
                if prev is not None:
                    if 0 <= prev[0] < w and 0 <= prev[1] < h:
                        draw.line([prev, (i, j)], fill=(0,0,255), width=1)
                prev = (i, j)
            else:
                prev = None

        self.update_new_display()
        messagebox.showinfo("Готово", "График построен (если функция определена на отрезке).")

    def save_image(self):
        if self.image_new is None:
            messagebox.showerror("Ошибка", "Нет изображения для сохранения")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png"),("JPEG","*.jpg"),("BMP","*.bmp")])
        if not path:
            return
        try:
            self.image_new.save(path)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Невозможно сохранить: {e}")
            return
        messagebox.showinfo("Успех", f"Сохранено: {path}")

    def save_ppm(self):
        if self.image_new is None:
            messagebox.showerror("Ошибка", "Нет изображения для сохранения")
            return
        path = filedialog.asksaveasfilename(defaultextension=".ppm", filetypes=[("PPM ASCII","*.ppm"),("All","*.*")])
        if not path:
            return
        try:
            img = self.image_new.convert("RGB")
            w,h = img.size
            pixels = img.load()
            with open(path, "w") as f:
                f.write("P3\n")
                f.write(f"{w} {h}\n")
                f.write("255\n")
                for y in range(h):
                    row = []
                    for x in range(w):
                        r,g,b = pixels[x,y]
                        row.append(f"{r} {g} {b}")
                    f.write(" ".join(row) + "\n")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Невозможно сохранить PPM: {e}")
            return
        messagebox.showinfo("Успех", f"Сохранено (PPM ASCII): {path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    def on_resize(event):
        app.update_new_display()
        app.update_src_display()
    root.bind("<Configure>", on_resize)
    root.mainloop()
