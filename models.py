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
    icono = db.Column(db.String(50), default='📁')  # Emoji o clase de ícono
    color = db.Column(db.String(7), default='#667eea')  # Color en hexadecimal
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con enlaces (cascade delete para eliminar enlaces al borrar categoría)
    enlaces = db.relationship('Enlace', backref='categoria', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convierte el objeto a diccionario para JSON."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'icono': self.icono,
            'color': self.color,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'cantidad_enlaces': len(self.enlaces),
            'enlaces_favoritos': len([e for e in self.enlaces if e.favorito])
        }

    def __repr__(self):
        return f'<Categoria {self.nombre}>'


class Enlace(db.Model):
    """Modelo para los enlaces web."""
    __tablename__ = 'enlaces'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    descripcion = db.Column(db.Text, default='')  # Notas o descripción del enlace
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    favorito = db.Column(db.Boolean, default=False)  # Marcar como favorito
    clicks = db.Column(db.Integer, default=0)  # Contador de clicks
    tags = db.Column(db.String(200), default='')  # Etiquetas separadas por comas
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_ultimo_acceso = db.Column(db.DateTime)  # Última vez que se accedió

    def to_dict(self):
        """Convierte el objeto a diccionario para JSON."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'url': self.url,
            'descripcion': self.descripcion,
            'categoria_id': self.categoria_id,
            'categoria_nombre': self.categoria.nombre if self.categoria else None,
            'categoria_icono': self.categoria.icono if self.categoria else '📁',
            'categoria_color': self.categoria.color if self.categoria else '#667eea',
            'favorito': self.favorito,
            'clicks': self.clicks,
            'tags': self.tags.split(',') if self.tags else [],
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_ultimo_acceso': self.fecha_ultimo_acceso.isoformat() if self.fecha_ultimo_acceso else None
        }

    def __repr__(self):
        return f'<Enlace {self.titulo}>'
