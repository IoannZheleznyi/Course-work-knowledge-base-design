from datetime import datetime

from app import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    spices = db.relationship("Spice", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"


class Spice(db.Model):
    __tablename__ = "spices"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    origin = db.Column(db.String(150))
    usage = db.Column(db.Text)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    category = db.relationship("Category", back_populates="spices")

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

    def __repr__(self):
        return f"<Spice {self.name}>"


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    source_name = db.Column(db.String(150))
    source_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    spice_id = db.Column(
        db.Integer,
        db.ForeignKey("spices.id"),
        nullable=False
    )

    spice = db.relationship("Spice", back_populates="articles")


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500), nullable=False)
    source_url = db.Column(db.String(500))

    spice_id = db.Column(
        db.Integer,
        db.ForeignKey("spices.id"),
        nullable=False
    )

    spice = db.relationship("Image", back_populates="spice")


class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(500), nullable=False)
    source_name = db.Column(db.String(150))

    spice_id = db.Column(
        db.Integer,
        db.ForeignKey("spices.id"),
        nullable=False
    )

    spice = db.relationship("Video", back_populates="spice")
