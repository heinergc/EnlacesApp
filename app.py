"""
Aplicación Flask para la gestión de enlaces web.
"""
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from models import db, Categoria, Enlace
from database import init_db

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu-clave-secreta-aqui-cambiala-en-produccion')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///enlaces.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)


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


@app.route('/simplex')
def metodo_simplex():
    """Tutorial interactivo del Método Simplex."""
    return send_from_directory('static', 'metodo-simplex.html')


# ========== API ENDPOINTS - CATEGORÍAS ==========

@app.route('/api/categorias', methods=['GET'])
def obtener_categorias():
    """Obtiene todas las categorías con la cantidad de enlaces."""
    try:
        categorias = Categoria.query.order_by(Categoria.nombre).all()
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
def obtener_categoria(categoria_id):
    """Obtiene una categoría específica."""
    try:
        categoria = Categoria.query.get_or_404(categoria_id)
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
def crear_categoria():
    """Crea una nueva categoría."""
    try:
        data = request.get_json()

        if not data or not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre de la categoría es requerido'
            }), 400

        # Verificar si ya existe una categoría con ese nombre
        if Categoria.query.filter_by(nombre=data['nombre']).first():
            return jsonify({
                'success': False,
                'error': 'Ya existe una categoría con ese nombre'
            }), 400

        nueva_categoria = Categoria(nombre=data['nombre'])
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
def actualizar_categoria(categoria_id):
    """Actualiza una categoría existente."""
    try:
        categoria = Categoria.query.get_or_404(categoria_id)
        data = request.get_json()

        if not data or not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre de la categoría es requerido'
            }), 400

        # Verificar si ya existe otra categoría con ese nombre
        categoria_existente = Categoria.query.filter_by(nombre=data['nombre']).first()
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
def eliminar_categoria(categoria_id):
    """Elimina una categoría y todos sus enlaces asociados."""
    try:
        categoria = Categoria.query.get_or_404(categoria_id)

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
def obtener_enlaces():
    """Obtiene todos los enlaces o los de una categoría específica."""
    try:
        categoria_id = request.args.get('categoria_id', type=int)

        if categoria_id:
            enlaces = Enlace.query.filter_by(categoria_id=categoria_id).order_by(Enlace.titulo).all()
        else:
            enlaces = Enlace.query.order_by(Enlace.titulo).all()

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
def obtener_enlace(enlace_id):
    """Obtiene un enlace específico."""
    try:
        enlace = Enlace.query.get_or_404(enlace_id)
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
def crear_enlace():
    """Crea un nuevo enlace."""
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

        # Verificar que la categoría existe
        categoria = Categoria.query.get(data['categoria_id'])
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
            categoria_id=data['categoria_id']
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
def actualizar_enlace(enlace_id):
    """Actualiza un enlace existente."""
    try:
        enlace = Enlace.query.get_or_404(enlace_id)
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
            categoria = Categoria.query.get(data['categoria_id'])
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
def eliminar_enlace(enlace_id):
    """Elimina un enlace."""
    try:
        enlace = Enlace.query.get_or_404(enlace_id)
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
