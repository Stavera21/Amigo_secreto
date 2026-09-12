# # 🎁 Amigo Secreto

Aplicación de escritorio en Python para organizar un sorteo de amigo secreto, con una interfaz gráfica pensada para que el mismo dispositivo se pase de mano en mano: cada participante ve **únicamente su propio resultado**.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter%20%2B%20ttkbootstrap-8FBFAE)
![Estado](https://img.shields.io/badge/estado-funcional-brightgreen)

---

## ✨ Características

- **Interfaz gráfica moderna**: paleta pastel, esquinas redondeadas y componentes construidos sobre [ttkbootstrap](https://ttkbootstrap.readthedocs.io/).
- **Sorteo justo y sin repeticiones**: nadie recibe el mismo amigo secreto que otra persona, y nadie se auto-asigna.
- **Reintento automático**: si el sorteo "se atora" (el último participante se queda sin opciones válidas), se reintenta solo hasta encontrar una combinación válida.
- **Regla de negocio configurable**: por defecto, `jessica` siempre tiene fijo a `santiago`, y `santiago` nunca puede tocarle a nadie más (ver [Personalizar las reglas](#-personalizar-las-reglas)).
- **Privacidad entre turnos**: al revelar un resultado, la persona queda marcada como "ya reveló" y desaparece del selector, evitando que alguien vea el nombre de otro por accidente.
- **Barra de progreso** con el conteo de cuántos participantes ya revelaron su resultado.

## 📋 Requisitos

- Python 3.9 o superior
- [ttkbootstrap](https://pypi.org/project/ttkbootstrap/)
- Tkinter (incluido con Python en Windows/macOS; en Linux puede requerir instalación aparte)

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/amigo-secreto.git
cd amigo-secreto

# Instalar la dependencia
pip install ttkbootstrap
```

### En Linux

Si no tienes Tkinter instalado (algunas distribuciones no lo incluyen por defecto):

```bash
sudo apt-get install python3-tk
```

## ▶️ Uso

```bash
python amigo_secreto.py
```

1. **Agregar participantes**: escribe cada nombre y presiona `Agregar` (o `Enter`). Puedes quitar a alguien con doble clic o la tecla `Supr` sobre su nombre en la lista.
2. **Continuar**: cuando estén todos, presiona `Continuar →`.
3. **Turno privado**: cada persona selecciona su nombre en el menú desplegable y presiona `Revelar mi amigo secreto`.
4. **Pasar el turno**: tras ver el resultado, presiona `Listo, siguiente persona →` antes de pasarle el computador a alguien más. Esa persona ya no podrá volver a seleccionarse ni ver el resultado ajeno.

## ⚙️ Personalizar las reglas

La lógica del sorteo vive en la función `sortear_amigo_secreto()`, dentro de `amigo_secreto.py`. Por defecto incluye una regla de ejemplo:

```python
if "jessica" in [p.lower() for p in lista_participantes]:
    asignaciones["jessica"] = "santiago"
```

Y en `es_nombre_valido_para_opciones()`, `santiago`/`santi` está excluido de la lista de posibles asignaciones:

```python
def es_nombre_valido_para_opciones(nombre):
    return nombre.lower() not in ("santi", "santiago")
```

Para adaptarlo a tu propio grupo:
- Cambia los nombres fijos en `sortear_amigo_secreto()`.
- Cambia la lista de exclusión en `es_nombre_valido_para_opciones()`.
- Si no necesitas ninguna regla especial, elimina ambos bloques y el sorteo será completamente aleatorio (solo evitando auto-asignaciones y duplicados).

## 🗂️ Estructura del proyecto

```
amigo-secreto/
├── amigo_secreto.py   # Lógica del sorteo + interfaz gráfica
└── README.md
```

## 🛣️ Posibles mejoras futuras

- Versión web estática (HTML/CSS/JS) para desplegar en Vercel u otro hosting gratuito.
- Guardar/cargar la lista de participantes desde un archivo.
- Exportar los resultados cifrados para enviarlos individualmente (correo, WhatsApp, etc.).

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Siéntete libre de usarlo, modificarlo y compartirlo.