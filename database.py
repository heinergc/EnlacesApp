"""
Configuración y utilidades de base de datos.
"""
from models import db, Categoria, Enlace


def init_db(app):
    """
    Inicializa la base de datos con el contexto de la aplicación.

    Args:
        app: Instancia de la aplicación Flask
    """
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✅ Base de datos inicializada correctamente")

        # Agregar datos de ejemplo si la base de datos está vacía
        if Categoria.query.count() == 0:
            agregar_datos_ejemplo()
            print("✅ Datos de ejemplo agregados")


def agregar_datos_ejemplo():
    """Agrega categorías y enlaces de ejemplo a la base de datos."""
    try:
        # Crear categorías de ejemplo
        categorias = [
            Categoria(nombre='Desarrollo'),
            Categoria(nombre='Noticias'),
            Categoria(nombre='Diseño'),
            Categoria(nombre='Educación'),
            Categoria(nombre='Entretenimiento')
        ]

        for cat in categorias:
            db.session.add(cat)

        db.session.commit()

        # Crear enlaces de ejemplo
        enlaces_ejemplo = [
            # Desarrollo
            Enlace(titulo='GitHub', url='https://github.com', categoria_id=1),
            Enlace(titulo='Stack Overflow', url='https://stackoverflow.com', categoria_id=1),
            Enlace(titulo='MDN Web Docs', url='https://developer.mozilla.org', categoria_id=1),
            Enlace(titulo='Python Documentation', url='https://docs.python.org', categoria_id=1),

            # Noticias
            Enlace(titulo='BBC News', url='https://www.bbc.com/news', categoria_id=2),
            Enlace(titulo='TechCrunch', url='https://techcrunch.com', categoria_id=2),
            Enlace(titulo='The Verge', url='https://www.theverge.com', categoria_id=2),

            # Diseño
            Enlace(titulo='Dribbble', url='https://dribbble.com', categoria_id=3),
            Enlace(titulo='Behance', url='https://www.behance.net', categoria_id=3),
            Enlace(titulo='Awwwards', url='https://www.awwwards.com', categoria_id=3),

            # Educación
            Enlace(titulo='Coursera', url='https://www.coursera.org', categoria_id=4),
            Enlace(titulo='Khan Academy', url='https://www.khanacademy.org', categoria_id=4),
            Enlace(titulo='edX', url='https://www.edx.org', categoria_id=4),

            # Entretenimiento
            Enlace(titulo='YouTube', url='https://www.youtube.com', categoria_id=5),
            Enlace(titulo='Netflix', url='https://www.netflix.com', categoria_id=5),
            Enlace(titulo='Spotify', url='https://www.spotify.com', categoria_id=5)
        ]

        for enlace in enlaces_ejemplo:
            db.session.add(enlace)

        db.session.commit()
        print("✅ Datos de ejemplo creados exitosamente")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al agregar datos de ejemplo: {str(e)}")
