# 🍽 restaurante_app — Semana 16
**Programación Orientada a Objetos — Universidad Estatal Amazónica**  
Tema: **Manejo de eventos en Tkinter**

---

## Propósito de la Semana 16

Esta semana extiende la aplicación desarrollada en semanas anteriores para incorporar
el **manejo explícito de eventos en Tkinter**. El contexto es la gestión de usuarios:
se implementa un CRUD completo (registrar, consultar, actualizar y eliminar) activado
mediante diferentes mecanismos de interacción, manteniendo la arquitectura modular
y la persistencia en archivos JSON sin filtrar lógica de negocio hacia la interfaz.

---

## Evolución respecto a semanas anteriores

| Semana | Novedad principal |
|--------|-------------------|
| 13 | Migración de consola a Tkinter; LoginView + MainView |
| 14 | Componentes, contenedores, tablas Treeview, CRUD Productos |
| 15 | Modelo Venta, ventas.json, sección Ventas con Combobox y command= |
| **16** | **Atributo `rol` en Usuario; CRUD completo de Usuarios; `<<TreeviewSelect>>`, `<Return>`, `<Escape>`, `<<ComboboxSelected>>`; acceso restringido por rol** |

---

## Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py        ← atributo rol (Administrador / Empleado / Cliente)
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py   ← CRUD completo de usuarios con reglas
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py      ← sección Usuarios con todos los eventos S16
├── assets/
│   ├── logo.png
│   ├── generar_assets.py
│   └── icon_*.png
├── main.py
└── README.md
```

---

## Gestión de usuarios y roles

El modelo `Usuario` incorpora el atributo `rol` con tres valores posibles:

- **Administrador** — accede a la sección *Usuarios* y puede gestionar Empleados y Clientes.
- **Empleado** — accede a Productos y Ventas; no ve la sección Usuarios.
- **Cliente** — acceso básico; no ve la sección Usuarios.

### Reglas de negocio (en `RestauranteServicio`)

- Solo se pueden crear usuarios de tipo **Empleado** o **Cliente** desde la interfaz.
- El administrador autenticado **no puede eliminar su propia cuenta**.
- El administrador autenticado **no puede modificar otro Administrador**.
- El administrador **no puede degradar su propio rol**.
- No se permiten nombres de usuario duplicados.

---

## Eventos implementados — Semana 16

### `<<TreeviewSelect>>` via `bind()`
Al seleccionar una fila en la tabla de usuarios, se activa el callback
`_al_seleccionar_usuario(event)`. Este obtiene el identificador de la fila,
consulta el objeto `Usuario` en `RestauranteServicio` y carga los datos en
el formulario. La contraseña **no se muestra** por seguridad.

```python
self._tabla_usuarios.bind("<<TreeviewSelect>>", self._al_seleccionar_usuario)

def _al_seleccionar_usuario(self, event):
    seleccion = self._tabla_usuarios.selection()
    if not seleccion:
        return
    valores = self._tabla_usuarios.item(seleccion[0], "values")
    usuario = self._servicio.buscar_usuario(valores[0])   # delega al servicio
    if usuario:
        self._cargar_usuario_en_formulario(usuario)
```

### `<Return>` via `bind()`
Presionar **Enter** en cualquier campo del formulario de usuarios ejecuta el
registro reutilizando `_registrar_usuario()`, sin duplicar la lógica.

```python
entry.bind("<Return>", self._al_presionar_enter)

def _al_presionar_enter(self, event):
    self._registrar_usuario()   # reutiliza el método, no duplica lógica
```

### `<Escape>` via `bind()`
Presionar **Escape** limpia el formulario y cancela la selección activa en el Treeview.

```python
entry.bind("<Escape>", self._al_presionar_escape)

def _al_presionar_escape(self, event):
    self._limpiar_formulario_usuario()
```

### `<<ComboboxSelected>>` via `bind()`
Al cambiar el rol en el Combobox, se actualiza la etiqueta informativa del formulario.

```python
self._combo_rol.bind("<<ComboboxSelected>>", self._al_seleccionar_rol)

def _al_seleccionar_rol(self, event):
    rol = self._u_rol_var.get()
    self._lbl_info_rol.config(text=f"ℹ  Rol seleccionado: {rol} — ...")
```

### `command=` en botones
Los botones principales usan `command=` (no `bind()`), diferenciando ambos mecanismos:

```python
ttk.Button(frame, text="✔ Registrar",  command=self._registrar_usuario)
ttk.Button(frame, text="✏ Actualizar", command=self._actualizar_usuario)
ttk.Button(frame, text="🗑 Eliminar",  command=self._eliminar_usuario)
ttk.Button(frame, text="⟳ Limpiar",   command=self._limpiar_formulario_usuario)
```

---

## Diferencia entre `command=` y `bind()`

| Aspecto | `command=` | `bind()` |
|---------|-----------|---------|
| Tipo de acción | Acción principal de un widget | Evento específico (tecla, selección…) |
| Uso típico | Botones | Treeview, Entry, Combobox |
| Callback recibe | Sin parámetro `event` | Parámetro `event` |
| Ejemplo en el proyecto | Botón Registrar | `<<TreeviewSelect>>`, `<Return>` |

---

## Flujo principal de la sección Usuarios

```
Usuario selecciona fila en Treeview
        ↓
<<TreeviewSelect>> → bind() → _al_seleccionar_usuario(event)
        ↓
Obtiene identificador de la fila (no datos sensibles)
        ↓
RestauranteServicio.buscar_usuario(id)
        ↓
_cargar_usuario_en_formulario(usuario)
        ↓
Usuario edita datos → Actualizar / Eliminar / Enter
        ↓
RestauranteServicio aplica reglas y persiste en usuarios.json
        ↓
_actualizar_tabla_usuarios() → respuesta visual
```

---

## Persistencia

Los cambios en usuarios se persisten inmediatamente en `datos/usuarios.json`
a través de `ArchivoServicio.guardar_usuarios()`, invocado desde
`RestauranteServicio`. La interfaz nunca lee ni escribe JSON directamente.

---

## Cómo ejecutar

### Requisitos
```
Python 3.10+
Pillow  (pip install Pillow)
```

### Pasos
```bash
# 1. Instalar dependencia
pip install Pillow

# 2. (Opcional) Regenerar assets
python assets/generar_assets.py

# 3. Ejecutar
python main.py
```

### Credenciales de prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| `admin` | `admin123` | Administrador |
| `cmora` | `emp123`   | Empleado |
| `lperez`| `cli123`   | Cliente |

---

## Comprobación de funcionalidades Semana 16

- [x] Login con validación y tecla Enter
- [x] Navegación por sección según rol (Usuarios solo para Administrador)
- [x] CRUD completo de usuarios desde la interfaz
- [x] `<<TreeviewSelect>>` carga el usuario seleccionado en el formulario
- [x] `<Return>` registra usuario desde el formulario
- [x] `<Escape>` limpia formulario y selección
- [x] `<<ComboboxSelected>>` actualiza etiqueta informativa del rol
- [x] `command=` en botones principales
- [x] Reglas de negocio en `RestauranteServicio` (no en la interfaz)
- [x] Persistencia en `usuarios.json`
- [x] Productos y Ventas continúan funcionando
- [x] Assets con logo e íconos en carpeta `assets/`
