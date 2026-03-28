# 📦 Sistema de Inventario

Aplicación de escritorio para la gestión de inventario desarrollada en **Python**, con arquitectura modular (MVC + servicios) y base de datos local en SQLite.

---

## 🚀 Descripción

Este sistema permite administrar productos, usuarios, ventas y clientes desde una interfaz gráfica organizada. Está diseñado para ser escalable, mantenible y fácil de usar.

El proyecto fue desarrollado con apoyo de herramientas de inteligencia artificial (Antigravity), combinando automatización con validación manual del código.

---

## 🧠 Arquitectura del proyecto

El sistema sigue una estructura modular basada en separación de responsabilidades:

* **models/** → Representación de datos (entidades)
* **services/** → Lógica de negocio
* **ui/** → Interfaz gráfica
* **database/** → Conexión y gestión de base de datos
* **utils/** → Funciones auxiliares

---

## 📂 Estructura del proyecto

```bash
Sistema_Inventario/
│── database/
│   └── db.py
│
│── models/
│   ├── persona.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
│
│── services/
│   ├── auth_service.py
│   ├── persona_service.py
│   ├── producto_service.py
│   ├── usuario_service.py
│   └── venta_service.py
│
│── ui/
│   ├── login_window.py
│   ├── main_window.py
│   ├── inventario_view.py
│   ├── ventas_view.py
│   ├── usuarios_view.py
│   ├── personas_view.py
│   └── historial_ventas_view.py
│
│── utils/
│   ├── helpers.py
│   └── api_celular.py
│
│── inventario.db
│── main.py
│── README.md
```

---

## 🔐 Funcionalidades principales

* 🔑 Sistema de autenticación (login de usuarios)
* 📦 Gestión de productos
* 👥 Gestión de usuarios y personas
* 💰 Registro de ventas
* 📊 Historial de ventas
* 🗄️ Base de datos local (SQLite)

---

## ⚙️ Tecnologías utilizadas

* **Python**
* **SQLite**
* **Arquitectura modular (MVC adaptado)**
* **Git & GitHub**

---

## 🗄️ Base de datos

El sistema utiliza **SQLite local**, lo que significa:

* No requiere servidor
* Funciona directamente en el equipo
* Ideal para proyectos pequeños y medianos

Archivo:

```
inventario.db
```

---

## 🤖 Uso de Inteligencia Artificial

Este proyecto fue desarrollado con apoyo de herramientas de IA (Antigravity de Google).

El código generado fue:

* Revisado manualmente
* Ajustado a necesidades reales
* Optimizado para mantener buenas prácticas

---

## 📦 Versión ejecutable

El proyecto incluye una versión ejecutable:

```
Sistema_de_Inventario_Portable.exe
```

Permite ejecutar la aplicación sin necesidad de instalar Python.

---

## 📈 Estado del proyecto

🟡 En desarrollo / mejoras en curso

---

## 👨‍💻 Autor

**José Manuel Correa**
Desarrollador enfocado en frontend y desarrollo de software asistido con IA.

---
