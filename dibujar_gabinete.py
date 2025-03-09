from tkinter import Canvas

def dibujar_gabinete(canvas: Canvas, vista: str, gabinete: dict, piezas: list):
    """
    Dibuja la vista seleccionada del gabinete en el canvas.

    :param canvas: Canvas de Tkinter donde se dibuja.
    :param vista: Vista a dibujar ("frontal", "lateral", etc.).
    :param gabinete: Diccionario con las dimensiones del gabinete.
    :param piezas: Lista de piezas del gabinete.
    """
    canvas.delete("all")  # Limpiar el canvas antes de dibujar
    
    # Configurar márgenes y escala
    margen = 50
    escala = min(
        (canvas.winfo_width() - 2 * margen) / (gabinete["Ancho"] if vista == "frontal" else gabinete["Profundidad"]),
        (canvas.winfo_height() - 2 * margen) / gabinete["Alto"]
    )

    def escalar(medida):
        return medida * escala

    x_inicio = margen
    y_inicio = margen
    
    if vista == "frontal":
        x_inicio = (canvas.winfo_width() - escalar(gabinete["Ancho"])) / 2
        y_inicio = (canvas.winfo_height() - escalar(gabinete["Alto"])) / 2
        dibujar_vista_frontal(canvas, gabinete, piezas, escalar, x_inicio, y_inicio)
    elif vista == "lateral":
        x_inicio = (canvas.winfo_width() - escalar(gabinete["Profundidad"])) / 2
        y_inicio = (canvas.winfo_height() - escalar(gabinete["Alto"])) / 2
        dibujar_vista_lateral(canvas, gabinete, piezas, escalar, x_inicio, y_inicio)
    else:
        raise ValueError(f"Vista desconocida: {vista}")

def dibujar_vista_frontal(canvas, gabinete, piezas, escalar, x_inicio, y_inicio):
    """
    Dibuja la vista frontal del gabinete en el canvas según el estilo.
    """
    estilo = gabinete.get("Estilo", "Base_1_Gav")  # Estilo por defecto si no se especifica
    
    if estilo == "Base_1_Gav":
        dibujar_vista_frontal_una_gaveta_dos_puertas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio)
    elif estilo == "Base_3_Gav":
        dibujar_vista_frontal_tres_gavetas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio)
    elif estilo == "Wall_cabinet":
        dibujar_vista_frontal_dos_puertas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio)
    else:
        raise ValueError(f"Estilo desconocido para vista frontal: {estilo}")

def dibujar_vista_lateral(canvas, gabinete, piezas, escalar, x_inicio, y_inicio):
    """
    Dibuja la vista lateral del gabinete en el canvas según el estilo.
    """
    estilo = gabinete.get("Estilo", "Base_1_Gav")  # Estilo por defecto si no se especifica
    
    if estilo == "Base_1_Gav":
        dibujar_vista_lateral_una_gaveta_dos_puertas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio)
    elif estilo == "Base_3_Gav":
        dibujar_vista_lateral_tres_gavetas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio)
    elif estilo == "Wall_cabinet":
        dibujar_vista_lateral_dos_puertas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio)
    else:
        raise ValueError(f"Estilo desconocido para vista lateral: {estilo}")

def dibujar_vista_frontal_una_gaveta_dos_puertas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio):
    espesor = gabinete["Espesor"]
    toe_kick_altura = 4
    espacio_superior = 0.25
    high_drawer = 5.875
    gap = 0.125

    # Dibujar marco exterior
    canvas.create_rectangle(
        x_inicio, y_inicio,
        x_inicio + escalar(gabinete["Ancho"]),
        y_inicio + escalar(gabinete["Alto"]),
        outline='black', width=1
    )

    # Dibujar los costados
    canvas.create_line(x_inicio + escalar(espesor), y_inicio,
                       x_inicio + escalar(espesor), y_inicio + escalar(gabinete["Alto"]),
                       fill='gray', width=1)
    canvas.create_line(x_inicio + escalar(gabinete["Ancho"] - espesor), y_inicio,
                       x_inicio + escalar(gabinete["Ancho"] - espesor), y_inicio + escalar(gabinete["Alto"]),
                       fill='gray', width=1)

    # Dibujar el toe kick
    canvas.create_rectangle(
        x_inicio, y_inicio + escalar(gabinete["Alto"] - toe_kick_altura),
        x_inicio + escalar(gabinete["Ancho"]),
        y_inicio + escalar(gabinete["Alto"]),
        fill='darkgray'
    )

    # Dibujar cajón superior
    drawer_y = y_inicio + escalar(espacio_superior)
    canvas.create_rectangle(
        x_inicio + escalar(gap/2), drawer_y,
        x_inicio + escalar(gabinete["Ancho"] - gap/2),
        drawer_y + escalar(high_drawer),
        fill='lightblue', outline='black', width=1
    )

    # Dibujar puertas
    altura_puerta = gabinete["Alto"] - high_drawer - espacio_superior - toe_kick_altura - gap - espacio_superior
    if gabinete["Ancho"] > 18:
        ancho_puerta = (gabinete["Ancho"] / 2) - gap
        canvas.create_rectangle(
            x_inicio + escalar(gap/2), drawer_y + escalar(high_drawer + espacio_superior),
            x_inicio + escalar(ancho_puerta), y_inicio + escalar(gabinete["Alto"] - toe_kick_altura - gap),
            fill='lightyellow', outline='black', width=1
        )
        canvas.create_rectangle(
            x_inicio + escalar(gabinete["Ancho"]/2 + gap/2), drawer_y + escalar(high_drawer + espacio_superior),
            x_inicio + escalar(gabinete["Ancho"] - gap/2), y_inicio + escalar(gabinete["Alto"] - toe_kick_altura - gap),
            fill='lightyellow', outline='black', width=1
        )
        canvas.create_line(
            x_inicio + escalar(gabinete["Ancho"]/2), drawer_y + escalar(high_drawer + espacio_superior),
            x_inicio + escalar(gabinete["Ancho"]/2), y_inicio + escalar(gabinete["Alto"] - toe_kick_altura - gap),
            fill='black', width=1
        )
    else:
        canvas.create_rectangle(
            x_inicio + escalar(gap/2), drawer_y + escalar(high_drawer + espacio_superior),
            x_inicio + escalar(gabinete["Ancho"] - gap/2), y_inicio + escalar(gabinete["Alto"] - toe_kick_altura - gap),
            fill='lightyellow', outline='black', width=1
        )
        
    # Añadir dimensiones
    canvas.create_text(
        x_inicio + escalar(gabinete["Ancho"]/2),
        y_inicio - 20,
        text=f"Ancho: {gabinete['Ancho']}\"",
        anchor="center"
    )
    canvas.create_text(
        x_inicio - 20,
        y_inicio + escalar(gabinete["Alto"]/2),
        text=f"Alto: {gabinete['Alto']}\"",
        anchor="center",
        angle=90
    )

def dibujar_vista_lateral_una_gaveta_dos_puertas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio):
    """
    Dibuja la vista lateral del gabinete con una gaveta y dos puertas.
    """
    espesor = gabinete["Espesor"]
    gap = 0.125
    toe_kick_altura = 4
    espacio_superior = 0.25
    high_drawer = 4
    drawer_front_thickness = 0.75
    prof_toekick = 3
    door_thickness = 0.75
    drawer_front_high = 5.875
    
    # Dibujar el marco exterior del gabinete (vista lateral)
    canvas.create_rectangle(
        x_inicio,
        y_inicio,
        x_inicio + escalar(gabinete["Profundidad"]),
        y_inicio + escalar(gabinete["Alto"]),
        outline='black',
        width=1
    )
    
    # Dibujar base
    canvas.create_rectangle(
        x_inicio,
        y_inicio + escalar(gabinete["Alto"] - espesor - toe_kick_altura),
        x_inicio + escalar(gabinete["Profundidad"]),
        y_inicio + escalar(gabinete["Alto"] - toe_kick_altura),
        fill='lightgray',
        outline='black'
    )
    
    # Dibujar toe kick
    canvas.create_rectangle(
        x_inicio + escalar(prof_toekick),
        y_inicio + escalar(gabinete["Alto"] - toe_kick_altura),
        x_inicio + escalar(prof_toekick + espesor),
        y_inicio + escalar(gabinete["Alto"]),
        fill='lightgray'
    )
    
    # Profundidad del cajón
    profundidad_box_drawer = 16
    if gabinete["Profundidad"] > 26:
        profundidad_box_drawer = 24
    elif gabinete["Profundidad"] > 23:
        profundidad_box_drawer = 21
    elif gabinete["Profundidad"] > 21:
        profundidad_box_drawer = 18
        
    # Dimensiones para los rails
    rail_thickness = 0.75
    rail_width = 3
    up_rail_gap = 0.5
    down_rail_gap = 0.625
    
    # Drawer face
    canvas.create_rectangle(
        x_inicio - escalar(drawer_front_thickness),
        y_inicio + escalar(espacio_superior),
        x_inicio,
        y_inicio + escalar(espacio_superior + drawer_front_high),
        fill='orange',
        outline='black',
        width=1
    )
    
    # Puertas
    canvas.create_rectangle(
        x_inicio - escalar(door_thickness),
        y_inicio + escalar(espacio_superior + drawer_front_high + gap),
        x_inicio,
        y_inicio + escalar(gabinete["Alto"] - toe_kick_altura),
        fill='orange',
        outline='black',
        width=1
    )
    
    # Box drawer
    canvas.create_rectangle(
        x_inicio,
        y_inicio + escalar(rail_thickness + up_rail_gap),
        x_inicio + escalar(profundidad_box_drawer),
        y_inicio + escalar(rail_thickness + up_rail_gap + high_drawer),
        fill='powderblue',
        outline='black'
    )
    
    # Rail frontal superior
    canvas.create_rectangle(
        x_inicio,
        y_inicio,
        x_inicio + escalar(rail_width),
        y_inicio + escalar(rail_thickness),
        fill='lightgray',
        outline='black'
    )
    
    # Rail frontal inferior
    canvas.create_rectangle(
        x_inicio,
        y_inicio + escalar(rail_thickness + up_rail_gap + high_drawer + down_rail_gap),
        x_inicio + escalar(rail_width),
        y_inicio + escalar(rail_thickness + up_rail_gap + high_drawer + down_rail_gap + rail_thickness),
        fill='lightgray',
        outline='black'
    )
    
    # Rail trasero
    canvas.create_rectangle(
        x_inicio + escalar(gabinete["Profundidad"] - rail_width),
        y_inicio,
        x_inicio + escalar(gabinete["Profundidad"]),
        y_inicio + escalar(rail_thickness),
        fill='lightgray',
        outline='black'
    )
    
    # Dibujar entrepano
    canvas.create_rectangle(
        x_inicio + escalar(espesor),
        y_inicio + escalar(gabinete["Alto"]/2),
        x_inicio + escalar(gabinete["Profundidad"] - espesor),
        y_inicio + escalar(gabinete["Alto"]/2 + espesor),
        fill='lightgray',
        outline='black'
    )
    
    # Agregar dimensiones
    canvas.create_text(
        x_inicio + escalar(gabinete["Profundidad"]/2),
        y_inicio - 20,
        text=f"Profundidad: {gabinete['Profundidad']}\"",
        anchor="center"
    )
    canvas.create_text(
        x_inicio - 20,
        y_inicio + escalar(gabinete["Alto"]/2),
        text=f"Alto: {gabinete['Alto']}\"",
        anchor="center",
        angle=90
    )
    
    # Agregar leyenda
    legend_x = x_inicio + escalar(gabinete["Profundidad"]) + 50
    legend_y = y_inicio
    legend_items = [
        ("Base/Shelf/Backer", "lightgray"),
        ("Toe Kick/Rieles", "lightgray"),
        ("Drawer Face/Door", "orange"),
        ("Box Drawer", "powderblue"),
    ]
    
    for i, (texto, color) in enumerate(legend_items):
        canvas.create_rectangle(
            legend_x,
            legend_y + i*20,
            legend_x + 20,
            legend_y + i*20 + 15,
            fill=color
        )
        canvas.create_text(
            legend_x + 30,
            legend_y + i*20 + 7,
            text=texto,
            anchor="w"
        )

def dibujar_vista_frontal_tres_gavetas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio):
    """
    Dibuja la vista frontal del gabinete con tres gavetas utilizando las dimensiones de las piezas.
    """
    espesor = gabinete["Espesor"]
    toe_kick_altura = 4  # Altura predeterminada para el toe kick
    gap = 0.125  # Gap predeterminado

    # Buscar las piezas relevantes en la lista de piezas
    drawer_face_superior = next((p for p in piezas if p["nombre"] == "Drawer Face Superior"), None)
    drawer_face_media = next((p for p in piezas if p["nombre"] == "Drawer Face Media"), None)
    drawer_face_inferior = next((p for p in piezas if p["nombre"] == "Drawer Face Inferior"), None)
    toe_kick_pieza = next((p for p in piezas if p["nombre"] == "Toe Kick"), None)

    # Obtener dimensiones de las piezas si están disponibles
    if toe_kick_pieza:
        toe_kick_altura = toe_kick_pieza["alto"]

    # Verificar que encontramos todas las piezas necesarias
    if not all([drawer_face_superior, drawer_face_media, drawer_face_inferior]):
        # Si faltan piezas, usar valores predeterminados como fallback
        print("Advertencia: No se encontraron todas las piezas necesarias para dibujar las gavetas")
        # Calcular altura de cada gaveta (como en el código original)
        altura_disponible = gabinete["Alto"] - toe_kick_altura - (2 * 0.25)  # 0.25 es espacio_entre_gavetas
        high_drawer_top = 5.875  # Gaveta superior más alta
        high_drawer_middle = (altura_disponible - high_drawer_top) / 2
        high_drawer_bottom = high_drawer_middle
    else:
        # Usar las dimensiones de las piezas
        high_drawer_top = drawer_face_superior["alto"]
        high_drawer_middle = drawer_face_media["alto"]
        high_drawer_bottom = drawer_face_inferior["alto"]
        # Usamos el ancho de la primera gaveta para determinar el gap (diferencia entre ancho del gabinete y ancho de gaveta)
        if drawer_face_superior["ancho"] < gabinete["Ancho"]:
            gap = gabinete["Ancho"] - drawer_face_superior["ancho"]

    # Dibujar marco exterior
    canvas.create_rectangle(
        x_inicio, y_inicio,
        x_inicio + escalar(gabinete["Ancho"]),
        y_inicio + escalar(gabinete["Alto"]),
        outline='black', width=1
    )

    # Dibujar los costados
    canvas.create_line(x_inicio + escalar(espesor), y_inicio,
                       x_inicio + escalar(espesor), y_inicio + escalar(gabinete["Alto"]),
                       fill='gray', width=1)
    canvas.create_line(x_inicio + escalar(gabinete["Ancho"] - espesor), y_inicio,
                       x_inicio + escalar(gabinete["Ancho"] - espesor), y_inicio + escalar(gabinete["Alto"]),
                       fill='gray', width=1)

    # Dibujar el toe kick
    canvas.create_rectangle(
        x_inicio, y_inicio + escalar(gabinete["Alto"] - toe_kick_altura),
        x_inicio + escalar(gabinete["Ancho"]),
        y_inicio + escalar(gabinete["Alto"]),
        fill='darkgray'
    )

    # Calcular posiciones de las gavetas
    # Espacio entre gavetas
    espacio_entre_gavetas = 0.25
    
    # Calcular posición y para cada gaveta
    # La gaveta superior comienza después del espacio_entre_gavetas desde arriba
    drawer_y_top = y_inicio + escalar(espacio_entre_gavetas)
    
    # Dibujar gaveta superior
    canvas.create_rectangle(
        x_inicio + escalar(gap/2), drawer_y_top,
        x_inicio + escalar(gabinete["Ancho"] - gap/2),
        drawer_y_top + escalar(high_drawer_top),
        fill='lightblue', outline='black', width=1
    )

    # Dibujar gaveta media
    drawer_y_middle = drawer_y_top + escalar(high_drawer_top + espacio_entre_gavetas)
    canvas.create_rectangle(
        x_inicio + escalar(gap/2), drawer_y_middle,
        x_inicio + escalar(gabinete["Ancho"] - gap/2),
        drawer_y_middle + escalar(high_drawer_middle),
        fill='lightblue', outline='black', width=1
    )

    # Dibujar gaveta inferior
    drawer_y_bottom = drawer_y_middle + escalar(high_drawer_middle + espacio_entre_gavetas)
    canvas.create_rectangle(
        x_inicio + escalar(gap/2), drawer_y_bottom,
        x_inicio + escalar(gabinete["Ancho"] - gap/2),
        drawer_y_bottom + escalar(high_drawer_bottom),
        fill='lightblue', outline='black', width=1
    )
    
    # Añadir dimensiones
    canvas.create_text(
        x_inicio + escalar(gabinete["Ancho"]/2),
        y_inicio - 20,
        text=f"Ancho: {gabinete['Ancho']}\"",
        anchor="center"
    )
    canvas.create_text(
        x_inicio - 20,
        y_inicio + escalar(gabinete["Alto"]/2),
        text=f"Alto: {gabinete['Alto']}\"",
        anchor="center",
        angle=90
    )

def dibujar_vista_lateral_tres_gavetas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio):
    """
    Dibuja la vista lateral del gabinete con tres gavetas.
    """
    espesor = gabinete["Espesor"]
    toe_kick_altura = 4
    espacio_entre_gavetas = 0.25
    gap = 0.125
    drawer_front_thickness = 0.75
    prof_toekick = 3
    
    # Calcular altura de cada gaveta
    altura_disponible = gabinete["Alto"] - toe_kick_altura - (2 * espacio_entre_gavetas)
    high_drawer_top = 5.875  # Gaveta superior más alta
    high_drawer_middle = (altura_disponible - high_drawer_top) / 2
    high_drawer_bottom = high_drawer_middle
    
    # Dibujar el marco exterior
    canvas.create_rectangle(
        x_inicio, y_inicio,
        x_inicio + escalar(gabinete["Profundidad"]),
        y_inicio + escalar(gabinete["Alto"]),
        outline='black', width=1
    )
    
    # Dibujar base
    canvas.create_rectangle(
        x_inicio,
        y_inicio + escalar(gabinete["Alto"] - espesor - toe_kick_altura),
        x_inicio + escalar(gabinete["Profundidad"]),
        y_inicio + escalar(gabinete["Alto"] - toe_kick_altura),
        fill='lightgray',
        outline='black'
    )
    
    # Dibujar toe kick
    canvas.create_rectangle(
        x_inicio + escalar(prof_toekick),
        y_inicio + escalar(gabinete["Alto"] - toe_kick_altura),
        x_inicio + escalar(prof_toekick + espesor),
        y_inicio + escalar(gabinete["Alto"]),
        fill='lightgray'
    )
    
    # Profundidad del cajón
    profundidad_box_drawer = 16
    if gabinete["Profundidad"] > 26:
        profundidad_box_drawer = 24
    elif gabinete["Profundidad"] > 23:
        profundidad_box_drawer = 21
    elif gabinete["Profundidad"] > 21:
        profundidad_box_drawer = 18
    
    # Dimensiones para los rails
    rail_thickness = 0.75
    rail_width = 3
    up_rail_gap = 0.5
    
    # Drawer face superior
    drawer_y_top = y_inicio + espacio_entre_gavetas
    canvas.create_rectangle(
        x_inicio - escalar(drawer_front_thickness),
        drawer_y_top,
        x_inicio,
        drawer_y_top + escalar(high_drawer_top),
        fill='orange',
        outline='black',
        width=1
    )
    
    # Box drawer superior
    canvas.create_rectangle(
        x_inicio,
        drawer_y_top + escalar(up_rail_gap),
        x_inicio + escalar(profundidad_box_drawer),
        drawer_y_top + escalar(up_rail_gap + high_drawer_top - rail_thickness),
        fill='powderblue',
        outline='black'
    )
    
    # Drawer face medio
    drawer_y_middle = drawer_y_top + escalar(high_drawer_top + espacio_entre_gavetas)
    canvas.create_rectangle(
        x_inicio - escalar(drawer_front_thickness),
        drawer_y_middle,
        x_inicio,
        drawer_y_middle + escalar(high_drawer_middle),
        fill='orange',
        outline='black',
        width=1
    )
    
    # Box drawer medio
    canvas.create_rectangle(
        x_inicio,
        drawer_y_middle + escalar(up_rail_gap),
        x_inicio + escalar(profundidad_box_drawer),
        drawer_y_middle + escalar(up_rail_gap + high_drawer_middle - rail_thickness),
        fill='powderblue',
        outline='black'
    )
    
    # Drawer face inferior
    drawer_y_bottom = drawer_y_middle + escalar(high_drawer_middle + espacio_entre_gavetas)
    canvas.create_rectangle(
        x_inicio - escalar(drawer_front_thickness),
        drawer_y_bottom,
        x_inicio,
        drawer_y_bottom + escalar(high_drawer_bottom),
        fill='orange',
        outline='black',
        width=1
    )
    
    # Box drawer inferior
    canvas.create_rectangle(
        x_inicio,
        drawer_y_bottom + escalar(up_rail_gap),
        x_inicio + escalar(profundidad_box_drawer),
        drawer_y_bottom + escalar(up_rail_gap + high_drawer_bottom - rail_thickness),
        fill='powderblue',
        outline='black'
    )
    
    # Rails para los cajones
    for i, drawer_y in enumerate([drawer_y_top, drawer_y_middle, drawer_y_bottom]):
        # Rail superior
        canvas.create_rectangle(
            x_inicio,
            drawer_y,
            x_inicio + escalar(rail_width),
            drawer_y + escalar(rail_thickness),
            fill='lightgray',
            outline='black'
        )
        
        # Rail inferior
        canvas.create_rectangle(
            x_inicio,
            drawer_y + escalar(high_drawer_top if i == 0 else high_drawer_middle) - escalar(rail_thickness),
            x_inicio + escalar(rail_width),
            drawer_y + escalar(high_drawer_top if i == 0 else high_drawer_middle),
            fill='lightgray',
            outline='black'
        )
    
    # Agregar dimensiones
    canvas.create_text(
        x_inicio + escalar(gabinete["Profundidad"]/2),
        y_inicio - 20,
        text=f"Profundidad: {gabinete['Profundidad']}\"",
        anchor="center"
    )
    canvas.create_text(
        x_inicio - 20,
        y_inicio + escalar(gabinete["Alto"]/2),
        text=f"Alto: {gabinete['Alto']}\"",
        anchor="center",
        angle=90
    )
    
    # Agregar leyenda
    legend_x = x_inicio + escalar(gabinete["Profundidad"]) + 50
    legend_y = y_inicio
    legend_items = [
        ("Base/Shelf", "lightgray"),
        ("Toe Kick/Rieles", "lightgray"),
        ("Drawer Face", "orange"),
        ("Box Drawer", "powderblue"),
    ]
    
    for i, (texto, color) in enumerate(legend_items):
        canvas.create_rectangle(
            legend_x,
            legend_y + i*20,
            legend_x + 20,
            legend_y + i*20 + 15,
            fill=color
        )
        canvas.create_text(
            legend_x + 30,
            legend_y + i*20 + 7,
            text=texto,
            anchor="w"
        )

def dibujar_vista_frontal_dos_puertas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio):
    espesor = gabinete["Espesor"]
    gap = 0.125

    # Dibujar marco exterior
    canvas.create_rectangle(
        x_inicio, y_inicio,
        x_inicio + escalar(gabinete["Ancho"]),
        y_inicio + escalar(gabinete["Alto"]),
        outline='black', width=1
    )

    # Dibujar los costados
    canvas.create_line(x_inicio + escalar(espesor), y_inicio,
                       x_inicio + escalar(espesor), y_inicio + escalar(gabinete["Alto"]),
                       fill='gray', width=1)
    canvas.create_line(x_inicio + escalar(gabinete["Ancho"] - espesor), y_inicio,
                       x_inicio + escalar(gabinete["Ancho"] - espesor), y_inicio + escalar(gabinete["Alto"]),
                       fill='gray', width=1)

    # Dibujar entrepano
    entrepano_y = y_inicio + escalar(gabinete["Alto"] / 2)
    canvas.create_line(
        x_inicio + escalar(espesor), entrepano_y,
        x_inicio + escalar(gabinete["Ancho"] - espesor), entrepano_y,
        fill='gray', width=2
    )

    # Dibujar puertas
    if gabinete["Ancho"] > 18:
        ancho_puerta = (gabinete["Ancho"] / 2) - (gap / 2)

        # Puerta izquierda
        canvas.create_rectangle(
            x_inicio + escalar(gap/2), y_inicio + escalar(gap/2),
            x_inicio + escalar(ancho_puerta), y_inicio + escalar(gabinete["Alto"] - gap/2),
            fill='lightyellow', outline='black', width=1
        )
        
        # Puerta derecha
        canvas.create_rectangle(
            x_inicio + escalar(gabinete["Ancho"]/2 + gap/2), y_inicio + escalar(gap/2),
            x_inicio + escalar(gabinete["Ancho"] - gap/2), y_inicio + escalar(gabinete["Alto"] - gap/2),
            fill='lightyellow', outline='black', width=1
        )

        # Línea divisoria vertical (entre las dos puertas)
        canvas.create_line(
            x_inicio + escalar(gabinete["Ancho"]/2), y_inicio + escalar(gap/2),
            x_inicio + escalar(gabinete["Ancho"]/2), y_inicio + escalar(gabinete["Alto"] - gap/2),
            fill='black', width=1
        )
    else:
        # Puerta única (cuando el ancho es 18 o menor)
        canvas.create_rectangle(
            x_inicio + escalar(gap/2), y_inicio + escalar(gap/2),
            x_inicio + escalar(gabinete["Ancho"] - gap/2), y_inicio + escalar(gabinete["Alto"] - gap/2),
            fill='lightyellow', outline='black', width=1
        )


   # Añadir dimensiones
    canvas.create_text(
        x_inicio + escalar(gabinete["Ancho"]/2),
        y_inicio - 20,
        text=f"Ancho: {gabinete['Ancho']}\"",
        anchor="center"
    )
    canvas.create_text(
        x_inicio - 20,
        y_inicio + escalar(gabinete["Alto"]/2),
        text=f"Alto: {gabinete['Alto']}\"",
        anchor="center",
        angle=90
    )
        
def dibujar_vista_lateral_dos_puertas(canvas, gabinete, piezas, escalar, x_inicio, y_inicio):
    espesor = gabinete["Espesor"]
    profundidad = gabinete["Profundidad"]
    espesor_puerta = 0.75
    gap = 0.125

    # Dibujar marco exterior (vista lateral)
    canvas.create_rectangle(
        x_inicio, y_inicio,
        x_inicio + escalar(profundidad),
        y_inicio + escalar(gabinete["Alto"]),
        outline='black', width=1
    )

    # Dibujar techo y piso
    canvas.create_line(
        x_inicio, y_inicio + escalar(espesor),
        x_inicio + escalar(profundidad), y_inicio + escalar(espesor),
        fill='gray', width=1
    )
    canvas.create_line(
        x_inicio, y_inicio + escalar(gabinete["Alto"] - espesor),
        x_inicio + escalar(profundidad), y_inicio + escalar(gabinete["Alto"] - espesor),
        fill='gray', width=1
    )

    # Dibujar respaldo
    canvas.create_line(
        x_inicio + escalar(profundidad - espesor), y_inicio,
        x_inicio + escalar(profundidad - espesor), y_inicio + escalar(gabinete["Alto"]),
        fill='gray', width=1
    )

    # Dibujar entrepano (en la mitad de la altura)
    entrepano_y = y_inicio + escalar(gabinete["Alto"] / 2)
    canvas.create_line(
        x_inicio, entrepano_y,
        x_inicio + escalar(profundidad - espesor), entrepano_y,
        fill='gray', width=2
    )

    # Dibujar puertas como un rectángulo con espesor de 0.75"
    canvas.create_rectangle(
        x_inicio + escalar(gap/2), y_inicio + escalar(gap/2),
        x_inicio + escalar(gap/2 + espesor_puerta), y_inicio + escalar(gabinete["Alto"] - gap/2),
        fill='lightyellow', outline='black', width=1
    )

    # Añadir dimensiones
    canvas.create_text(
        x_inicio + escalar(profundidad/2),
        y_inicio - 20,
        text=f"Profundidad: {profundidad}\"",
        anchor="center"
    )
    canvas.create_text(
        x_inicio - 20,
        y_inicio + escalar(gabinete["Alto"]/2),
        text=f"Alto: {gabinete['Alto']}\"",
        anchor="center",
        angle=90
    )

    # Añadir etiqueta para identificar que es vista lateral
    canvas.create_text(
        x_inicio + escalar(profundidad/2),
        y_inicio + escalar(gabinete["Alto"]) + 20,
        text="Vista Lateral",
        anchor="center",
        font=("Arial", 10, "bold")
    )
