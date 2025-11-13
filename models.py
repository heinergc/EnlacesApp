"""
Modelos de base de datos para la aplicación de gestión de enlaces.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class Usuario(UserMixin, db.Model):
    """Modelo para los usuarios (autenticación con Google)."""
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    nombre = db.Column(db.String(200))
    foto_perfil = db.Column(db.String(500))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acceso = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    categorias = db.relationship('Categoria', backref='usuario', lazy=True, cascade='all, delete-orphan')
    enlaces = db.relationship('Enlace', backref='usuario', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convierte el objeto a diccionario para JSON."""
        return {
            'id': self.id,
            'email': self.email,
            'nombre': self.nombre,
            'foto_perfil': self.foto_perfil,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

    def __repr__(self):
        return f'<Usuario {self.email}>'


class Categoria(db.Model):
    """Modelo para las categorías de enlaces."""
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con enlaces (cascade delete para eliminar enlaces al borrar categoría)
    enlaces = db.relationship('Enlace', backref='categoria', lazy=True, cascade='all, delete-orphan')

    # Índice único para evitar categorías duplicadas por usuario
    __table_args__ = (db.UniqueConstraint('nombre', 'usuario_id', name='_nombre_usuario_uc'),)

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
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
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
