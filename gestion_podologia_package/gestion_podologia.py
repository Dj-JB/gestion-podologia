import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import os
try:
    from tkcalendar import Calendar
except Exception:
    Calendar = None
from PIL import Image, ImageTk

DB_NAME = "podologia.db"

def init_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        apellidos TEXT,
        dni TEXT,
        direccion TEXT,
        telefono TEXT,
        email TEXT,
        observaciones TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        fecha TEXT,
        hora TEXT,
        descripcion TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS imagenes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        ruta TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    """)
    conn.commit()

class PodologiaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Podología")
        self.root.geometry("1000x600")

        self.conn = sqlite3.connect(DB_NAME)
        init_db(self.conn)
        self.cursor = self.conn.cursor()

        self.tabControl = ttk.Notebook(root)
        self.tab_clientes = ttk.Frame(self.tabControl)
        self.tab_citas = ttk.Frame(self.tabControl)
        self.tab_imagenes = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_clientes, text='Clientes')
        self.tabControl.add(self.tab_citas, text='Citas')
        self.tabControl.add(self.tab_imagenes, text='Imágenes')
        self.tabControl.pack(expand=1, fill="both")

        self.crear_tab_clientes()
        self.crear_tab_citas()
        self.crear_tab_imagenes()

    def crear_tab_clientes(self):
        frame_form = tk.Frame(self.tab_clientes)
        frame_form.pack(side=tk.LEFT, padx=10, pady=10, fill="y")

        labels = ["Nombre", "Apellidos", "DNI", "Dirección", "Teléfono", "Email", "Observaciones"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(frame_form, text=label).grid(row=i, column=0, sticky="e")
            entry = tk.Entry(frame_form, width=30)
            entry.grid(row=i, column=1, pady=2)
            self.entries[label] = entry

        tk.Button(frame_form, text="Guardar Cliente", command=self.guardar_cliente).grid(row=len(labels), columnspan=2, pady=10)

        self.tree_clientes = ttk.Treeview(self.tab_clientes, columns=("ID", "Nombre", "Apellidos", "Teléfono"), show='headings')
        for col in ("ID", "Nombre", "Apellidos", "Teléfono"):
            self.tree_clientes.heading(col, text=col)
            self.tree_clientes.column(col, width=150)
        self.tree_clientes.pack(fill="both", expand=True, padx=10, pady=10)
        self.cargar_clientes()

    def guardar_cliente(self):
        datos = [self.entries["Nombre"].get(), self.entries["Apellidos"].get(), self.entries["DNI"].get(),
                 self.entries["Dirección"].get(), self.entries["Teléfono"].get(), self.entries["Email"].get(),
                 self.entries["Observaciones"].get()]
        self.cursor.execute("INSERT INTO clientes (nombre, apellidos, dni, direccion, telefono, email, observaciones) VALUES (?,?,?,?,?,?,?)", datos)
        self.conn.commit()
        self.cargar_clientes()
        messagebox.showinfo("Éxito", "Cliente guardado correctamente")

    def cargar_clientes(self):
        for row in self.tree_clientes.get_children():
            self.tree_clientes.delete(row)
        self.cursor.execute("SELECT id, nombre, apellidos, telefono FROM clientes")
        for cliente in self.cursor.fetchall():
            self.tree_clientes.insert("", tk.END, values=cliente)

    def crear_tab_citas(self):
        frame = tk.Frame(self.tab_citas)
        frame.pack(pady=20, padx=10, fill="x")

        tk.Label(frame, text="Seleccionar Cliente (ID)").grid(row=0, column=0, sticky="e")
        self.cliente_id_cita = tk.Entry(frame)
        self.cliente_id_cita.grid(row=0, column=1, sticky="w")

        tk.Label(frame, text="Fecha").grid(row=1, column=0, sticky="ne")
        if Calendar:
            self.cal = Calendar(frame, selectmode='day')
            self.cal.grid(row=1, column=1, sticky="w")
        else:
            self.cal = None
            tk.Label(frame, text="(tkcalendar no instalado, la fecha se guardará como texto)").grid(row=1, column=1, sticky="w")

        tk.Label(frame, text="Hora").grid(row=2, column=0, sticky="e")
        self.hora_cita = tk.Entry(frame)
        self.hora_cita.grid(row=2, column=1, sticky="w")

        tk.Label(frame, text="Descripción").grid(row=3, column=0, sticky="e")
        self.desc_cita = tk.Entry(frame)
        self.desc_cita.grid(row=3, column=1, sticky="w")

        tk.Button(frame, text="Guardar Cita", command=self.guardar_cita).grid(row=4, columnspan=2, pady=10)

        self.tree_citas = ttk.Treeview(self.tab_citas, columns=("ID", "Cliente", "Fecha", "Hora"), show='headings')
        for col in ("ID", "Cliente", "Fecha", "Hora"):
            self.tree_citas.heading(col, text=col)
            self.tree_citas.column(col, width=150)
        self.tree_citas.pack(fill="both", expand=True, padx=10, pady=10)
        self.cargar_citas()

    def guardar_cita(self):
        fecha = self.cal.get_date() if self.cal else self.cliente_id_cita.get()
        datos = [self.cliente_id_cita.get(), fecha, self.hora_cita.get(), self.desc_cita.get()]
        self.cursor.execute("INSERT INTO citas (cliente_id, fecha, hora, descripcion) VALUES (?,?,?,?)", datos)
        self.conn.commit()
        self.cargar_citas()
        messagebox.showinfo("Éxito", "Cita guardada correctamente")

    def cargar_citas(self):
        for row in self.tree_citas.get_children():
            self.tree_citas.delete(row)
        self.cursor.execute("SELECT id, cliente_id, fecha, hora FROM citas")
        for cita in self.cursor.fetchall():
            self.tree_citas.insert("", tk.END, values=cita)

    def crear_tab_imagenes(self):
        frame = tk.Frame(self.tab_imagenes)
        frame.pack(pady=20, padx=10, fill="both", expand=True)

        tk.Label(frame, text="ID Cliente").grid(row=0, column=0, sticky="e")
        self.cliente_id_img = tk.Entry(frame)
        self.cliente_id_img.grid(row=0, column=1, sticky="w")

        tk.Button(frame, text="Añadir Imagen", command=self.guardar_imagen).grid(row=1, columnspan=2, pady=10)

        self.panel_img = tk.Label(self.tab_imagenes)
        self.panel_img.pack(pady=10)

        self.lista_imgs = ttk.Treeview(self.tab_imagenes, columns=("ID", "Cliente", "Ruta"), show='headings')
        for col in ("ID", "Cliente", "Ruta"):
            self.lista_imgs.heading(col, text=col)
            self.lista_imgs.column(col, width=300)
        self.lista_imgs.pack(fill="both", expand=True)
        self.lista_imgs.bind("<Double-1>", self.ver_imagen)
        self.cargar_imagenes()

    def guardar_imagen(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            return
        # copy image to a local folder for portability
        os.makedirs('imagenes', exist_ok=True)
        filename = os.path.basename(file_path)
        dest = os.path.join('imagenes', filename)
        try:
            with open(file_path, 'rb') as fr, open(dest, 'wb') as fw:
                fw.write(fr.read())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar la imagen: {e}")
            return
        datos = [self.cliente_id_img.get(), dest]
        self.cursor.execute("INSERT INTO imagenes (cliente_id, ruta) VALUES (?,?)", datos)
        self.conn.commit()
        self.cargar_imagenes()

    def cargar_imagenes(self):
        for row in self.lista_imgs.get_children():
            self.lista_imgs.delete(row)
        self.cursor.execute("SELECT id, cliente_id, ruta FROM imagenes")
        for img in self.cursor.fetchall():
            self.lista_imgs.insert("", tk.END, values=img)

    def ver_imagen(self, event):
        sel = self.lista_imgs.selection()
        if not sel:
            return
        item = sel[0]
        ruta = self.lista_imgs.item(item, "values")[2]
        try:
            img = Image.open(ruta)
            img.thumbnail((600,600))
            img_tk = ImageTk.PhotoImage(img)
            self.panel_img.config(image=img_tk)
            self.panel_img.image = img_tk
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PodologiaApp(root)
    root.mainloop()
