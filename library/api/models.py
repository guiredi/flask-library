from library import db
from sqlalchemy.orm import relationship



class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return self.name

assoc_author_book = db.Table('author_book', db.Model.metadata,
                                      db.Column('id', db.Integer, primary_key=True),
                                      db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
                                      db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.String(250), nullable=False)
    author = relationship('Author', secondary=assoc_author_book, backref='book')


    def __repr__(self):
        return self.name
