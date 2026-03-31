# 📦 Sistema de Inventario / InventarioJC

Aplicación de escritorio para la gestión de inventario desarrollada en **Python**, con arquitectura modular (MVC + servicios) y base de datos local en SQLite.

---

## 🚀 Descripción

Este sistema permite administrar productos, usuarios, ventas y clientes desde una interfaz gráfica organizada. Está diseñado para ser escalable, mantenible y fácil de usar, permitiendo búsquedas dinámicas en tiempo real cuando hay grandes volúmenes de datos.

El proyecto fue desarrollado con apoyo de herramientas de inteligencia artificial (Antigravity), combinando automatización con validación manual del código.

---

## 🧠 Arquitectura del proyecto

El sistema sigue una estructura modular basada en separación de responsabilidades:

* **models/** → Representación de datos (entidades)
* **services/** → Lógica de negocio
* **ui/** → Interfaz gráfica (Construida con PySide6)
* **database/** → Conexión y gestión de base de datos
* **utils/** → Funciones auxiliares y API móvil

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
│── api_celular.py
│── inventario.db
│── main.py
│── README.md
```

---

## 🔐 Funcionalidades principales

* 🔑 Sistema de autenticación encriptado (login de usuarios)
* 📦 Gestión de productos con **búsqueda y filtros dinámicos**
* 👥 Gestión concurrente de usuarios, clientes, proveedores e instaladores
* 💰 Registro de ventas y control de roles (Administrador vs Vendedor)
* 📊 Historial completo de ventas con opción a anulación
* 📱 **API REST Interna** (Flask + Waitress) para consultas desde el celular en red local.
* 🗄️ Base de datos local (SQLite) y **Exportación a Excel**.

---

## ⚙️ Tecnologías utilizadas

* **Python 3.13**
* **PySide6 (Qt)**
* **Flask y Waitress (Backend móvil)**
* **SQLite**
* **Arquitectura modular (MVC adaptado)**
* **Git & GitHub**

---

## 🗄️ Base de datos

El sistema utiliza **SQLite local**, lo que significa:

* No requiere servidor externo
* Funciona directamente en el equipo sin depender de internet
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

El proyecto está diseñado para compilarse en una versión ejecutable instaladora (`.exe`) lista para producción a clientes y negocios. 

Debido a que el instalador final es comercial, dicho archivo (como `Instalar_InventarioJC.exe` o `Sistema_de_Inventario.exe`) se distribuye de manera estrictamente privada y no se encuentra publicado en este repositorio.

---

## 👨‍💻 Autor

**José Manuel Correa**
Desarrollador enfocado en frontend y desarrollo de software asistido con IA.
