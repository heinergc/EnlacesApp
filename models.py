"""
Modelos de base de datos para la aplicación de gestión de enlaces.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Categoria(db.Model):
    """Modelo para las categorías de enlaces."""
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con enlaces (cascade delete para eliminar enlaces al borrar categoría)
    enlaces = db.relationship('Enlace', backref='categoria', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convierte el objeto a diccionario para JSON."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'cantidad_enlaces': len(self.enlaces)
        }

    def __repr__(self):
        return f'<Categoria {self.nombre}>'


class Enlace(db.Model):
    """Modelo para los enlaces web."""
    __tablename__ = 'enlaces'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convierte el objeto a diccionario para JSON."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'url': self.url,
            'categoria_id': self.categoria_id,
            'categoria_nombre': self.categoria.nombre if self.categoria else None,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

    def __repr__(self):
        return f'<Enlace {self.titulo}>'
