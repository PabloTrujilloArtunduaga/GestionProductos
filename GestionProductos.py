import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import messagebox
import csv

# ===========================
# LÓGICA (tus funciones: sin cambios significativos)
# ===========================

# Funcion para exportar csv
def export_csv():
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nombre, categoria, precio, cantidad, proveedor FROM productos ORDER BY id ASC")
                filas = cur.fetchall()
                with open("productos.csv", mode="w", newline='', encoding="utf-8") as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv)
                    escritor_csv.writerow(["ID", "Producto", "Categoría", "Precio", "Cantidad", "Proveedor"])
                    escritor_csv.writerows(filas)

        messagebox.showinfo("Éxito", "Datos exportados a productos.csv correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar datos: {e}")

# Funcion para borrar
def eliminar_producto():
    seleccion = tree.focus()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Debes seleccionar un producto en la tabla.")
        return

    valores = tree.item(seleccion, "values")
    product_id = valores[0]

    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM productos WHERE id = %s", (product_id,))
                conn.commit()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        mostrar_datos()
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error: {e}")

# Funcion para seleccionar item del treeview
def seleccionar_item(event):
    seleccion = tree.focus()
    if seleccion:
        valores = tree.item(seleccion, "values")
        entry_producto.delete(0, tk.END)
        entry_categoria.set("")
        entry_precio.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_proveedor.delete(0, tk.END)

        entry_producto.insert(0, valores[1])
        entry_categoria.set(valores[2])
        entry_precio.insert(0, valores[3])
        entry_cantidad.insert(0, valores[4])
        entry_proveedor.insert(0, valores[5])

# Funcion para mostrar datos en el treeview
def mostrar_datos():
    for item in tree.get_children():
        tree.delete(item)
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nombre, categoria, precio, cantidad, proveedor FROM productos ORDER BY id ASC")
                filas = cur.fetchall()
                for i, fila in enumerate(filas):
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    tree.insert("", tk.END, values=fila, tags=(tag,))
    except Exception as e:
        messagebox.showerror("Error", e)

# Funcion para la conexion a la base de datos
def obtener_conexion():
    return psycopg2.connect(
        host="localhost",
        dbname="demo",
        user="postgres",
        password="1234",
        port=5432
    )

# Insertar datos
def agregar_producto():
    if entry_producto.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo producto está vacío")
        return
    if entry_categoria.get().strip() == "":
        messagebox.showwarning("Advertencia", "Debe seleccionar una categoria")
        return
    if entry_precio.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo precio está vacío")
        return
    if entry_cantidad.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo cantidad está vacío")
        return
    if entry_proveedor.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo proveedor está vacío")
        return

    try:
        precio = int(entry_precio.get())
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número entero.")
        return

    try:
        cantidad = int(entry_cantidad.get())
    except ValueError as ve:
        messagebox.showerror("Error", f"La cantidad debe ser un número entero.")
        return

    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO productos (nombre, categoria, precio, cantidad, proveedor) VALUES (%s, %s, %s, %s, %s)",
                    (entry_producto.get(), entry_categoria.get(), precio, cantidad, entry_proveedor.get())
                )
                conn.commit()
        messagebox.showinfo("Éxito", "Producto registrada correctamente.")
        mostrar_datos()
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error: {e}")

# Funcion para actualizar datos
def actualizar_producto():
    seleccion = tree.focus()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Debes seleccionar un producto en la tabla.")
        return
    
    if entry_producto.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo producto está vacío")
        return
    if entry_categoria.get().strip() == "":
        messagebox.showwarning("Advertencia", "Debe seleccionar una categoria")
        return
    if entry_precio.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo precio está vacío")
        return
    if entry_cantidad.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo cantidad está vacío")
        return
    if entry_proveedor.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo proveedor está vacío")
        return

    

    valores = tree.item(seleccion, "values")
    product_id = valores[0]

    try:
        precio = int(entry_precio.get())
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número entero.")
        return

    try:
        cantidad = int(entry_cantidad.get())
    except ValueError as ve:
        messagebox.showerror("Error", f"La cantidad debe ser un número entero.")
        return

    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                cur.execute(
                 "UPDATE productos SET nombre = %s, categoria = %s, precio = %s, cantidad = %s, proveedor = %s WHERE id = %s",
                    (entry_producto.get(), entry_categoria.get(), precio, cantidad, entry_proveedor.get(), product_id)
                )
                conn.commit()
        messagebox.showinfo("Éxito", "Producto registrada correctamente.")
        mostrar_datos()
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error: {e}")
        
# Funciona para buscar "nombre" 
def buscar_producto():
    filtro = search_var.get().strip()
    for item in tree.get_children():
        tree.delete(item)
    if filtro == "":
        mostrar_datos()
        return
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nombre, categoria, precio, cantidad, proveedor FROM productos WHERE nombre ILIKE %s ORDER BY id ASC", (f"%{filtro}%",))
                filas = cur.fetchall()
                for i, fila in enumerate(filas):
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    tree.insert("", tk.END, values=fila, tags=(tag,))
    except Exception as e:
        messagebox.showerror("Error", e)


# Funcion para limpiar campos
def limpiar_campos():
    entry_producto.delete(0, tk.END)
    entry_categoria.set("Seleccione...")
    entry_precio.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    entry_proveedor.delete(0, tk.END)

# ===========================
# DISEÑO / UI (mejorado)
# ===========================

root = tk.Tk()
root.title("Inventory Pro — Sistema de Inventario")
root.geometry("1300x770")
root.configure(bg="#f7f9fb")  # fondo claro suave
root.minsize(1000, 600)

# Fuente principal
FONT_HEADER = ("Segoe UI Semibold", 18)
FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 10, "bold")

# ---------- Style ----------
style = ttk.Style()
style.theme_use("clam")

# Treeview style
style.configure("Clean.Treeview",
                background="#ffffff",
                foreground="#334155",
                fieldbackground="#ffffff",
                rowheight=26,
                font=FONT_ENTRY)
style.configure("Clean.Treeview.Heading",
                background="#0ea5a4",
                foreground="#ffffff",
                font=("Segoe UI Semibold", 11))
style.map("Clean.Treeview", background=[("selected", "#7dd3fc")])

# TTK Buttons default look (we'll use tk.Button for custom look)
style.configure("TLabel", background="#f7f9fb", foreground="#334155")

# ---------- Layout frames ----------
# Header
header = tk.Frame(root, bg="#ffffff", bd=0, relief="flat")
header.pack(fill="x", padx=18, pady=(18,8))

lbl_title = tk.Label(header, text="Inventory Pro", font=FONT_HEADER, bg="#ffffff", fg="#0f172a")
lbl_title.pack(side="left")

lbl_sub = tk.Label(header, text="— Gestión de productos", font=("Segoe UI", 10), bg="#ffffff", fg="#64748b")
lbl_sub.pack(side="left", padx=(12,0))

# Search box in header
frame_search = tk.Frame(header, bg="#ffffff")
frame_search.pack(side="right")
search_var = tk.StringVar()
entry_search = tk.Entry(frame_search, textvariable=search_var, font=FONT_ENTRY, width=28, bd=1, relief="solid")
entry_search.pack(side="left", padx=(0,8), ipady=3)

def buscar_por_nombre():
    filtro = search_var.get().strip()
    for item in tree.get_children():
        tree.delete(item)
    if filtro == "":
        mostrar_datos()
        return
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nombre, categoria, precio, cantidad, proveedor FROM productos WHERE nombre ILIKE %s ORDER BY id ASC", (f"%{filtro}%",))
                filas = cur.fetchall()
                for i, fila in enumerate(filas):
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    tree.insert("", tk.END, values=fila, tags=(tag,))
    except Exception as e:
        messagebox.showerror("Error", e)

btn_search_top = tk.Button(frame_search, text="Buscar", command=buscar_producto, bg="#0ea5a4", fg="white", font=FONT_BTN, bd=0, padx=12, pady=6, cursor="hand2")
btn_search_top.pack(side="left")

# Main content frames
content = tk.Frame(root, bg="#f7f9fb")
content.pack(fill="both", expand=True, padx=18, pady=(0,18))

left_panel = tk.Frame(content, bg="#ffffff", bd=1, relief="groove")
left_panel.pack(side="left", fill="y", padx=(0,12), pady=6)

right_panel = tk.Frame(content, bg="#ffffff", bd=1, relief="groove")
right_panel.pack(side="right", fill="both", expand=True, padx=(12,0), pady=6)

# ---------- Left panel: Form ----------
form_title = tk.Label(left_panel, text="Datos del Producto", bg="#ffffff", fg="#0f172a", font=("Segoe UI Semibold", 12))
form_title.pack(anchor="w", padx=16, pady=(12,4))

form_frame = tk.Frame(left_panel, bg="#ffffff")
form_frame.pack(padx=12, pady=8)

# Labels & entries (placed nicely)
tk.Label(form_frame, text="Producto", font=FONT_LABEL, bg="#ffffff", fg="#0f172a").grid(row=0, column=0, sticky="w", padx=6, pady=6)
entry_producto = tk.Entry(form_frame, font=FONT_ENTRY, width=28, bd=1, relief="solid")
entry_producto.grid(row=0, column=1, padx=6, pady=6)

tk.Label(form_frame, text="Categoría", font=FONT_LABEL, bg="#ffffff", fg="#0f172a").grid(row=1, column=0, sticky="w", padx=6, pady=6)
categorias = ["Electrónica", "Ropa", "Bebidas", "Aseo", "Alimentos", "Papelería", "Herramientas"]
entry_categoria = ttk.Combobox(form_frame, values=categorias, font=FONT_ENTRY, width=26, state="readonly")
entry_categoria.grid(row=1, column=1, padx=6, pady=6)
entry_categoria.set("Seleccione...")

tk.Label(form_frame, text="Precio", font=FONT_LABEL, bg="#ffffff", fg="#0f172a").grid(row=2, column=0, sticky="w", padx=6, pady=6)
entry_precio = tk.Entry(form_frame, font=FONT_ENTRY, width=28, bd=1, relief="solid")
entry_precio.grid(row=2, column=1, padx=6, pady=6)

tk.Label(form_frame, text="Cantidad", font=FONT_LABEL, bg="#ffffff", fg="#0f172a").grid(row=3, column=0, sticky="w", padx=6, pady=6)
entry_cantidad = tk.Entry(form_frame, font=FONT_ENTRY, width=28, bd=1, relief="solid")
entry_cantidad.grid(row=3, column=1, padx=6, pady=6)

tk.Label(form_frame, text="Proveedor", font=FONT_LABEL, bg="#ffffff", fg="#0f172a").grid(row=4, column=0, sticky="w", padx=6, pady=6)
entry_proveedor = tk.Entry(form_frame, font=FONT_ENTRY, width=28, bd=1, relief="solid")
entry_proveedor.grid(row=4, column=1, padx=6, pady=6)

# Action buttons (stacked)
btn_frame = tk.Frame(left_panel, bg="#ffffff")
btn_frame.pack(padx=12, pady=(6,12), fill="x")

def make_button(parent, text, cmd, bg="#0ea5a4"):
    return tk.Button(parent, text=text, command=cmd, bg=bg, fg="white", font=FONT_BTN, bd=0, relief="flat", padx=10, pady=8, cursor="hand2")

btn_add = make_button(btn_frame, "Agregar", agregar_producto, bg="#0ea5a4")
btn_add.grid(row=0, column=0, padx=6, pady=6, sticky="ew")
btn_update = make_button(btn_frame, "Actualizar", actualizar_producto, bg="#3b82f6")
btn_update.grid(row=0, column=1, padx=6, pady=6, sticky="ew")
btn_delete = make_button(btn_frame, "Eliminar", eliminar_producto, bg="#ef4444")
btn_delete.grid(row=1, column=0, padx=6, pady=6, sticky="ew")
btn_clear = make_button(btn_frame, "Limpiar", limpiar_campos, bg="#6b7280")
btn_clear.grid(row=1, column=1, padx=6, pady=6, sticky="ew")
# ---------- Right panel: Table & controls ----------
table_title = tk.Label(right_panel, text="Inventario", bg="#ffffff", fg="#0f172a", font=("Segoe UI Semibold", 12))
table_title.pack(anchor="w", padx=12, pady=(12,4))

# Contenedor de tabla
table_container = tk.Frame(right_panel, bg="#ffffff")
table_container.pack(fill="both", expand=True, padx=12, pady=(0,12))

# Definir columnas
columns = ("ID","Producto","Categoría","Precio","Cantidad","Proveedor")

tree = ttk.Treeview(table_container, columns=columns, show="headings", style="Clean.Treeview")

# Encabezados
for col in columns:
    tree.heading(col, text=col)

# Anchos ajustados
tree.column("ID", width=60, anchor="center")
tree.column("Producto", width=240, anchor="w")
tree.column("Categoría", width=160, anchor="w")
tree.column("Precio", width=120, anchor="e")
tree.column("Cantidad", width=120, anchor="center")
tree.column("Proveedor", width=220, anchor="w")

# Scrollbars
scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
scroll_x = ttk.Scrollbar(table_container, orient="horizontal", command=tree.xview)

tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

# Ubicación en la grilla
tree.grid(row=0, column=0, sticky="nsew")
scroll_y.grid(row=0, column=1, sticky="ns")
scroll_x.grid(row=1, column=0, sticky="ew")

table_container.grid_rowconfigure(0, weight=1)
table_container.grid_columnconfigure(0, weight=1)

# Alternancia de color
tree.tag_configure('evenrow', background='#ffffff')
tree.tag_configure('oddrow', background='#f1f5f9')

# Evento selección
tree.bind("<<TreeviewSelect>>", seleccionar_item)


# Small controls under table
controls = tk.Frame(right_panel, bg="#ffffff")
controls.pack(fill="x", padx=12, pady=(4,12))

btn_show_all = make_button(controls, "Mostrar Todo", mostrar_datos, bg="#10b981")
btn_show_all.pack(side="left", padx=6)

btn_export = make_button(controls, "Exportar CSV", export_csv, bg="#0ea5a4")
btn_export.pack(side="left", padx=6)

def ordenar_precio():
    # re-carga la tabla ordenando por precio asc
    for item in tree.get_children():
        tree.delete(item)
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nombre, categoria, precio, cantidad, proveedor FROM productos ORDER BY precio ASC")
                filas = cur.fetchall()
                for i, fila in enumerate(filas):
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    tree.insert("", tk.END, values=fila, tags=(tag,))
    except Exception as e:
        messagebox.showerror("Error", e)

btn_order_price = make_button(controls, "Ordenar por Precio", ordenar_precio, bg="#3b82f6")
btn_order_price.pack(side="left", padx=6)

# Status bar
status = tk.Label(root, text="Listo", bd=0, relief="flat", anchor="w", bg="#f7f9fb", fg="#475569", font=("Segoe UI", 9))
status.pack(fill="x", side="bottom", ipady=6, padx=6)

# Run initial load

root.mainloop()
