from flask import Flask, request, render_template_string, redirect, url_for, flash, session
from services.auth_service import AuthService
from services.producto_service import producto_service
from services.usuario_service import usuario_service
from services.venta_service import venta_service
from services.persona_service import persona_service

app = Flask(__name__)
app.secret_key = "super_secret_inventario_key"

HTML_BASE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventario Móvil</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 15px; background: #f0f2f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #2c3e50; }
        .nav { background: #3498db; padding: 10px; border-radius: 8px; margin-bottom: 20px; display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
        .nav a { color: white; text-decoration: none; font-weight: bold; background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 5px; font-size: 14px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 14px; color: #555; }
        input[type="text"], input[type="password"], input[type="number"], select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
        button { width: 100%; padding: 14px; background-color: #2ecc71; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .alert { padding: 12px; background-color: #d4edda; color: #155724; border-radius: 6px; margin-bottom: 15px; text-align: center; font-weight: bold; }
        .alert-error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body><div class="container">
    {% if session.get('user_id') %}
    <div class="nav">
        <a href="{{ url_for('index') }}">Inicio</a>
        <a href="{{ url_for('nueva_venta') }}">Vender</a>
        <a href="{{ url_for('nuevo_producto') }}">Productos</a>
        <a href="{{ url_for('nueva_persona') }}">Clientes</a>
        {% if session.get('rol') == 'admin' %}<a href="{{ url_for('nuevo_usuario') }}">Usuarios</a>{% endif %}
        <a href="{{ url_for('logout') }}" style="background:#e74c3c;">Salir</a>
    </div>
    {% endif %}
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}{% for cat, msg in messages %}
        <div class="alert {% if cat == 'error' %}alert-error{% endif %}">{{ msg }}</div>
      {% endfor %}{% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
</div></body></html>
"""

def page(content):
    return HTML_BASE.replace("{% block content %}{% endblock %}", content)

LOGIN_PAGE = page("""
<h2>Acceso Móvil</h2>
<form method="POST">
    <div class="form-group"><label>Usuario:</label><input type="text" name="username" required></div>
    <div class="form-group"><label>Contraseña:</label><input type="password" name="password" required></div>
    <button type="submit">Iniciar Sesión</button>
</form>""")

INDEX_PAGE = page("<h2>Dashboard</h2><p style='text-align:center'>Bienvenido(a), <strong>{{ session['nombre'] }}</strong></p><p style='color:#666'>Usa el menú superior para navegar.</p>")

PRODUCTO_PAGE = page("""
<h2>📦 Nuevo Producto</h2>
<form method="POST">
    <div class="form-group"><label>Nombre:</label><input type="text" name="nombre" required></div>
    <div class="form-group"><label>Precio Cliente ($):</label><input type="number" step="0.01" name="precio_cliente" required></div>
    <div class="form-group"><label>Precio Proveedor ($):</label><input type="number" step="0.01" name="precio_proveedor" required></div>
    <div class="form-group"><label>Precio Instalador ($):</label><input type="number" step="0.01" name="precio_instalador" required></div>
    <div class="form-group"><label>Stock Inicial:</label><input type="number" name="stock" required></div>
    <button type="submit">Guardar</button>
</form>""")

PERSONA_PAGE = page("""
<h2>👥 Nueva Persona</h2>
<form method="POST">
    <div class="form-group"><label>Cédula:</label><input type="text" name="cedula" required></div>
    <div class="form-group"><label>Nombre Completo:</label><input type="text" name="nombre" required></div>
    <div class="form-group"><label>Tipo:</label><select name="tipo"><option value="cliente">Cliente</option><option value="proveedor">Proveedor</option><option value="instalador">Instalador</option></select></div>
    <button type="submit">Guardar</button>
</form>""")

USUARIO_PAGE = page("""
<h2>👨‍💼 Nuevo Usuario</h2>
<form method="POST">
    <div class="form-group"><label>Usuario:</label><input type="text" name="username" required></div>
    <div class="form-group"><label>Contraseña:</label><input type="password" name="password" required></div>
    <div class="form-group"><label>Nombre Real:</label><input type="text" name="nombre" required></div>
    <div class="form-group"><label>Rol:</label><select name="rol"><option value="vendedor">Vendedor</option><option value="admin">Administrador</option></select></div>
    <button type="submit">Crear</button>
</form>""")

VENTA_PAGE = page("""
<h2>🧾 Registrar Venta</h2>
<form method="POST">
    <div class="form-group"><label>Cédula del Comprador:</label><input type="text" name="cedula" required></div>
    <div class="form-group"><label>Producto:</label>
        <select name="producto_id" required>
            <option value="" disabled selected>-- Elige un producto --</option>
            {% for prod in productos %}
            <option value="{{ prod.id }}">{{ prod.nombre }} (Stock: {{ prod.stock }})</option>
            {% endfor %}
        </select>
    </div>
    <div class="form-group"><label>Cantidad:</label><input type="number" name="cantidad" value="1" min="1" required></div>
    <button type="submit" style="background:#e67e22;">Confirmar Venta</button>
</form>
<p style="font-size:12px;color:#888;text-align:center">El precio se detecta automáticamente según el tipo de persona.</p>""")

@app.before_request
def require_login():
    if request.endpoint not in ['login', 'static'] and 'user_id' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        local_auth = AuthService()
        if local_auth.login(request.form.get('username'), request.form.get('password')):
            u = local_auth.get_current_user()
            session.update({'user_id': u.id, 'username': u.username, 'nombre': u.nombre, 'rol': u.rol})
            flash(f"¡Bienvenido, {u.nombre}!", "success")
            return redirect(url_for('index'))
        flash("Credenciales incorrectas", "error")
    return render_template_string(LOGIN_PAGE)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template_string(INDEX_PAGE)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        try:
            if producto_service.create(request.form['nombre'], float(request.form['precio_cliente']),
                                       float(request.form['precio_proveedor']), float(request.form['precio_instalador']),
                                       int(request.form['stock'])):
                flash("Producto agregado exitosamente.", "success")
            else:
                flash("Error al crear el producto.", "error")
        except Exception as e:
            flash(f"Error de formato: {e}", "error")
        return redirect(url_for('nuevo_producto'))
    return render_template_string(PRODUCTO_PAGE)

@app.route('/personas/nueva', methods=['GET', 'POST'])
def nueva_persona():
    if request.method == 'POST':
        if persona_service.create(request.form['cedula'], request.form['nombre'], request.form['tipo']):
            flash("Persona registrada.", "success")
        else:
            flash("Cédula ya existe o error interno.", "error")
        return redirect(url_for('nueva_persona'))
    return render_template_string(PERSONA_PAGE)

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    if session.get('rol') != 'admin':
        flash("Acceso denegado.", "error")
        return redirect(url_for('index'))
    if request.method == 'POST':
        if usuario_service.create(request.form['username'], request.form['password'], request.form['nombre'], request.form['rol']):
            flash(f"Usuario creado con éxito.", "success")
        else:
            flash("Error: usuario duplicado o datos inválidos.", "error")
        return redirect(url_for('nuevo_usuario'))
    return render_template_string(USUARIO_PAGE)

@app.route('/ventas/nueva', methods=['GET', 'POST'])
def nueva_venta():
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        persona = persona_service.get_by_cedula(cedula)
        if not persona:
            flash(f"No se encontró persona con cédula {cedula}.", "error")
            return redirect(url_for('nueva_venta'))
        producto_id = int(request.form.get('producto_id'))
        cantidad = int(request.form.get('cantidad'))
        producto = producto_service.get_by_id(producto_id)
        tipo = persona.tipo.lower()
        precio = producto.precio_proveedor if tipo == 'proveedor' else (producto.precio_instalador if tipo == 'instalador' else producto.precio_cliente)
        exito, msg = venta_service.registrar_venta(producto_id, session['user_id'], persona.id, cantidad, precio)
        if exito:
            flash(f"¡Venta registrada! Comprador: {persona.nombre} | Total: ${precio * cantidad:.2f}", "success")
        else:
            flash(f"Error: {msg}", "error")
        return redirect(url_for('nueva_venta'))
    productos = [p for p in producto_service.get_all() if p.stock > 0]
    return render_template_string(VENTA_PAGE, productos=productos)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
