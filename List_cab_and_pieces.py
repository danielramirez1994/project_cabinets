import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk, messagebox
from tkinter import Canvas
import json
import os
from dibujar_gabinete import dibujar_gabinete
from tkinter import TclError

# Variables para las dimensiones de Canvas
Canvas_width = 800
Canvas_high = 500
drawer_mount = 0.375

class EstiloGabinete:
    """Clase base para diferentes estilos de gabinete"""
    def calcular_piezas(self, gabinete):
        raise NotImplementedError("Cada estilo debe implementar este método")
    
    def nombre(self):
        raise NotImplementedError("Cada estilo debe implementar este método")
    
class EstiloWallCabinet(EstiloGabinete):
    """Estilo de una gaveta y dos puertas"""
    def nombre(self):
        return "Wall_cabinet"
    
    def calcular_piezas(self, gabinete):
        gap = 0.125
        total = 30
        front = 2
        rear = 2
        top = 6
        botton = 6
        space = 1.26
        rows = 2
        dia = 0.25
        
        piezas = [
            {"nombre": "Lateral Izquierdo", "ancho": gabinete["Profundidad"], "alto": gabinete["Alto"],
             "orificios_shelf": {"cantidad": total, "diametro": dia, "filas": rows, "distancia_frontal": front, "distancia_trasera": rear, "separacion": space, "distancia_inferior": botton, "distancia_superior": top}},
            {"nombre": "Lateral Derecho", "ancho": gabinete["Profundidad"], "alto": gabinete["Alto"],
             "orificios_shelf": {"cantidad": total, "diametro": dia, "filas": rows, "distancia_frontal": front, "distancia_trasera": rear, "separacion": space, "distancia_inferior": botton, "distancia_superior": top}},
            {"nombre": "Base", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": gabinete["Profundidad"]},
            {"nombre": "Trasera", "ancho": gabinete["Ancho"], "alto": gabinete["Alto"] - gabinete["Espesor"]},
            {"nombre": "Entrepano", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": gabinete["Profundidad"]},
            {"nombre": "top", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": gabinete["Profundidad"]},
            {"nombre": "Rear Drawer Rail", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": 3}
        ]
        
        altura_puerta = (gabinete["Alto"]) - gap
        
        if gabinete["Ancho"] > 18:
            piezas.append({"nombre": "Puerta Izquierda", "ancho": (gabinete["Ancho"] / 2) - gap, "alto": altura_puerta})
            piezas.append({"nombre": "Puerta Derecha", "ancho": (gabinete["Ancho"] / 2) - gap, "alto": altura_puerta})
        else:
            piezas.append({"nombre": "Puerta", "ancho": gabinete["Ancho"] - gap, "alto": altura_puerta})
        
        return piezas

class EstiloUnaGavetaDosPuertas(EstiloGabinete):
    """Estilo de una o más gavetas y dos puertas"""
    def __init__(self):
        super().__init__()
        self.high_drawer_top = 5.875  # Altura predeterminada de la primera gaveta
        self.high_drawer_middle = 0.0  # Se calculará dinámicamente
        self.high_drawer_bottom = 0.0  # Se calculará dinámicamente
    
    def nombre(self):
        return "Base_1_Gav"
    
    def calcular_piezas(self, gabinete):
        toe_kick = 4
        gap = 0.125
        espacio_entre_gavetas = 0.25
        total = 6
        front = 2
        rear = 2
        top = 14
        botton = 12
        space = 1.26
        rows = 2
        dia = 0.25
        
        cantidad_gavetas = gabinete.get("num_gavetas", 1)
        altura_disponible = gabinete["Alto"] - toe_kick - ((cantidad_gavetas - 1) * espacio_entre_gavetas)
        
        alturas_gavetas = []
        for i in range(cantidad_gavetas):
            key = f"high_drawer_{i}"
            if key in gabinete:
                alturas_gavetas.append(gabinete[key])
            else:
                alturas_gavetas.append(altura_disponible / cantidad_gavetas)
        
        piezas = [
            {"nombre": "Lateral Izquierdo", "ancho": gabinete["Profundidad"] -1, "alto": gabinete["Alto"],
             "orificios_shelf": {"cantidad": total, "diametro": dia, "filas": rows, "distancia_frontal": front, "distancia_trasera": rear, "separacion": space, "distancia_inferior": botton, "distancia_superior": top}},
            {"nombre": "Lateral Derecho", "ancho": gabinete["Profundidad"] -1, "alto": gabinete["Alto"],
             "orificios_shelf": {"cantidad": total, "diametro": dia, "filas": rows, "distancia_frontal": front, "distancia_trasera": rear, "separacion": space, "distancia_inferior": botton, "distancia_superior": top}},
            {"nombre": "Base", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": gabinete["Profundidad"] -1},
            {"nombre": "Trasera", "ancho": gabinete["Ancho"], "alto": gabinete["Alto"] - gabinete["Espesor"]},
            {"nombre": "Entrepano", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": gabinete["Profundidad"]},
            {"nombre": "Toe Kick", "ancho": gabinete["Ancho"], "alto": 4},
            {"nombre": "Under Drawer Rail", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": 3},
            {"nombre": "Upper Drawer Rail", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": 3},
            {"nombre": "Rear Drawer Rail", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": 3}
        ]
        
        # Agregar las gavetas dinámicamente
        for i, altura_gaveta in enumerate(alturas_gavetas):
            piezas.append({"nombre": f"Drawer Face {i+1}", "ancho": gabinete["Ancho"] - gap, "alto": altura_gaveta})
        
        altura_puertas = altura_disponible - sum(alturas_gavetas) - ((cantidad_gavetas - 1) * espacio_entre_gavetas)
        if gabinete["Ancho"] > 18:
            piezas.append({"nombre": "Puerta Izquierda", "ancho": (gabinete["Ancho"] / 2) - gap, "alto": altura_puertas})
            piezas.append({"nombre": "Puerta Derecha", "ancho": (gabinete["Ancho"] / 2) - gap, "alto": altura_puertas})
        else:
            piezas.append({"nombre": "Puerta", "ancho": gabinete["Ancho"] - gap, "alto": altura_puertas})

        # Determinar profundidad para las cajas de gavetas
        profundidad_box_drawer = 21
        if gabinete["Profundidad"] > 26:
            profundidad_box_drawer = 24
        elif gabinete["Profundidad"] > 23:
            profundidad_box_drawer = 21
        elif gabinete["Profundidad"] > 20:
            profundidad_box_drawer = 18
        elif gabinete["Profundidad"] > 17:
            profundidad_box_drawer = 15
        elif gabinete["Profundidad"] > 14:
            profundidad_box_drawer = 12
        elif gabinete["Profundidad"] > 11:
            profundidad_box_drawer = 9

        # Agregar las cajas de gavetas dinámicamente
        for i, _ in enumerate(alturas_gavetas):
            piezas.append({
                "nombre": f"Box Drawer {i+1}",
                "ancho": gabinete["Ancho"] - drawer_mount - (gabinete["Espesor"] * 2),
                "alto": 4,
                "profundidad": profundidad_box_drawer
            })
                
        return piezas


class EstiloTresGavetas(EstiloGabinete):
    """Estilo de tres gavetas"""
    def __init__(self):
        super().__init__()
        self.high_drawer_top = 5.875     # Valor predeterminado para gaveta superior
        self.high_drawer_middle = 0.0    # Se calculará dinámicamente
        self.high_drawer_bottom = 0.0    # Se calculará dinámicamente
    
    def nombre(self):
        return "Base_3_Gav"
    
    def calcular_piezas(self, gabinete):
        gap = 0.125
        toe_kick = 4
        espacio_entre_gavetas = 0.25
        total = 6
        front = 2
        rear = 2
        top = 14
        botton = 12
        space = 1.26
        rows = 2
        dia = 0.25
        
        # Calcular altura de cada gaveta
        altura_disponible = gabinete["Alto"] - toe_kick - (2 * espacio_entre_gavetas)
        
        # Usar el valor de los atributos de altura si están disponibles
        high_drawer_top = gabinete.get("high_drawer_top", self.high_drawer_top)

        
        # Si las alturas de las gavetas media e inferior ya están definidas, usarlas
        high_drawer_middle = gabinete.get("high_drawer_middle")
        high_drawer_bottom = gabinete.get("high_drawer_bottom")

        if high_drawer_middle is None or high_drawer_bottom is None:
            espacio_restante = altura_disponible - high_drawer_top
            high_drawer_middle = espacio_restante / 2
            high_drawer_bottom = espacio_restante / 2

            
            # Guardar los valores calculados
            self.high_drawer_middle = high_drawer_middle
            self.high_drawer_bottom = high_drawer_bottom
        
        piezas = [
            {"nombre": "Lateral Izquierdo", "ancho": gabinete["Profundidad"] -1, "alto": gabinete["Alto"],
             "orificios_shelf": {"cantidad": total, "diametro": dia, "filas": rows, "distancia_frontal": front, "distancia_trasera": rear, "separacion": space, "distancia_inferior": botton, "distancia_superior": top}},
            {"nombre": "Lateral Derecho", "ancho": gabinete["Profundidad"] -1, "alto": gabinete["Alto"],
             "orificios_shelf": {"cantidad": total, "diametro": dia, "filas": rows, "distancia_frontal": front, "distancia_trasera": rear, "separacion": space, "distancia_inferior": botton, "distancia_superior": top}},
            {"nombre": "Base", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": gabinete["Profundidad"] -1},
            {"nombre": "Trasera", "ancho": gabinete["Ancho"], "alto": gabinete["Alto"] - gabinete["Espesor"]},
            {"nombre": "Drawer Face Superior", "ancho": gabinete["Ancho"] - gap, "alto": high_drawer_top},
            {"nombre": "Drawer Face Media", "ancho": gabinete["Ancho"] - gap, "alto": high_drawer_middle},
            {"nombre": "Drawer Face Inferior", "ancho": gabinete["Ancho"] - gap, "alto": high_drawer_bottom},
            {"nombre": "Under Drawer Rail Superior", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": 3},
            {"nombre": "Upper Drawer Rail Superior", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": 3},
            {"nombre": "Rear Drawer Rail Superior", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": 3},
            {"nombre": "Under Drawer Rail Media", "ancho": gabinete["Ancho"] - 2 * gabinete["Espesor"], "alto": 3},
            {"nombre": "Toe Kick", "ancho": gabinete["Ancho"], "alto": toe_kick},
        ]
        
        # Determinar profundidad para las cajas de gavetas
        profundidad_box_drawer = 21
        if gabinete["Profundidad"] > 26:
            profundidad_box_drawer = 24
        elif gabinete["Profundidad"] > 23:
            profundidad_box_drawer = 21
        elif gabinete["Profundidad"] > 20:
            profundidad_box_drawer = 18
        elif gabinete["Profundidad"] > 17:
            profundidad_box_drawer = 15
        elif gabinete["Profundidad"] > 14:
            profundidad_box_drawer = 12
        elif gabinete["Profundidad"] > 11:
            profundidad_box_drawer = 9
            
            
        if high_drawer_top < 8:
            restar1 = 1.875
        else:
            restar1 = 2.75
            
        if high_drawer_middle < 8:
            restar2 = 1.875
        else:
            restar2 = 2.75
            
        if high_drawer_bottom < 8:
            restar3 = 1.875
        else:
            restar3 = 2.75
        
        # Añadir las cajas de gavetas
        piezas.append({"nombre": "Box Drawer Superior", "ancho": gabinete["Ancho"] - drawer_mount - (gabinete["Espesor"] * 2), "alto": high_drawer_top - restar1, "profundidad": profundidad_box_drawer})
        piezas.append({"nombre": "Box Drawer Media", "ancho": gabinete["Ancho"] - drawer_mount - (gabinete["Espesor"] * 2), "alto": high_drawer_middle - restar2, "profundidad": profundidad_box_drawer})
        piezas.append({"nombre": "Box Drawer Inferior", "ancho": gabinete["Ancho"] - drawer_mount - (gabinete["Espesor"] * 2), "alto": high_drawer_bottom - restar3, "profundidad": profundidad_box_drawer})
        
        return piezas
    
class GestorGabinetes:
    """Clase para gestionar los diferentes estilos de gabinetes"""
    def __init__(self):
        self.estilos = {
            "Base_1_Gav": EstiloUnaGavetaDosPuertas(),
            "Base_3_Gav": EstiloTresGavetas(),
            "Wall_cabinet": EstiloWallCabinet()
        }
        self.estilo_actual = "Base_1_Gav"
    
    def cambiar_estilo(self, nombre_estilo):
        """Cambia el estilo del gabinete"""
        if nombre_estilo in self.estilos:
            self.estilo_actual = nombre_estilo
            return True
        return False
    
    def calcular_piezas(self, gabinete):
        estilo_gabinete = gabinete["Estilo"]  # Cada gabinete tiene su propio estilo
        if estilo_gabinete in self.estilos:
            return self.estilos[estilo_gabinete].calcular_piezas(gabinete)
        else:
            raise ValueError(f"El estilo '{estilo_gabinete}' no existe en los estilos registrados.")
    
    def obtener_estilos_disponibles(self):
        """Devuelve la lista de estilos disponibles"""
        return list(self.estilos.keys())
    
    def obtener_nombres_estilos(self):
        """Devuelve un diccionario con los nombres descriptivos de los estilos"""
        return {key: estilo.nombre() for key, estilo in self.estilos.items()}

class GabineteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Piezas para Gabinetes")
        
        # Inicializar el gestor de estilos
        self.gestor_gabinetes = GestorGabinetes()
        
        # Variables y datos
        self.gabinetes = []  # Lista de gabinetes
        self.vista_actual = "frontal"
        self.gabinete_actual = None
        self.piezas_actual = None
        self.pieza_seleccionada = None
        
        # Configuración para el autoguardado
        self.archivo_temp = "temp_gabinetes.json"  # Archivo temporal predeterminado
        
        # Marco izquierdo para controles y tablas
        frame_izquierdo = ttk.Frame(root)
        frame_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
        
        # Marco derecho para visualización y botones
        frame_derecho = ttk.Frame(root)
        frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="nse")
        
        # Marco derecho para visualización y botones
        frame_datosentrada = ttk.Frame(frame_izquierdo)
        frame_datosentrada.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        # Etiquetas y campos de entrada
        ttk.Label(frame_datosentrada, text="Ancho (in):").grid(row=0, column=0, sticky="w")
        self.ancho_var = tk.DoubleVar(value=16)
        ttk.Entry(frame_datosentrada, textvariable=self.ancho_var).grid(row=0, column=1)

        ttk.Label(frame_datosentrada, text="Alto (in):").grid(row=1, column=0, sticky="w")
        self.alto_var = tk.DoubleVar(value=34.5)
        ttk.Entry(frame_datosentrada, textvariable=self.alto_var).grid(row=1, column=1)

        ttk.Label(frame_datosentrada, text="Profundidad (in):").grid(row=2, column=0, sticky="w")
        self.profundidad_var = tk.DoubleVar(value=24)
        ttk.Entry(frame_datosentrada, textvariable=self.profundidad_var).grid(row=2, column=1)

        ttk.Label(frame_datosentrada, text="Espesor material (in):").grid(row=3, column=0, sticky="w")
        self.espesor_var = tk.DoubleVar(value=0.75)
        ttk.Entry(frame_datosentrada, textvariable=self.espesor_var).grid(row=3, column=1)
        
        ttk.Label(frame_datosentrada, text="Cantidad:").grid(row=4, column=0, sticky="w")
        self.cantidad_var = tk.IntVar(value=1)
        ttk.Entry(frame_datosentrada, textvariable=self.cantidad_var).grid(row=4, column=1)

        # Selector de estilo (ComboBox)
        ttk.Label(frame_datosentrada, text="Estilo de gabinete:").grid(row=5, column=0, sticky="w")
        
        # Obtener nombres descriptivos de los estilos
        nombres_estilos = self.gestor_gabinetes.obtener_nombres_estilos()
        self.estilo_keys = list(nombres_estilos.keys())
        self.estilo_values = [nombres_estilos[key] for key in self.estilo_keys]
        
        self.estilo_var = tk.StringVar()
        self.combo_estilo = ttk.Combobox(frame_datosentrada, textvariable=self.estilo_var, values=self.estilo_values)
        self.combo_estilo.current(0)  # Establecer el primer estilo como predeterminado
        self.combo_estilo.grid(row=5, column=1, sticky="s")
        self.combo_estilo.bind("<<ComboboxSelected>>", self.cambiar_estilo)
        
        # Marco izquierdo para controles y tablas
        frame_inizquierdo = ttk.Frame(frame_izquierdo)
        frame_inizquierdo.grid(row=5, column=0, padx=10, pady=10, sticky="nsw")
        
        ttk.Label(frame_inizquierdo, text="Seleccionar Estilo de Drawer Slider").grid(row=0, column=0, columnspan=2, sticky="w")

        # Botón para agregar gabinete
        ttk.Button(frame_inizquierdo, text="Agregar Gabinete", command=self.agregar_gabinete).grid(
            row=1, column=2, pady=10, padx=(50, 0), sticky="e")
        
        # Opciones de radio dispuestas horizontalmente
        self.option_value = tk.StringVar(value="Undermount")
        fractions = {"Undermount": 0.375, "Sidemount": 1}

        col = 0  # Iniciar en la columna 0
        for fraction, value in fractions.items():
            ttk.Radiobutton(frame_inizquierdo, text=fraction, variable=self.option_value, value=fraction,
                            command=lambda v=value: self.update_entry_value(v)).grid(row=1, column=col, padx=10, pady=10)
            col += 1  # Incrementar la columna para el siguiente botón

        # Tabla para lista de gabinetes
        self.tree_gabinetes = ttk.Treeview(frame_izquierdo, columns=("ID", "Ancho", "Alto", "Profundidad", "Estilo", "Cantidad"), show="headings")
        self.tree_gabinetes.heading("ID", text="ID")
        self.tree_gabinetes.heading("Ancho", text="Ancho (in)")
        self.tree_gabinetes.heading("Alto", text="Alto (in)")
        self.tree_gabinetes.heading("Profundidad", text="Profundidad (in)")
        self.tree_gabinetes.heading("Estilo", text="Estilo")
        self.tree_gabinetes.heading("Cantidad", text="Cantidad")
        self.tree_gabinetes.grid(row=6, column=0, columnspan=2, pady=5)
        self.tree_gabinetes.bind("<ButtonRelease-1>", self.mostrar_piezas)
        self.tree_gabinetes.bind("<Button-3>", self.mostrar_menu_contextual)
        
        # Ajustar el tamaño de las columnas
        self.tree_gabinetes.column("ID", width=40)
        self.tree_gabinetes.column("Ancho", width=60)
        self.tree_gabinetes.column("Alto", width=60)
        self.tree_gabinetes.column("Profundidad", width=60)
        self.tree_gabinetes.column("Estilo", width=120)
        self.tree_gabinetes.column("Cantidad", width=40)
        
        ttk.Button(frame_izquierdo, text="Cambiar Estilo del Gabinete", command=self.cambiar_estilo_gabinete_seleccionado).grid(row=7, column=0, columnspan=2, pady=10)

        # Tabla para mostrar piezas del gabinete seleccionado
        self.tree_piezas = ttk.Treeview(frame_izquierdo, columns=("Nombre", "Ancho", "Alto", "Profundidad"), show="headings")
        self.tree_piezas.heading("Nombre", text="Nombre")
        self.tree_piezas.heading("Ancho", text="Ancho (in)")
        self.tree_piezas.heading("Alto", text="Alto (in)")
        self.tree_piezas.heading("Profundidad", text="Profundidad (in)")
        self.tree_piezas.grid(row=8, column=0, columnspan=2, pady=5)
        

        # Ajustar el tamaño de las columnas
        self.tree_piezas.column("Nombre", width=150)
        self.tree_piezas.column("Ancho", width=100)
        self.tree_piezas.column("Alto", width=100)
        self.tree_piezas.column("Profundidad", width=100)

        # Botón para editar gabinetes y cambiar vistas
        ttk.Button(frame_derecho, text="Vista Frontal", command=lambda: self.cambiar_vista("frontal")).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(frame_derecho, text="Vista Lateral", command=lambda: self.cambiar_vista("lateral")).grid(row=2, column=0, columnspan=2, pady=10)

        # Canvas para visualización 2D
        self.canvas = tk.Canvas(frame_derecho, width=Canvas_width, height=Canvas_high, bg='white')
        self.canvas.grid(row=5, column=0, columnspan=2, pady=10)

        # Botones para guardar y cargar datos
        ttk.Button(frame_derecho, text="Guardar Datos", command=self.guardar_datos).grid(row=6, column=0, pady=5, sticky="w")
        ttk.Button(frame_derecho, text="Cargar Datos", command=self.cargar_datos_temporales).grid(row=6, column=1, pady=5, sticky="w")
        ttk.Button(frame_derecho, text="Eliminar datos", command=self.limpiar_tabla).grid(row=7, column=1, pady=5, sticky="w")
        
        # Cargar datos guardados automáticamente (si existen)
        # self.cargar_datos_temporales()
        
    def update_entry_value(self, value):
        """Actualiza el valor del campo de entrada y la variable drawer_mount cuando se selecciona una opción"""
        global drawer_mount
        drawer_mount = value
        
        print(f"drawer_mount actualizado a: {drawer_mount}")
        
    def cambiar_estilo(self, event=None):
        # Este método se llama cuando se selecciona un estilo del combobox
        selected_index = self.combo_estilo.current()
        if selected_index >= 0:
            selected_key = self.estilo_keys[selected_index]
            self.gestor_gabinetes.cambiar_estilo(selected_key)
                
    def cambiar_estilo_gabinete_seleccionado(self):
        selected_item = self.tree_gabinetes.selection()
        if not selected_item:
            messagebox.showinfo("Información", "Por favor seleccione un gabinete para cambiar su estilo.")
            return

        item = self.tree_gabinetes.item(selected_item)
        gabinete_id = item["values"][0]

        gabinete = next((g for g in self.gabinetes if g["ID"] == gabinete_id), None)
        if not gabinete:
            messagebox.showerror("Error", "No se encontró el gabinete seleccionado.")
            return

        ventana_estilo = tk.Toplevel(self.root)
        ventana_estilo.title("Modificar Gabinete")
        ventana_estilo.geometry("450x550")

        self.loading_values = False
        # Variable para rastrear qué campos han sido modificados manualmente
        campos_modificados = set()

        # 🔹 ComboBox para seleccionar el estilo
        ttk.Label(ventana_estilo, text="Seleccione el nuevo estilo:").pack(pady=5)
        combo_estilo = ttk.Combobox(ventana_estilo, values=self.estilo_values)
        combo_estilo.current(self.estilo_keys.index(gabinete["Estilo"]))
        combo_estilo.pack(pady=5)

        # 🔹 Frame para dimensiones
        frame_dimensiones = ttk.LabelFrame(ventana_estilo, text="Dimensiones del Gabinete")
        frame_dimensiones.pack(fill=tk.X, padx=10, pady=5)

        # Ancho
        frame_ancho = ttk.Frame(frame_dimensiones)
        frame_ancho.pack(fill=tk.X, pady=2)
        ttk.Label(frame_ancho, text="Ancho (in):").pack(side=tk.LEFT, padx=5)
        entry_ancho = ttk.Entry(frame_ancho)
        entry_ancho.insert(0, str(gabinete["Ancho"]))
        entry_ancho.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)

        # Alto
        frame_alto = ttk.Frame(frame_dimensiones)
        frame_alto.pack(fill=tk.X, pady=2)
        ttk.Label(frame_alto, text="Alto (in):").pack(side=tk.LEFT, padx=5)
        entry_alto = ttk.Entry(frame_alto)
        entry_alto.insert(0, str(gabinete["Alto"]))
        entry_alto.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)

        # Profundidad
        frame_prof = ttk.Frame(frame_dimensiones)
        frame_prof.pack(fill=tk.X, pady=2)
        ttk.Label(frame_prof, text="Profundidad (in):").pack(side=tk.LEFT, padx=5)
        entry_profundidad = ttk.Entry(frame_prof)
        entry_profundidad.insert(0, str(gabinete["Profundidad"]))
        entry_profundidad.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        
        # Cantidad
        frame_cantidad = ttk.Frame(frame_dimensiones)
        frame_cantidad.pack(fill=tk.X, pady=2)
        ttk.Label(frame_cantidad, text="Cantidad:").pack(side=tk.LEFT, padx=5)
        entry_cantidad = ttk.Entry(frame_cantidad)
        entry_cantidad.insert(0, str(gabinete["Cantidad"]))
        entry_cantidad.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)

        # 🆕 Sección para seleccionar cantidad de gavetas (para estilos con gavetas)
        frame_num_gavetas = ttk.Frame(ventana_estilo)
        ttk.Label(frame_num_gavetas, text="Cantidad de gavetas:").pack(side=tk.LEFT, padx=5)
        combo_num_gavetas = ttk.Combobox(frame_num_gavetas, values=["1", "2", "3", "4", "5"], width=5)
        combo_num_gavetas.pack(side=tk.LEFT, padx=5)
        frame_num_gavetas.pack(fill=tk.X, padx=10, pady=5)
        
        # Por defecto, seleccionamos el valor original o el valor guardado
        num_gavetas_actual = gabinete.get("num_gavetas", 1)  # Por defecto 1 para Base_1_Gav, 3 para Base_3_Gav
        if gabinete["Estilo"] == "Base_3_Gav" and "num_gavetas" not in gabinete:
            num_gavetas_actual = 3
        combo_num_gavetas.current(min(num_gavetas_actual, 5) - 1)

        # 🔹 Sección para alturas de gavetas
        frame_gavetas = ttk.LabelFrame(ventana_estilo, text="Alturas de Gavetas")
        
        # Constantes
        TOE_KICK = 4
        ESPACIO_ENTRE_GAVETAS = 0.25
        ESPACIO_SUPERIOR_GAVETA = 0.25  # Espacio arriba de la primera gaveta (para Base_1_Gav)
        GAP = 0.125
        
        # Crear un frame contenedor para las gavetas que se mostrarán/ocultarán dinámicamente
        frame_container_gavetas = ttk.Frame(frame_gavetas)
        frame_container_gavetas.pack(fill=tk.X, pady=5)
        
        # Diccionario para almacenar entradas de gavetas y sus variables
        gavetas_entries = {}
        gavetas_vars = {}
        
        # 🆕 Sección para las puertas (para estilo Base_1_Gav)
        frame_puertas = ttk.LabelFrame(ventana_estilo, text="Configuración de Puertas")
        frame_container_puertas = ttk.Frame(frame_puertas)
        frame_container_puertas.pack(fill=tk.X, pady=5)
        
        # Variables para puertas
        var_altura_puerta = tk.DoubleVar()
        var_tiene_dos_puertas = tk.BooleanVar(value=gabinete.get("dos_puertas", gabinete["Ancho"] > 18))
        
        # Variables para mostrar información
        var_espacio_disponible = tk.StringVar()
        var_espacio_utilizado = tk.StringVar()
        var_espacio_restante = tk.StringVar()
        var_espacio_puertas = tk.StringVar()
        
        # Función para crear UI de gavetas según la cantidad seleccionada
        def crear_ui_gavetas(cantidad):
            nonlocal gavetas_entries, gavetas_vars, campos_modificados
            
            # Limpiar entradas anteriores
            for widget in frame_container_gavetas.winfo_children():
                widget.destroy()
                
            gavetas_entries = {}
            gavetas_vars = {}
            campos_modificados = set()  # Resetear campos modificados al cambiar el número de gavetas
            
            # Crear entradas para cada gaveta
            for i in range(cantidad):
                posicion = "Superior" if i == 0 else "Inferior" if i == cantidad-1 else f"Media {i}"
                if cantidad == 1:
                    posicion = "Única"
                    
                var = tk.DoubleVar()
                gavetas_vars[i] = var
                
                ttk.Label(frame_container_gavetas, text=f"Drawer Face {posicion}:").pack(pady=2)
                entry = ttk.Entry(frame_container_gavetas, textvariable=var)
                entry.pack(pady=2, fill=tk.X, padx=10)
                gavetas_entries[i] = entry
                
                # Asignar un identificador de índice para rastrear
                entry.idx = i
                
                # Vincular eventos de edición
                entry.bind("<FocusIn>", registrar_campo_para_edicion)
                entry.bind("<FocusOut>", calcular_alturas)
                entry.bind("<Return>", handle_enter)
        
        # Función para crear UI de puertas
        def crear_ui_puertas():
            for widget in frame_container_puertas.winfo_children():
                widget.destroy()
            
            # Opción para determinar si usar una o dos puertas
            frame_opcion_puertas = ttk.Frame(frame_container_puertas)
            frame_opcion_puertas.pack(fill=tk.X, pady=5)
            
            ttk.Checkbutton(frame_opcion_puertas, text="Usar dos puertas", variable=var_tiene_dos_puertas,
                        command=calcular_alturas).pack(side=tk.LEFT, padx=5)
            
            # Indicador de altura de puerta
            frame_altura_puerta = ttk.Frame(frame_container_puertas)
            frame_altura_puerta.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame_altura_puerta, text="Altura de puerta(s):").pack(side=tk.LEFT, padx=5)
            lbl_altura_puerta = ttk.Label(frame_altura_puerta, textvariable=var_espacio_puertas)
            lbl_altura_puerta.pack(side=tk.LEFT, padx=5)
            
            # Información sobre ancho de puertas
            frame_ancho_puertas = ttk.Frame(frame_container_puertas)
            frame_ancho_puertas.pack(fill=tk.X, pady=5)
            
            if var_tiene_dos_puertas.get():
                ancho_puerta = (float(entry_ancho.get()) / 2) - GAP
                ttk.Label(frame_ancho_puertas, 
                        text=f"Ancho de cada puerta: {ancho_puerta:.3f} in").pack(side=tk.LEFT, padx=5)
            else:
                ancho_puerta = float(entry_ancho.get()) - GAP
                ttk.Label(frame_ancho_puertas, 
                        text=f"Ancho de la puerta: {ancho_puerta:.3f} in").pack(side=tk.LEFT, padx=5)
        
        # Función para marcar un campo como siendo editado
        def registrar_campo_para_edicion(event):
            # Identificar qué campo está siendo editado
            widget = event.widget
            if hasattr(widget, 'idx'):
                # No hacer nada más, solo registrar que este campo está siendo editado
                pass

        # Función para calcular alturas cuando cambia cualquier valor
        def calcular_alturas(event=None):
            if self.loading_values:
                return
            try:
                # Si hay un evento, identificar qué campo acaba de ser modificado
                if event and hasattr(event.widget, 'idx'):
                    campos_modificados.add(event.widget.idx)
                
                estilo_seleccionado = self.estilo_keys[combo_estilo.current()]
                cantidad_gavetas = int(combo_num_gavetas.get())
                altura_gabinete = float(entry_alto.get())
                
                if estilo_seleccionado == "Base_3_Gav":
                    # Cálculo para estilo Base_3_Gav
                    espacios_entre_gavetas = (cantidad_gavetas - 1) * ESPACIO_ENTRE_GAVETAS
                    altura_disponible = altura_gabinete - TOE_KICK - espacios_entre_gavetas
                    
                    var_espacio_disponible.set(f"Espacio disponible total: {altura_disponible:.3f} in")
                    
                    # Obtener valores actuales de todas las gavetas
                    alturas_gavetas = {}
                    for idx, entry in gavetas_entries.items():
                        try:
                            alturas_gavetas[idx] = float(entry.get())
                        except ValueError:
                            alturas_gavetas[idx] = 0.0
                    
                    # Calcular espacio total usado por campos ya modificados
                    espacio_usado_por_modificados = 0
                    for idx in campos_modificados:
                        if idx in alturas_gavetas:
                            espacio_usado_por_modificados += alturas_gavetas[idx]
                    
                    # Calcular espacio restante para distribuir entre campos no modificados
                    espacio_restante = altura_disponible - espacio_usado_por_modificados
                    campos_no_modificados = [idx for idx in range(cantidad_gavetas) if idx not in campos_modificados]
                    
                    # Si hay campos no modificados, distribuir equitativamente
                    if campos_no_modificados and espacio_restante > 0:
                        altura_por_gaveta = espacio_restante / len(campos_no_modificados)
                        for idx in campos_no_modificados:
                            alturas_gavetas[idx] = altura_por_gaveta
                    
                    # Actualizar todas las entradas
                    for idx, altura in alturas_gavetas.items():
                        gavetas_vars[idx].set(round(altura, 3))
                        gavetas_entries[idx].delete(0, tk.END)
                        gavetas_entries[idx].insert(0, f"{altura:.3f}")
                    
                    # Calcular espacio utilizado total y restante
                    espacio_utilizado = sum(alturas_gavetas.values())
                    espacio_restante_final = altura_disponible - espacio_utilizado
                    
                    var_espacio_utilizado.set(f"Espacio utilizado: {espacio_utilizado:.3f} in")
                    var_espacio_restante.set(f"Espacio restante: {espacio_restante_final:.3f} in")
                    
                    # Cambiar el color del texto según el espacio restante
                    if espacio_restante_final < -0.001:  # Un pequeño margen para evitar problemas de redondeo
                        lbl_espacio_restante.config(foreground="red")
                        lbl_advertencia.config(text="¡Advertencia! El espacio utilizado excede el disponible.")
                    else:
                        lbl_espacio_restante.config(foreground="green")
                        lbl_advertencia.config(text="")
                
                elif estilo_seleccionado == "Base_1_Gav":
                    # Cálculo para estilo Base_1_Gav
                    espacios_entre_gavetas = (cantidad_gavetas - 1) * ESPACIO_ENTRE_GAVETAS
                    # El espacio disponible para las gavetas ahora depende de la cantidad
                    altura_disponible_total = altura_gabinete - TOE_KICK - ESPACIO_SUPERIOR_GAVETA
                    
                    # Obtener valores actuales de todas las gavetas
                    alturas_gavetas = {}
                    for idx, entry in gavetas_entries.items():
                        try:
                            alturas_gavetas[idx] = float(entry.get())
                        except ValueError:
                            alturas_gavetas[idx] = 0.0
                    
                    # Calcular espacio total usado por campos ya modificados
                    espacio_usado_por_modificados = 0
                    for idx in campos_modificados:
                        if idx in alturas_gavetas:
                            espacio_usado_por_modificados += alturas_gavetas[idx]
                    
                    # Si no hay gavetas modificadas, usar valores predeterminados
                    if not campos_modificados:
                        # Definir cuánto espacio total queremos para gavetas (por ejemplo, 30% del espacio disponible)
                        porcentaje_gavetas = gabinete.get("porcentaje_gavetas", 0.3)  # 30% por defecto para gavetas
                        espacio_gavetas = altura_disponible_total * porcentaje_gavetas
                        altura_por_gaveta = (espacio_gavetas - espacios_entre_gavetas) / cantidad_gavetas
                        
                        for idx in range(cantidad_gavetas):
                            alturas_gavetas[idx] = altura_por_gaveta
                    else:
                        # Ya hay gavetas modificadas, solo ajustar las no modificadas
                        campos_no_modificados = [idx for idx in range(cantidad_gavetas) if idx not in campos_modificados]
                        if campos_no_modificados:
                            # Usar el mismo porcentaje de espacio para gavetas que el actual
                            espacio_usado_gavetas = espacio_usado_por_modificados + (espacios_entre_gavetas)
                            if len(campos_modificados) < cantidad_gavetas:
                                espacio_por_gaveta = espacio_usado_por_modificados / len(campos_modificados)
                                espacio_restante_gavetas = (espacio_por_gaveta * cantidad_gavetas) - espacio_usado_por_modificados
                                altura_por_gaveta = espacio_restante_gavetas / len(campos_no_modificados)
                                
                                for idx in campos_no_modificados:
                                    alturas_gavetas[idx] = altura_por_gaveta
                    
                    # Calcular espacio total usado por gavetas
                    espacio_utilizado_gavetas = sum(alturas_gavetas.values()) + espacios_entre_gavetas
                    
                    # Actualizar todas las entradas de gavetas
                    for idx, altura in alturas_gavetas.items():
                        gavetas_vars[idx].set(round(altura, 3))
                        gavetas_entries[idx].delete(0, tk.END)
                        gavetas_entries[idx].insert(0, f"{altura:.3f}")
                    
                    # Calcular el espacio restante para las puertas
                    espacio_puertas = altura_disponible_total - espacio_utilizado_gavetas - GAP
                    var_altura_puerta.set(espacio_puertas)
                    
                    # Actualizar las variables de información
                    var_espacio_disponible.set(f"Espacio disponible total: {altura_disponible_total:.3f} in")
                    var_espacio_utilizado.set(f"Espacio utilizado por gavetas: {espacio_utilizado_gavetas:.3f} in")
                    var_espacio_puertas.set(f"{espacio_puertas:.3f} in")
                    
                    # Actualizar la interfaz de puertas
                    crear_ui_puertas()
                    
                    # Validar si el espacio es suficiente para gavetas y puertas
                    if espacio_puertas < 1.0:  # Menos de 1 pulgada para puertas no es práctico
                        lbl_advertencia.config(text="¡Advertencia! Las gavetas ocupan demasiado espacio. Espacio insuficiente para puertas.")
                        lbl_espacio_restante.config(foreground="red")
                    else:
                        lbl_advertencia.config(text="")
                        lbl_espacio_restante.config(foreground="green")
                    
                # Validar valores
                validar_valores()

            except ValueError as e:
                lbl_advertencia.config(text=f"Error de cálculo: {str(e)}")

        # Función para validar valores
        def validar_valores(*args):
            try:
                # Verificar que la altura del gabinete sea suficiente
                altura_gabinete = float(entry_alto.get())
                estilo_seleccionado = self.estilo_keys[combo_estilo.current()]
                cantidad_gavetas = int(combo_num_gavetas.get())
                
                if estilo_seleccionado == "Base_3_Gav":
                    espacios_entre_gavetas = (cantidad_gavetas - 1) * ESPACIO_ENTRE_GAVETAS
                    espacio_minimo = TOE_KICK + espacios_entre_gavetas
                    
                    if altura_gabinete < espacio_minimo:
                        lbl_advertencia.config(text=f"¡Advertencia! La altura mínima del gabinete debe ser {espacio_minimo} in para acomodar el toe kick y espacios entre gavetas.")
                
                elif estilo_seleccionado == "Base_1_Gav":
                    espacios_entre_gavetas = (cantidad_gavetas - 1) * ESPACIO_ENTRE_GAVETAS
                    espacio_minimo = TOE_KICK + ESPACIO_SUPERIOR_GAVETA + espacios_entre_gavetas + 1  # Al menos 1 in para puerta
                    
                    if altura_gabinete < espacio_minimo:
                        lbl_advertencia.config(text=f"¡Advertencia! La altura mínima debe ser {espacio_minimo} in para acomodar toe kick, gavetas y puertas.")
                
                # Verificar que ninguna gaveta tenga altura negativa
                for idx, var in gavetas_vars.items():
                    if var.get() < 0:
                        lbl_advertencia.config(text="¡Advertencia! La altura de alguna gaveta es negativa. Ajuste los valores.")
                        break
            except ValueError:
                pass

        # Función para manejar el evento Enter
        def handle_enter(event):
            if hasattr(event.widget, 'idx'):
                campos_modificados.add(event.widget.idx)
            calcular_alturas()
            return "break"

        entry_alto.bind("<Return>", handle_enter)

        # Separador
        ttk.Separator(frame_gavetas, orient="horizontal").pack(fill=tk.X, pady=5)
        
        # Frame para mostrar información sobre espacio
        frame_info = ttk.Frame(frame_gavetas)
        frame_info.pack(fill=tk.X, pady=5)
        
        # Labels para información de espacio
        lbl_espacio_disponible = ttk.Label(frame_info, textvariable=var_espacio_disponible)
        lbl_espacio_disponible.pack(anchor=tk.W, pady=2)
        
        lbl_espacio_utilizado = ttk.Label(frame_info, textvariable=var_espacio_utilizado)
        lbl_espacio_utilizado.pack(anchor=tk.W, pady=2)
        
        lbl_espacio_restante = ttk.Label(frame_info, textvariable=var_espacio_restante)
        lbl_espacio_restante.pack(anchor=tk.W, pady=2)
        
        # Etiquetas de ayuda
        ttk.Label(frame_gavetas, text="Edite los valores de cualquier gaveta. Los campos que no modifique se ajustarán automáticamente.", 
                wraplength=420, font=("", 8)).pack(pady=5)
        
        ttk.Label(frame_gavetas, text="Presione Enter después de ingresar un valor para actualizar los cálculos", 
                wraplength=420, font=("", 8), foreground="blue").pack(pady=5)
        
        # Frame para advertencias
        frame_advertencia = ttk.Frame(frame_gavetas)
        frame_advertencia.pack(fill=tk.X, pady=5)
        lbl_advertencia = ttk.Label(frame_advertencia, text="", foreground="red", wraplength=420)
        lbl_advertencia.pack(anchor=tk.W)

        # Función para resetear las modificaciones y distribuir equitativamente
        def resetear_valores():
            nonlocal campos_modificados
            campos_modificados = set()
            
            try:
                estilo_seleccionado = self.estilo_keys[combo_estilo.current()]
                cantidad_gavetas = int(combo_num_gavetas.get())
                altura_gabinete = float(entry_alto.get())
                
                if estilo_seleccionado == "Base_3_Gav":
                    espacios_entre_gavetas = (cantidad_gavetas - 1) * ESPACIO_ENTRE_GAVETAS
                    altura_disponible = altura_gabinete - TOE_KICK - espacios_entre_gavetas
                    altura_por_gaveta = altura_disponible / cantidad_gavetas
                
                elif estilo_seleccionado == "Base_1_Gav":
                    # Para Base_1_Gav, usar sólo un porcentaje del espacio para gavetas
                    espacios_entre_gavetas = (cantidad_gavetas - 1) * ESPACIO_ENTRE_GAVETAS
                    altura_disponible_total = altura_gabinete - TOE_KICK - ESPACIO_SUPERIOR_GAVETA
                    
                    # Por defecto, usar 30% del espacio para gavetas
                    porcentaje_gavetas = gabinete.get("porcentaje_gavetas", 0.3)
                    espacio_gavetas = altura_disponible_total * porcentaje_gavetas
                    altura_por_gaveta = (espacio_gavetas - espacios_entre_gavetas) / cantidad_gavetas
                
                # Actualizar todas las gavetas con la misma altura
                for idx in range(cantidad_gavetas):
                    gavetas_vars[idx].set(round(altura_por_gaveta, 3))
                    gavetas_entries[idx].delete(0, tk.END)
                    gavetas_entries[idx].insert(0, f"{altura_por_gaveta:.3f}")
                
                calcular_alturas()
            except ValueError:
                pass
        
        # Añadir botón para resetear valores
        ttk.Button(frame_gavetas, text="Distribuir equitativamente", command=resetear_valores).pack(pady=5)

        # Función para actualizar la UI cuando cambia la cantidad de gavetas
        def actualizar_cantidad_gavetas(event=None):
            try:
                cantidad = int(combo_num_gavetas.get())
                estilo_seleccionado = self.estilo_keys[combo_estilo.current()]
                
                crear_ui_gavetas(cantidad)
                
                # Inicializar con valores predeterminados o distribuidos
                self.loading_values = True
                altura_gabinete = float(entry_alto.get())
                
                if estilo_seleccionado == "Base_3_Gav":
                    espacios_entre_gavetas = (cantidad - 1) * ESPACIO_ENTRE_GAVETAS
                    altura_disponible = altura_gabinete - TOE_KICK - espacios_entre_gavetas
                    altura_por_gaveta = altura_disponible / cantidad
                
                elif estilo_seleccionado == "Base_1_Gav":
                    espacios_entre_gavetas = (cantidad - 1) * ESPACIO_ENTRE_GAVETAS
                    altura_disponible_total = altura_gabinete - TOE_KICK - ESPACIO_SUPERIOR_GAVETA
                    
                    # Por defecto, usar 30% del espacio para gavetas
                    porcentaje_gavetas = gabinete.get("porcentaje_gavetas", 0.3)
                    espacio_gavetas = altura_disponible_total * porcentaje_gavetas
                    altura_por_gaveta = (espacio_gavetas - espacios_entre_gavetas) / cantidad
                
                # Si hay valores guardados, usarlos
                alturas_guardadas = {}
                for i in range(cantidad):
                    key = f"high_drawer_{i}"
                    if key in gabinete:
                        alturas_guardadas[i] = gabinete[key]
                
                # Para compatibilidad con el código antiguo
                if 0 not in alturas_guardadas and "high_drawer_top" in gabinete and cantidad >= 1:
                    alturas_guardadas[0] = gabinete["high_drawer_top"]
                if 1 not in alturas_guardadas and "high_drawer_middle" in gabinete and cantidad >= 2:
                    alturas_guardadas[1] = gabinete["high_drawer_middle"]
                if 2 not in alturas_guardadas and "high_drawer_bottom" in gabinete and cantidad >= 3:
                    alturas_guardadas[2] = gabinete["high_drawer_bottom"]
                
                # Si no hay suficientes valores guardados, distribuir equitativamente
                if len(alturas_guardadas) != cantidad:
                    for i in range(cantidad):
                        gavetas_vars[i].set(round(altura_por_gaveta, 3))
                        gavetas_entries[i].delete(0, tk.END)
                        gavetas_entries[i].insert(0, f"{altura_por_gaveta:.3f}")
                else:
                    for i, altura in alturas_guardadas.items():
                        gavetas_vars[i].set(round(altura, 3))
                        gavetas_entries[i].delete(0, tk.END)
                        gavetas_entries[i].insert(0, f"{altura:.3f}")
                
                self.loading_values = False
                calcular_alturas()
            except ValueError:
                pass
        
        # Vincular el cambio de cantidad de gavetas
        combo_num_gavetas.bind("<<ComboboxSelected>>", actualizar_cantidad_gavetas)

        # Función para mostrar u ocultar los frames según el estilo seleccionado
        def mostrar_ocultar_controles(*args):
            estilo_seleccionado = self.estilo_keys[combo_estilo.current()]
            
            # Ocultar primero todos los frames específicos
            frame_num_gavetas.pack_forget()
            frame_gavetas.pack_forget()
            frame_puertas.pack_forget()
            
            # Mostrar solo los frames relevantes según el estilo
            if estilo_seleccionado == "Base_3_Gav":
                # Para Base_3_Gav: solo mostrar gavetas
                frame_num_gavetas.pack(fill=tk.X, padx=10, pady=5)
                frame_gavetas.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
                actualizar_cantidad_gavetas()
            
            elif estilo_seleccionado == "Base_1_Gav":
                # Para Base_1_Gav: mostrar gavetas y puertas
                frame_num_gavetas.pack(fill=tk.X, padx=10, pady=5)
                frame_gavetas.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
                frame_puertas.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
                actualizar_cantidad_gavetas()
                crear_ui_puertas()
            
        # Vincular el combobox al evento de cambio de estilo
        combo_estilo.bind("<<ComboboxSelected>>", mostrar_ocultar_controles)
        
    # Inicializar la interfaz según el estilo actual
        self.loading_values = True
        mostrar_ocultar_controles()
        self.loading_values = False
        
        # Botones de acción
        frame_botones = ttk.Frame(ventana_estilo)
        frame_botones.pack(fill=tk.X, pady=10, padx=10)
        
        # Botón para guardar cambios
        def guardar_cambios():
            try:
                # Obtener valores de la interfaz
                estilo_nuevo = self.estilo_keys[combo_estilo.current()]
                ancho_nuevo = float(entry_ancho.get())
                alto_nuevo = float(entry_alto.get())
                profundidad_nueva = float(entry_profundidad.get())
                cantidad_nueva = int(entry_cantidad.get())
                
                # Validar valores
                if ancho_nuevo <= 0 or alto_nuevo <= 0 or profundidad_nueva <= 0 or cantidad_nueva <= 0:
                    messagebox.showerror("Error", "Las dimensiones y cantidad deben ser números positivos.")
                    return
                    
                # Actualizar gabinete
                gabinete["Estilo"] = estilo_nuevo
                gabinete["Ancho"] = ancho_nuevo
                gabinete["Alto"] = alto_nuevo
                gabinete["Profundidad"] = profundidad_nueva
                gabinete["Cantidad"] = cantidad_nueva
                
                # Obtener cantidad de gavetas y guardarla
                cantidad_gavetas = int(combo_num_gavetas.get())
                gabinete["num_gavetas"] = cantidad_gavetas
                
                # Guardar altura de cada gaveta
                for i in range(cantidad_gavetas):
                    altura = float(gavetas_entries[i].get())
                    # Usar nueva nomenclatura para almacenar gavetas
                    gabinete[f"high_drawer_{i}"] = altura
                    
                    # Para mantener compatibilidad con código antiguo
                    if i == 0 and cantidad_gavetas >= 1:
                        gabinete["high_drawer_top"] = altura
                    elif i == 1 and cantidad_gavetas >= 2:
                        gabinete["high_drawer_middle"] = altura
                    elif i == 2 and cantidad_gavetas >= 3:
                        gabinete["high_drawer_bottom"] = altura
                
                # Para Base_1_Gav, guardar configuración de puertas
                if estilo_nuevo == "Base_1_Gav":
                    gabinete["dos_puertas"] = var_tiene_dos_puertas.get()
                    gabinete["altura_puerta"] = var_altura_puerta.get()
                    
                    # Calcular espacio usado por gavetas
                    espacios_entre_gavetas = (cantidad_gavetas - 1) * ESPACIO_ENTRE_GAVETAS
                    altura_disponible_total = alto_nuevo - TOE_KICK - ESPACIO_SUPERIOR_GAVETA
                    
                    # Obtener espacio usado por gavetas
                    espacio_gavetas = sum(float(gavetas_entries[i].get()) for i in range(cantidad_gavetas)) + espacios_entre_gavetas
                    
                    # Guardar porcentaje usado por gavetas para futura referencia
                    if altura_disponible_total > 0:
                        gabinete["porcentaje_gavetas"] = espacio_gavetas / altura_disponible_total
                
                # Recalcular piezas y actualizar la vista
                gabinete["piezas"] = self.gestor_gabinetes.calcular_piezas(gabinete)
                self.mostrar_piezas(None)
                self.autoguardar_datos()
                
                # Cerrar ventana
                ventana_estilo.destroy()
                messagebox.showinfo("Éxito", "Gabinete actualizado correctamente.")
                
            except ValueError as e:
                messagebox.showerror("Error", f"Por favor ingrese valores numéricos válidos: {str(e)}")
        
        ttk.Button(frame_botones, text="Guardar Cambios", command=guardar_cambios).pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=ventana_estilo.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Vincular eventos de entrada para cálculos automáticos
        entry_alto.bind("<KeyRelease>", calcular_alturas)
        entry_ancho.bind("<KeyRelease>", calcular_alturas)
        entry_profundidad.bind("<KeyRelease>", calcular_alturas)
        
        # Centrar la ventana
        ventana_estilo.update_idletasks()
        ancho_ventana = ventana_estilo.winfo_width()
        alto_ventana = ventana_estilo.winfo_height()
        x = (ventana_estilo.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (ventana_estilo.winfo_screenheight() // 2) - (alto_ventana // 2)
        ventana_estilo.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        # Hacer que la ventana sea modal
        ventana_estilo.transient(self.root)
        ventana_estilo.grab_set()
        
        # Iniciar con cálculos
        calcular_alturas()

    def cambiar_vista(self, vista):
        self.vista_actual = vista
        if self.gabinete_actual and self.piezas_actual:
            dibujar_gabinete(
                canvas=self.canvas,
                vista=vista,
                gabinete=self.gabinete_actual,
                piezas=self.piezas_actual
        )
    
    def agregar_gabinete(self):
        ancho = self.ancho_var.get()
        alto = self.alto_var.get()
        profundidad = self.profundidad_var.get()
        espesor = self.espesor_var.get()
        cantidad = self.cantidad_var.get()

        if not (ancho > 0 and alto > 0 and profundidad > 0 and espesor > 0 and cantidad > 0):
            messagebox.showerror("Error", "Todas las dimensiones y la cantidad deben ser mayores a 0")
            return

        selected_index = self.combo_estilo.current()
        selected_key = self.estilo_keys[selected_index]
        selected_value = self.estilo_values[selected_index]

        gabinete_id = len(self.gabinetes) + 1
        self.gabinetes.append({
            "ID": gabinete_id,
            "Ancho": ancho,
            "Alto": alto,
            "Profundidad": profundidad,
            "Espesor": espesor,
            "Estilo": selected_key,
            "Cantidad": cantidad
        })

        self.tree_gabinetes.insert("", "end", values=(gabinete_id, ancho, alto, profundidad, selected_value, cantidad))
        self.autoguardar_datos()
    
    def mostrar_piezas(self, event):
        selected_item = self.tree_gabinetes.selection()
        if not selected_item:
            return
        
        item = self.tree_gabinetes.item(selected_item)
        gabinete_id = item["values"][0]
        gabinete = next(g for g in self.gabinetes if g["ID"] == gabinete_id)
        
        # Configurar el estilo según el gabinete seleccionado
        if "Estilo" in gabinete:
            self.gestor_gabinetes.cambiar_estilo(gabinete["Estilo"])
            
            # Actualizar el combobox para mostrar el estilo actual
            index = self.estilo_keys.index(gabinete["Estilo"])
            self.combo_estilo.current(index)
        
        # Calcular piezas usando el gestor de estilos
        piezas = self.gestor_gabinetes.calcular_piezas(gabinete)
        self.piezas_actual = piezas
        self.gabinete_actual = gabinete
        
        # Limpiar el canvas antes de dibujar la nueva pieza
        self.canvas.delete("all")
        
        # Actualizar la tabla de piezas
        self.tree_piezas.delete(*self.tree_piezas.get_children())
        for pieza in piezas:
            # Maneja el caso especial de box Drawer que tiene profundidad
            if "profundidad" in pieza:
                self.tree_piezas.insert("", "end", values=(pieza["nombre"], pieza["ancho"], pieza["alto"], pieza["profundidad"]))
            else:
                self.tree_piezas.insert("", "end", values=(pieza["nombre"], pieza["ancho"], pieza["alto"], ""))
        
        # Asociar un evento para seleccionar una pieza
        dibujar_gabinete(self.canvas, self.vista_actual, gabinete, piezas)
        self.tree_piezas.bind("<ButtonRelease-1>", self.dibujar_pieza_seleccionada)

    def dibujar_pieza_seleccionada(self, event):
        # Obtener la pieza seleccionada en la tabla
        selected_item = self.tree_piezas.selection()
        if not selected_item:
            return
        
        item = self.tree_piezas.item(selected_item)
        nombre_pieza = item["values"][0]
        ancho = float(item["values"][1])
        alto = float(item["values"][2])
        
        # Buscar la pieza completa con todos sus datos
        pieza_completa = None
        for p in self.piezas_actual:
            if p["nombre"] == nombre_pieza:
                pieza_completa = p
                break
        
        if not pieza_completa:
            return
        
        # Limpiar el canvas antes de dibujar la nueva pieza
        self.canvas.delete("all")
        
        # Factor de escala para la visualización
        escala = 10
        margen_x = (Canvas_width - ancho) / 3
        margen_y = 50
        
        # Dibujar la pieza seleccionada
        self.canvas.create_rectangle(
            margen_x, margen_y, 
            margen_x + ancho * escala, 
            margen_y + alto * escala, 
            outline="black", fill="lightblue"
        )
        
        # Añadir etiqueta con nombre y dimensiones
        self.canvas.create_text(
            margen_x + ancho * escala / 2, 
            margen_y + -15, 
            text=f"{nombre_pieza}: {ancho}\" x {alto}\"", 
            fill="black",
            font=("Arial", 12, "bold")
        )
        
        # Verificar si la pieza tiene orificios para shelf y dibujarlos
        if "orificios_shelf" in pieza_completa:
            orificios = pieza_completa["orificios_shelf"]
            
            # Extraer información de orificios
            cantidad_orificios = orificios["cantidad"]
            separacion = orificios.get("separacion", 1.26)
            diametro = orificios["diametro"]
            filas = orificios["filas"]
            distancia_trasera = orificios["distancia_trasera"]
            distancia_frontal = orificios["distancia_frontal"]
            distancia_inferior = orificios["distancia_inferior"]
            distancia_superior = distancia_inferior + 1.75
            
            # Determinar cuántos orificios caben con la separación fija
            espacio_disponible = alto - distancia_inferior - distancia_superior
            max_orificios = int(espacio_disponible / separacion) + 1
            
            # Limitar a un número razonable si es necesario
            cantidad = min(max_orificios, cantidad_orificios)
            
            # Dibujar las filas de orificios
            if filas >= 1:
                # Primera fila (desde el borde izquierdo/frontal)
                distancia_vertical_1 = alto - distancia_inferior - (cantidad * separacion)
                
                for i in range(cantidad):
                    y_pos = margen_y + (distancia_vertical_1 + i * separacion) * escala
                    x_pos = margen_x + distancia_frontal * escala
                    
                    # Dibujar círculo para el orificio
                    radio = diametro * escala / 2
                    self.canvas.create_oval(
                        x_pos - radio, y_pos - radio,
                        x_pos + radio, y_pos + radio,
                        fill="black"
                    )
            
            if filas >= 2:
                # Segunda fila (desde el borde derecho/trasero)
                distancia_vertical_2 = alto - distancia_inferior - (cantidad * separacion)
                distancia_horizontal_2 = ancho - distancia_trasera
                
                for i in range(cantidad):
                    y_pos = margen_y + (distancia_vertical_2 + i * separacion) * escala
                    x_pos = margen_x + distancia_horizontal_2 * escala
                    
                    # Dibujar círculo para el orificio
                    radio = diametro * escala / 2
                    self.canvas.create_oval(
                        x_pos - radio, y_pos - radio,
                        x_pos + radio, y_pos + radio,
                        fill="black"
                    )
            
            # Añadir leyenda para los orificios
            self.canvas.create_text(
                margen_x + ancho * escala / 2, 
                margen_y + alto * escala + 20, 
                text=f"Orificios: {cantidad} en cada fila, separación {separacion}\", Ø {diametro}\"", 
                fill="black",
                font=("Arial", 10)
            )

    def cargar_datos_temporales(self):
        """Carga los datos del archivo temporal si existe"""
        if os.path.exists(self.archivo_temp):
            try:
                with open(self.archivo_temp, "r") as archivo:
                    datos = json.load(archivo)
                    
                    # Limpia los datos actuales
                    self.gabinetes = []
                    self.tree_gabinetes.delete(*self.tree_gabinetes.get_children())

                    # Procesa los datos cargados
                    for item in datos:
                        gabinete = item["gabinete"]
                        self.gabinetes.append(gabinete)
                        self.tree_gabinetes.insert("", "end", values=(
                            gabinete["ID"], 
                            gabinete["Ancho"], 
                            gabinete["Alto"], 
                            gabinete["Profundidad"],
                            gabinete["Estilo"],
                            gabinete.get("Cantidad", 1)
                        ))
                    
                    # Restaurar los gabinetes desde los datos cargados
                    self.gabinetes = [item["gabinete"] for item in datos]
                    print(f"Se cargaron {len(self.gabinetes)} gabinetes desde archivo temporal")
            except Exception as e:
                print(f"Error al cargar datos temporales: {str(e)}")
        
    def autoguardar_datos(self):
        """Guarda automáticamente los datos en el archivo temporal"""
        datos = []

        for gabinete in self.gabinetes:
            try:
                # Usa el gestor de gabinetes para calcular las piezas según el estilo del gabinete
                piezas = self.gestor_gabinetes.calcular_piezas(gabinete)

                # Agrega el gabinete y sus piezas a la lista de datos
                datos.append({
                    "gabinete": gabinete,
                    "piezas": piezas,
                })
            except Exception as e:
                print(f"Error al procesar gabinete para autoguardado: {str(e)}")
                # Continúa con el siguiente gabinete
                continue

        try:
            with open(self.archivo_temp, "w") as archivo:
                json.dump(datos, archivo, indent=4)
            print(f"Autoguardado: {len(self.gabinetes)} gabinetes guardados en {self.archivo_temp}")
            return True
        except Exception as e:
            print(f"Error al autoguardar: {str(e)}")
            return False
    
    def guardar_datos(self):
        """Guarda los datos en un archivo seleccionado por el usuario"""
        # Crea una lista para almacenar los gabinetes y sus piezas
        datos = []

        for gabinete in self.gabinetes:
            try:
                # Usa el gestor de gabinetes para calcular las piezas según el estilo actual
                piezas = self.gestor_gabinetes.calcular_piezas(gabinete)

                # Agrega el gabinete y sus piezas a la lista de datos
                datos.append({
                    "gabinete": gabinete,
                    "piezas": piezas,
                })
            except Exception as e:
                print(f"Error al procesar gabinete para guardado: {str(e)}")
                # Continúa con el siguiente gabinete
                continue

        # Abre el diálogo para seleccionar el directorio y nombre del archivo
        archivo_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json")],
            title="Guardar archivo"
        )

        # Si el usuario no cancela la selección
        if archivo_path:
            try:
                with open(archivo_path, "w") as archivo:
                    json.dump(datos, archivo, indent=4)

                messagebox.showinfo("Guardado", f"Se han guardado {len(self.gabinetes)} gabinetes en {archivo_path}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
                return False
        else:
            messagebox.showwarning("Cancelado", "No se guardaron los datos.")
            return False
            
    def eliminar_gabinete(self):
        """Elimina el gabinete seleccionado de la lista"""
        seleccion = self.tree_gabinetes.selection()
        if not seleccion:
            messagebox.showinfo("Información", "No hay gabinete seleccionado para eliminar.")
            return
        
        # Confirmación antes de eliminar
        if not messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este gabinete?"):
            return
        
        # Obtener el ID del gabinete seleccionado
        item_id = seleccion[0]
        valores = self.tree_gabinetes.item(item_id)["values"]
        id_gabinete = valores[0]
        
        # Buscar y eliminar el gabinete de la lista
        for i, gabinete in enumerate(self.gabinetes):
            if gabinete["ID"] == id_gabinete:
                del self.gabinetes[i]
                break
        
        # Eliminar el elemento del treeview
        self.tree_gabinetes.delete(item_id)
        
        # Limpiar la vista de piezas
        self.tree_piezas.delete(*self.tree_piezas.get_children())
        
        # Autoguardar los cambios
        self.autoguardar_datos()
        
        messagebox.showinfo("Éxito", "Gabinete eliminado correctamente.")
        
        # Si quedan gabinetes, seleccionar el primero
        if self.gabinetes:
            first_item = self.tree_gabinetes.get_children()[0]
            self.tree_gabinetes.selection_set(first_item)
            self.mostrar_piezas(None)

    def cargar_datos(self):
        # Abre el cuadro de diálogo para seleccionar el archivo JSON
        archivo_path = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json")],
            title="Seleccionar archivo de datos"
        )

        # Verifica si el usuario canceló la selección
        if not archivo_path:
            messagebox.showinfo("Cancelado", "No se seleccionó ningún archivo.")
            return

        try:
            # Carga los datos desde el archivo JSON seleccionado
            with open(archivo_path, "r") as archivo:
                datos = json.load(archivo)

            # Limpia los datos actuales
            self.gabinetes = []
            self.tree_gabinetes.delete(*self.tree_gabinetes.get_children())

            # Procesa los datos cargados
            for item in datos:
                gabinete = item["gabinete"]
                self.gabinetes.append(gabinete)
                self.tree_gabinetes.insert("", "end", values=(
                    gabinete["ID"], 
                    gabinete["Ancho"], 
                    gabinete["Alto"], 
                    gabinete["Profundidad"],
                    gabinete["Estilo"],
                    gabinete.get("Cantidad", 1)
                ))

            messagebox.showinfo("Cargado", f"Se han cargado {len(self.gabinetes)} gabinetes desde {archivo_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")

    def mostrar_menu_contextual(self, event):
        """Muestra un menú contextual al hacer clic derecho en un gabinete"""
        seleccion = self.tree_gabinetes.selection()
        if seleccion:
            # Crear el menú contextual
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Editar gabinete", command=self.cambiar_estilo_gabinete_seleccionado)
            menu.add_command(label="Eliminar gabinete", command=self.eliminar_gabinete)
            
            # Mostrar el menú en la ubicación del clic
            menu.post(event.x_root, event.y_root)

    def limpiar_tabla(self):
        """Limpia completamente la tabla de gabinetes y el archivo temporal"""
        # Pedir confirmación antes de eliminar todos los datos
        if not messagebox.askyesno("Confirmar eliminación", 
                                "¿Está seguro de que desea eliminar TODOS los gabinetes?\n\nEsta acción no se puede deshacer."):
            return
        
        # Limpiar la lista de gabinetes
        self.gabinetes = []
        
        # Limpiar los treeviews
        self.tree_gabinetes.delete(*self.tree_gabinetes.get_children())
        self.tree_piezas.delete(*self.tree_piezas.get_children())
        
        # Guardar el archivo temporal vacío
        try:
            with open(self.archivo_temp, "w") as archivo:
                json.dump([], archivo)
            print("Se ha limpiado la tabla y el archivo temporal")
        except Exception as e:
            print(f"Error al limpiar archivo temporal: {str(e)}")
        
        messagebox.showinfo("Éxito", "Se han eliminado todos los gabinetes correctamente.")
        
        # Opcionalmente, reiniciar el contador de IDs si lo estás usando
        if hasattr(self, 'contador_id'):
            self.contador_id = 1
    
if __name__ == "__main__":
    root = tk.Tk()
    app = GabineteApp(root)
    root.mainloop()