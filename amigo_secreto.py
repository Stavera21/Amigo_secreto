
import random
import tkinter as tk
from tkinter import ttk, messagebox

import ttkbootstrap as tb
from ttkbootstrap.constants import *


# ----------------------------
# LÓGICA
# ----------------------------

def sortear_amigo_secreto(lista_participantes, lista_opciones_participantes, intentos_maximos=2000):
    for _ in range(intentos_maximos):
        try:
            asignaciones = {}
            opciones_disponibles = lista_opciones_participantes.copy()

            if "jessica" in [p.lower() for p in lista_participantes]:
                asignaciones["jessica"] = "santiago"

            resto_participantes = [p for p in lista_participantes if p.lower() != "jessica"]
            random.shuffle(resto_participantes)

            for p in resto_participantes:
                candidatos = [o for o in opciones_disponibles if o.lower() != p.lower()]
                if not candidatos:
                    raise ValueError("sorteo_atorado")
                elegido = random.choice(candidatos)
                asignaciones[p] = elegido
                opciones_disponibles.remove(elegido)

            return asignaciones

        except ValueError:
            continue

    raise RuntimeError(
        "No fue posible generar un sorteo válido. Agrega al menos un "
        "participante más o revisa las restricciones del grupo."
    )


def es_nombre_valido_para_opciones(nombre):
    return nombre.lower() not in ("santi", "santiago")


# ----------------------------
# PALETA PASTEL
# ----------------------------

class Paleta:
    FONDO = "#FBF7F2"       # crema cálido
    TARJETA = "#FFFFFF"
    BORDE = "#EDE6DC"
    TEXTO = "#4A4642"
    MUTED = "#A79E93"
    PRIMARIO = "#8FBFAE"    # verde salvia pastel
    PRIMARIO_HOVER = "#79AC98"
    PRIMARIO_SUAVE = "#E4F0EB"
    ACENTO = "#F2B6A0"      # coral pastel (detalles secundarios)
    OSCURO = "#6B6560"      # botón "siguiente" neutro


# ----------------------------
# WIDGETS REDONDEADOS (dibujados con Canvas)
# ----------------------------

def _puntos_rect_redondeado(x1, y1, x2, y2, r):
    return [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]


class BotonRedondeado(tk.Canvas):
    """Botón con esquinas redondeadas reales, dibujado con Canvas."""

    def __init__(self, parent, text, command=None, bg_parent=Paleta.TARJETA,
                 color=Paleta.PRIMARIO, color_hover=None, fg="white",
                 font=("Helvetica", 11, "bold"), radius=14, height=44, **kwargs):
        super().__init__(parent, height=height, bg=bg_parent, highlightthickness=0,
                          bd=0, **kwargs)
        self.command = command
        self.text = text
        self.color = color
        self.color_hover = color_hover or color
        self.fg = fg
        self.font = font
        self.radius = radius
        self._hover = False

        self.bind("<Configure>", self._redibujar)
        self.bind("<Button-1>", self._click)
        self.bind("<Enter>", self._entrar)
        self.bind("<Leave>", self._salir)
        self.configure(cursor="hand2")

    def _redibujar(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 4 or h < 4:
            return
        color = self.color_hover if self._hover else self.color
        pts = _puntos_rect_redondeado(1, 1, w - 1, h - 1, self.radius)
        self.create_polygon(pts, smooth=True, fill=color, outline=color)
        self.create_text(w / 2, h / 2, text=self.text, fill=self.fg, font=self.font)

    def _click(self, event=None):
        if self.command:
            self.command()

    def _entrar(self, event=None):
        self._hover = True
        self._redibujar()

    def _salir(self, event=None):
        self._hover = False
        self._redibujar()

    def set_text(self, texto):
        self.text = texto
        self._redibujar()


class TarjetaRedondeada(tk.Frame):
    """
    Contenedor con esquinas redondeadas reales: un Canvas de fondo dibuja el
    rectángulo redondeado, y encima se coloca un Frame normal (mismo color)
    donde se empaquetan los widgets de contenido, ligeramente encogido para
    dejar ver las esquinas curvas del canvas.
    """

    def __init__(self, parent, bg_parent=Paleta.FONDO, color=Paleta.TARJETA,
                 radius=22, padding=22, **kwargs):
        super().__init__(parent, bg=bg_parent, **kwargs)
        self._canvas = tk.Canvas(self, bg=bg_parent, highlightthickness=0, bd=0)
        self._canvas.pack(fill=BOTH, expand=True)
        self._color = color
        self._radius = radius

        self.contenido = tk.Frame(self._canvas, bg=color)
        self._canvas.bind("<Configure>", self._redibujar)
        self._ventana_id = None
        self._padding = padding

    def _redibujar(self, event=None):
        w = event.width if event else self._canvas.winfo_width()
        h = event.height if event else self._canvas.winfo_height()
        self._canvas.delete("fondo")
        if w < 4 or h < 4:
            return
        pts = _puntos_rect_redondeado(1, 1, w - 1, h - 1, self._radius)
        self._canvas.create_polygon(pts, smooth=True, fill=self._color,
                                     outline=self._color, tags="fondo")
        self._canvas.tag_lower("fondo")

        if self._ventana_id is None:
            self._ventana_id = self._canvas.create_window(
                self._padding, self._padding, anchor="nw", window=self.contenido,
            )
        self._canvas.coords(self._ventana_id, self._padding, self._padding)
        self._canvas.itemconfig(
            self._ventana_id,
            width=max(w - 2 * self._padding, 10),
            height=max(h - 2 * self._padding, 10),
        )


class Pill(tk.Canvas):
    """Insignia pequeña tipo 'pill' con esquinas totalmente redondas."""

    def __init__(self, parent, text, bg_parent=Paleta.TARJETA,
                 color=Paleta.PRIMARIO, fg="white", font=("Helvetica", 9, "bold"),
                 **kwargs):
        super().__init__(parent, height=26, bg=bg_parent, highlightthickness=0, bd=0, **kwargs)
        self.color = color
        self.fg = fg
        self.font = font
        self._text = text
        self.bind("<Configure>", self._redibujar)

    def _redibujar(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 4 or h < 4:
            return
        r = h / 2
        pts = _puntos_rect_redondeado(1, 1, w - 1, h - 1, r)
        self.create_polygon(pts, smooth=True, fill=self.color, outline=self.color)
        self.create_text(w / 2, h / 2, text=self._text, fill=self.fg, font=self.font)

    def set_text(self, texto):
        self._text = texto
        self._redibujar()


# ----------------------------
# APP
# ----------------------------

class AmigoSecretoApp(tb.Window):
    PLACEHOLDER = "Selecciona tu nombre..."

    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Amigo Secreto")
        self.geometry("480x700")
        self.configure(bg=Paleta.FONDO)
        self.resizable(False, False)

        self._construir_estilo()

        self.lista_participantes = []
        self.lista_opciones_participantes = []
        self.asignaciones = {}
        self.ya_revelados = set()

        self._construir_pantalla_agregar()

    def _construir_estilo(self):
        style = self.style
        style.configure("TFrame", background=Paleta.FONDO)

        # Entry / Combobox: sin bordes duros, pastel
        style.configure(
            "Pastel.TEntry", fieldbackground="#FDFBF9", foreground=Paleta.TEXTO,
            bordercolor=Paleta.BORDE, lightcolor=Paleta.BORDE, darkcolor=Paleta.BORDE,
            insertcolor=Paleta.TEXTO, borderwidth=1, padding=10, relief="flat",
        )
        style.map("Pastel.TEntry", bordercolor=[("focus", Paleta.PRIMARIO)])

        style.configure(
            "Pastel.TCombobox", fieldbackground="#FDFBF9", foreground=Paleta.TEXTO,
            background="#FDFBF9", arrowcolor=Paleta.PRIMARIO, bordercolor=Paleta.BORDE,
            lightcolor=Paleta.BORDE, darkcolor=Paleta.BORDE, padding=10, borderwidth=1,
            relief="flat",
        )
        style.map("Pastel.TCombobox", bordercolor=[("focus", Paleta.PRIMARIO)])
        self.option_add("*TCombobox*Listbox*Background", "#FDFBF9")
        self.option_add("*TCombobox*Listbox*Foreground", Paleta.TEXTO)
        self.option_add("*TCombobox*Listbox*selectBackground", Paleta.PRIMARIO_SUAVE)
        self.option_add("*TCombobox*Listbox*selectForeground", Paleta.TEXTO)

        style.configure(
            "Pastel.Horizontal.TProgressbar", troughcolor=Paleta.PRIMARIO_SUAVE,
            background=Paleta.PRIMARIO, bordercolor=Paleta.PRIMARIO_SUAVE,
            lightcolor=Paleta.PRIMARIO, darkcolor=Paleta.PRIMARIO,
        )

    # ---------- utilidades ----------

    def _limpiar_pantalla(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _header(self, parent, icono, titulo, subtitulo):
        tk.Label(
            parent, text=f"{icono}  {titulo}", bg=Paleta.FONDO, fg=Paleta.TEXTO,
            font=("Helvetica", 22, "bold"),
        ).pack(anchor="w")
        tk.Label(
            parent, text=subtitulo, bg=Paleta.FONDO, fg=Paleta.MUTED,
            font=("Helvetica", 10), wraplength=420, justify="left",
        ).pack(anchor="w", pady=(4, 22))

    def _etiqueta(self, parent, texto, tamano=9, negrita=True, color=None, fondo=Paleta.TARJETA):
        return tk.Label(
            parent, text=texto, bg=fondo, fg=color or Paleta.MUTED,
            font=("Helvetica", tamano, "bold" if negrita else "normal"),
        )

    # ---------- Pantalla 1: agregar participantes ----------

    def _construir_pantalla_agregar(self):
        self._limpiar_pantalla()
        self.asignaciones = {}
        self.ya_revelados = set()

        contenedor = tk.Frame(self, bg=Paleta.FONDO, padx=28, pady=28)
        contenedor.pack(fill=BOTH, expand=True)

        self._header(
            contenedor, "🎁", "Amigo Secreto",
            "Agrega a cada participante. Cuando estén todos, presiona Continuar.",
        )

        tarjeta = TarjetaRedondeada(contenedor, bg_parent=Paleta.FONDO, padding=22)
        tarjeta.pack(fill=BOTH, expand=True)
        interior = tarjeta.contenido

        fila_entry = tk.Frame(interior, bg=Paleta.TARJETA)
        fila_entry.pack(fill=X, pady=(0, 16))

        self.entry_nombre = ttk.Entry(fila_entry, style="Pastel.TEntry", font=("Helvetica", 12))
        self.entry_nombre.pack(side=LEFT, fill=X, expand=True, ipady=5)
        self.entry_nombre.bind("<Return>", lambda e: self._agregar_participante())
        self.entry_nombre.focus()

        BotonRedondeado(
            fila_entry, "＋ Agregar", command=self._agregar_participante,
            bg_parent=Paleta.TARJETA, color=Paleta.PRIMARIO,
            color_hover=Paleta.PRIMARIO_HOVER, width=110, height=40,
        ).pack(side=LEFT, padx=(10, 0))

        fila_header = tk.Frame(interior, bg=Paleta.TARJETA)
        fila_header.pack(fill=X, pady=(0, 8))
        self._etiqueta(fila_header, "PARTICIPANTES").pack(side=LEFT)
        self.badge_contador = Pill(
            fila_header, "0", bg_parent=Paleta.TARJETA, color=Paleta.PRIMARIO,
            width=34,
        )
        self.badge_contador.pack(side=RIGHT)

        lista_wrap = tk.Frame(interior, bg=Paleta.BORDE)
        lista_wrap.pack(fill=BOTH, expand=True)

        self.lista_visual = tk.Listbox(
            lista_wrap, height=10, font=("Helvetica", 12),
            bg="#FDFBF9", fg=Paleta.TEXTO, relief="flat",
            selectbackground=Paleta.PRIMARIO_SUAVE, selectforeground=Paleta.TEXTO,
            highlightthickness=0, activestyle="none", bd=0,
        )
        self.lista_visual.pack(fill=BOTH, expand=True, padx=1, pady=1)
        self.lista_visual.bind("<Delete>", lambda e: self._quitar_participante())
        self.lista_visual.bind("<Double-Button-1>", lambda e: self._quitar_participante())

        tk.Label(
            contenedor, text="Doble clic (o Supr) sobre un nombre para quitarlo",
            bg=Paleta.FONDO, fg=Paleta.MUTED, font=("Helvetica", 8),
        ).pack(anchor="w", pady=(8, 16))

        BotonRedondeado(
            contenedor, "Continuar  →", command=self._terminar_agregar,
            bg_parent=Paleta.FONDO, color=Paleta.PRIMARIO,
            color_hover=Paleta.PRIMARIO_HOVER, height=46,
        ).pack(fill=X)

    def _agregar_participante(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            return
        if nombre.lower() in [p.lower() for p in self.lista_participantes]:
            messagebox.showwarning("Nombre repetido", f"'{nombre}' ya fue agregado.")
            self.entry_nombre.delete(0, tk.END)
            return

        self.lista_participantes.append(nombre)
        self.lista_visual.insert(tk.END, f"   {nombre}")

        if es_nombre_valido_para_opciones(nombre):
            self.lista_opciones_participantes.append(nombre)

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.focus()
        self.badge_contador.set_text(str(len(self.lista_participantes)))

    def _quitar_participante(self):
        seleccion = self.lista_visual.curselection()
        if not seleccion:
            return
        idx = seleccion[0]
        nombre = self.lista_participantes.pop(idx)
        self.lista_visual.delete(idx)
        if nombre in self.lista_opciones_participantes:
            self.lista_opciones_participantes.remove(nombre)
        self.badge_contador.set_text(str(len(self.lista_participantes)))

    def _terminar_agregar(self):
        if len(self.lista_participantes) < 2:
            messagebox.showwarning(
                "Faltan participantes", "Agrega al menos 2 participantes antes de continuar.",
            )
            return
        self._construir_pantalla_seleccion()

    # ---------- Pantalla 2: elegir quién eres y sortear ----------

    def _construir_pantalla_seleccion(self):
        self._limpiar_pantalla()

        contenedor = tk.Frame(self, bg=Paleta.FONDO, padx=28, pady=28)
        contenedor.pack(fill=BOTH, expand=True)

        self._header(
            contenedor, "🔒", "Turno privado",
            "Pasa el computador de mano en mano. Cada quien ve solo su propio resultado.",
        )

        self.tarjeta_seleccion = TarjetaRedondeada(contenedor, bg_parent=Paleta.FONDO, padding=22)
        self.tarjeta_seleccion.pack(fill=BOTH, expand=True)

        self._render_estado_seleccion()

        BotonRedondeado(
            contenedor, "←  Editar participantes", command=self._confirmar_volver,
            bg_parent=Paleta.FONDO, color=Paleta.FONDO, color_hover=Paleta.BORDE,
            fg=Paleta.MUTED, font=("Helvetica", 10), height=38,
        ).pack(fill=X, pady=(14, 0))

    def _render_estado_seleccion(self):
        interior = self.tarjeta_seleccion.contenido
        for widget in interior.winfo_children():
            widget.destroy()

        pendientes = [p for p in self.lista_participantes if p.lower() not in self.ya_revelados]
        total = len(self.lista_participantes)
        hechos = len(self.ya_revelados)

        fila_header = tk.Frame(interior, bg=Paleta.TARJETA)
        fila_header.pack(fill=X, pady=(0, 8))
        self._etiqueta(fila_header, "¿QUIÉN ERES?").pack(side=LEFT)
        Pill(
            fila_header, f"{hechos}/{total}", bg_parent=Paleta.TARJETA,
            color=Paleta.PRIMARIO, width=54,
        ).pack(side=RIGHT)

        progreso = ttk.Progressbar(
            interior, style="Pastel.Horizontal.TProgressbar",
            maximum=total, value=hechos,
        )
        progreso.pack(fill=X, pady=(0, 18))

        if not pendientes:
            tk.Label(
                interior, text="🎉", font=("Helvetica", 40), bg=Paleta.TARJETA,
            ).pack(pady=(20, 6))
            self._etiqueta(
                interior, "Todos ya revelaron su amigo secreto", tamano=12, negrita=False,
            ).pack()
            self.frame_resultado = tk.Frame(interior, bg=Paleta.TARJETA)
            self.frame_resultado.pack(fill=BOTH, expand=True)
            return

        self.combo_usuario = ttk.Combobox(
            interior, values=pendientes, state="readonly",
            font=("Helvetica", 12), style="Pastel.TCombobox",
        )
        self.combo_usuario.set(self.PLACEHOLDER)
        self.combo_usuario.pack(fill=X, ipady=5, pady=(0, 16))

        self.boton_buscar = BotonRedondeado(
            interior, "🔍  Revelar mi amigo secreto", command=self._buscar_resultado,
            bg_parent=Paleta.TARJETA, color=Paleta.PRIMARIO,
            color_hover=Paleta.PRIMARIO_HOVER, height=46,
        )
        self.boton_buscar.pack(fill=X)

        self.frame_resultado = tk.Frame(interior, bg=Paleta.TARJETA)
        self.frame_resultado.pack(fill=BOTH, expand=True, pady=(20, 0))

    def _buscar_resultado(self):
        usuario = self.combo_usuario.get()
        if not usuario or usuario == self.PLACEHOLDER:
            messagebox.showwarning("Falta seleccionar", "Selecciona tu nombre primero.")
            return

        if not self.asignaciones:
            try:
                self.asignaciones = sortear_amigo_secreto(
                    self.lista_participantes, self.lista_opciones_participantes
                )
            except RuntimeError as e:
                messagebox.showerror("Error en el sorteo", str(e))
                return

        resultado = None
        for clave, valor in self.asignaciones.items():
            if clave.lower() == usuario.lower():
                resultado = valor
                break

        self.ya_revelados.add(usuario.lower())

        self.combo_usuario.pack_forget()
        self.boton_buscar.pack_forget()

        for widget in self.frame_resultado.winfo_children():
            widget.destroy()

        self._etiqueta(
            self.frame_resultado, f"Hola, {usuario.capitalize()} 👋", tamano=11, negrita=False,
        ).pack(pady=(6, 10))
        self._etiqueta(
            self.frame_resultado, "Tu amigo secreto es", tamano=11, negrita=False,
        ).pack()
        self._etiqueta(
            self.frame_resultado, resultado.capitalize(), tamano=30, color=Paleta.PRIMARIO_HOVER,
        ).pack(pady=(2, 26))

        BotonRedondeado(
            self.frame_resultado, "Listo, siguiente persona  →", command=self._render_estado_seleccion,
            bg_parent=Paleta.TARJETA, color=Paleta.OSCURO, color_hover="#57524D", height=46,
        ).pack(fill=X)

    def _confirmar_volver(self):
        if messagebox.askyesno(
            "Volver a editar",
            "Si editas la lista de participantes, se reiniciará el sorteo actual. ¿Continuar?",
        ):
            self._construir_pantalla_agregar()


if __name__ == "__main__":
    app = AmigoSecretoApp()
    app.mainloop()