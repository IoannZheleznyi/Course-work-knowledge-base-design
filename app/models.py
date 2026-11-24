
from datetime import datetime

from app.database import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    spices = db.relationship(
        "Spice",
        back_populates="category"
    )


class Spice(db.Model):
    __tablename__ = "spices"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    origin = db.Column(db.String(255))
    usage = db.Column(db.Text)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    category = db.relationship(
        "Category",
        back_populates="spices"
    )

    articles = db.relationship(
        "Article",
        back_populates="spice",
        cascade="all, delete-orphan"
    )

    images = db.relationship(
        "Image",
        back_populates="spice",
        cascade="all, delete-orphan"
    )

    videos = db.relationship(
        "Video",
        back_populates="spice",
        cascade="all, delete-orphan"
    )


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    source_name = db.Column(db.String(255))
    source_url = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    spice_id = db.Column(
        db.Integer,
        db.ForeignKey("spices.id"),
        nullable=False
    )

    spice = db.relationship(
        "Spice",
        back_populates="articles"
    )


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.Text)

    spice_id = db.Column(
        db.Integer,
        db.ForeignKey("spices.id"),
        nullable=False
    )

    spice = db.relationship(
        "Spice",
        back_populates="images"
    )


class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.Text, nullable=False)
    source_name = db.Column(db.String(255))

    spice_id = db.Column(
        db.Integer,
        db.ForeignKey("spices.id"),
        nullable=False
    )

    spice = db.relationship(
        "Spice",
        back_populates="videos"
    )
