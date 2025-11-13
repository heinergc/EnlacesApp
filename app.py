"""
Aplicación Flask para la gestión de enlaces web con autenticación Google OAuth.
"""
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from models import db, Usuario, Categoria, Enlace
from database import init_db

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración
# Usar variable de entorno para SECRET_KEY en producción, o una por defecto en desarrollo
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu-clave-secreta-aqui-cambiala-en-produccion')

# Configurar base de datos según el entorno
if os.environ.get('RENDER'):
    # En producción (Render), usar base de datos persistente
    db_path = '/opt/render/project/data/enlaces.db'
else:
    # En desarrollo local
    db_path = 'enlaces.db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

# Configurar OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


@login_manager.user_loader
def load_user(user_id):
    """Cargar usuario para Flask-Login."""
    return Usuario.query.get(int(user_id))


# ========== RUTAS DE AUTENTICACIÓN ==========

@app.route('/login')
def login():
    """Redirigir a Google para autenticación."""
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    """Callback de Google OAuth."""
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')

        if not user_info:
            return jsonify({'success': False, 'error': 'No se pudo obtener información del usuario'}), 400

        # Buscar o crear usuario
        usuario = Usuario.query.filter_by(google_id=user_info['sub']).first()

        if not usuario:
            usuario = Usuario(
                google_id=user_info['sub'],
                email=user_info['email'],
                nombre=user_info.get('name', ''),
                foto_perfil=user_info.get('picture', '')
            )
            db.session.add(usuario)
        else:
            # Actualizar último acceso y datos
            usuario.ultimo_acceso = datetime.utcnow()
            usuario.nombre = user_info.get('name', usuario.nombre)
            usuario.foto_perfil = user_info.get('picture', usuario.foto_perfil)

        db.session.commit()
        login_user(usuario)

        return redirect(url_for('index'))

    except Exception as e:
        print(f"Error en autorización: {str(e)}")
        return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión del usuario."""
    logout_user()
    return redirect(url_for('index'))


@app.route('/api/user')
def get_current_user():
    """Obtener información del usuario actual."""
    if current_user.is_authenticated:
        return jsonify({
            'success': True,
            'user': current_user.to_dict()
        })
    return jsonify({
        'success': False,
        'user': None
    })


# ========== RUTAS DE PÁGINAS ==========

@app.route('/')
def index():
    """Página principal - Dashboard con categorías."""
    return render_template('index.html')


@app.route('/categoria/<int:categoria_id>')
def categoria_detalle(categoria_id):
    """Página de detalle de una categoría específica."""
    categoria = Categoria.query.get_or_404(categoria_id)
    return render_template('categoria.html', categoria=categoria)


# ========== API ENDPOINTS - CATEGORÍAS ==========

@app.route('/api/categorias', methods=['GET'])
@login_required
def obtener_categorias():
    """Obtiene todas las categorías del usuario autenticado."""
    try:
        categorias = Categoria.query.filter_by(usuario_id=current_user.id).order_by(Categoria.nombre).all()
        return jsonify({
            'success': True,
            'categorias': [cat.to_dict() for cat in categorias]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/categorias/<int:categoria_id>', methods=['GET'])
@login_required
def obtener_categoria(categoria_id):
    """Obtiene una categoría específica del usuario autenticado."""
    try:
        categoria = Categoria.query.filter_by(id=categoria_id, usuario_id=current_user.id).first_or_404()
        return jsonify({
            'success': True,
            'categoria': categoria.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@app.route('/api/categorias', methods=['POST'])
@login_required
def crear_categoria():
    """Crea una nueva categoría para el usuario autenticado."""
    try:
        data = request.get_json()

        if not data or not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre de la categoría es requerido'
            }), 400

        # Verificar si ya existe una categoría con ese nombre para este usuario
        if Categoria.query.filter_by(nombre=data['nombre'], usuario_id=current_user.id).first():
            return jsonify({
                'success': False,
                'error': 'Ya existe una categoría con ese nombre'
            }), 400

        nueva_categoria = Categoria(nombre=data['nombre'], usuario_id=current_user.id)
        db.session.add(nueva_categoria)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Categoría creada exitosamente',
            'categoria': nueva_categoria.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/categorias/<int:categoria_id>', methods=['PUT'])
@login_required
def actualizar_categoria(categoria_id):
    """Actualiza una categoría existente del usuario autenticado."""
    try:
        categoria = Categoria.query.filter_by(id=categoria_id, usuario_id=current_user.id).first_or_404()
        data = request.get_json()

        if not data or not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre de la categoría es requerido'
            }), 400

        # Verificar si ya existe otra categoría con ese nombre para este usuario
        categoria_existente = Categoria.query.filter_by(nombre=data['nombre'], usuario_id=current_user.id).first()
        if categoria_existente and categoria_existente.id != categoria_id:
            return jsonify({
                'success': False,
                'error': 'Ya existe una categoría con ese nombre'
            }), 400

        categoria.nombre = data['nombre']
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Categoría actualizada exitosamente',
            'categoria': categoria.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/categorias/<int:categoria_id>', methods=['DELETE'])
@login_required
def eliminar_categoria(categoria_id):
    """Elimina una categoría del usuario autenticado y todos sus enlaces asociados."""
    try:
        categoria = Categoria.query.filter_by(id=categoria_id, usuario_id=current_user.id).first_or_404()

        # SQLAlchemy manejará la eliminación en cascada de los enlaces
        db.session.delete(categoria)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Categoría "{categoria.nombre}" y sus enlaces eliminados exitosamente'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========== API ENDPOINTS - ENLACES ==========

@app.route('/api/enlaces', methods=['GET'])
@login_required
def obtener_enlaces():
    """Obtiene todos los enlaces del usuario autenticado o los de una categoría específica."""
    try:
        categoria_id = request.args.get('categoria_id', type=int)

        if categoria_id:
            enlaces = Enlace.query.filter_by(categoria_id=categoria_id, usuario_id=current_user.id).order_by(Enlace.titulo).all()
        else:
            enlaces = Enlace.query.filter_by(usuario_id=current_user.id).order_by(Enlace.titulo).all()

        return jsonify({
            'success': True,
            'enlaces': [enlace.to_dict() for enlace in enlaces]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/enlaces/<int:enlace_id>', methods=['GET'])
@login_required
def obtener_enlace(enlace_id):
    """Obtiene un enlace específico del usuario autenticado."""
    try:
        enlace = Enlace.query.filter_by(id=enlace_id, usuario_id=current_user.id).first_or_404()
        return jsonify({
            'success': True,
            'enlace': enlace.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@app.route('/api/enlaces', methods=['POST'])
@login_required
def crear_enlace():
    """Crea un nuevo enlace para el usuario autenticado."""
    try:
        data = request.get_json()

        # Validaciones
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos'
            }), 400

        if not data.get('titulo'):
            return jsonify({
                'success': False,
                'error': 'El título es requerido'
            }), 400

        if not data.get('url'):
            return jsonify({
                'success': False,
                'error': 'La URL es requerida'
            }), 400

        if not data.get('categoria_id'):
            return jsonify({
                'success': False,
                'error': 'La categoría es requerida'
            }), 400

        # Verificar que la categoría existe y pertenece al usuario
        categoria = Categoria.query.filter_by(id=data['categoria_id'], usuario_id=current_user.id).first()
        if not categoria:
            return jsonify({
                'success': False,
                'error': 'La categoría especificada no existe'
            }), 400

        # Asegurar que la URL tenga protocolo
        url = data['url']
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        nuevo_enlace = Enlace(
            titulo=data['titulo'],
            url=url,
            categoria_id=data['categoria_id'],
            usuario_id=current_user.id
        )

        db.session.add(nuevo_enlace)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Enlace creado exitosamente',
            'enlace': nuevo_enlace.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/enlaces/<int:enlace_id>', methods=['PUT'])
@login_required
def actualizar_enlace(enlace_id):
    """Actualiza un enlace existente del usuario autenticado."""
    try:
        enlace = Enlace.query.filter_by(id=enlace_id, usuario_id=current_user.id).first_or_404()
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos'
            }), 400

        # Actualizar campos si están presentes
        if 'titulo' in data:
            if not data['titulo']:
                return jsonify({
                    'success': False,
                    'error': 'El título no puede estar vacío'
                }), 400
            enlace.titulo = data['titulo']

        if 'url' in data:
            if not data['url']:
                return jsonify({
                    'success': False,
                    'error': 'La URL no puede estar vacía'
                }), 400
            url = data['url']
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            enlace.url = url

        if 'categoria_id' in data:
            categoria = Categoria.query.filter_by(id=data['categoria_id'], usuario_id=current_user.id).first()
            if not categoria:
                return jsonify({
                    'success': False,
                    'error': 'La categoría especificada no existe'
                }), 400
            enlace.categoria_id = data['categoria_id']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Enlace actualizado exitosamente',
            'enlace': enlace.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/enlaces/<int:enlace_id>', methods=['DELETE'])
@login_required
def eliminar_enlace(enlace_id):
    """Elimina un enlace del usuario autenticado."""
    try:
        enlace = Enlace.query.filter_by(id=enlace_id, usuario_id=current_user.id).first_or_404()
        titulo = enlace.titulo

        db.session.delete(enlace)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Enlace "{titulo}" eliminado exitosamente'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========== MANEJO DE ERRORES ==========

@app.errorhandler(404)
def not_found(error):
    """Maneja errores 404."""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 'Recurso no encontrado'
        }), 404
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Maneja errores 500."""
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
    return "Error interno del servidor", 500


# ========== INICIALIZACIÓN ==========

if __name__ == '__main__':
    # Inicializar la base de datos
    init_db(app)

    # Ejecutar la aplicación
    print("\n" + "=" * 60)
    print("🚀 APLICACIÓN DE GESTIÓN DE ENLACES")
    print("=" * 60)
    print("📍 Abre tu navegador en: http://localhost:5000")
    print("🛑 Presiona Ctrl+C para detener el servidor")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
