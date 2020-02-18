from flask import request, jsonify, Blueprint, Response
from library import app, db
from .models import Author, Book
from .serializer import AuthorSchema, BookSchema
from sqlalchemy.orm import joinedload


author_schema = AuthorSchema()
book_schema = BookSchema()



views = Blueprint('view_page',__name__)

@app.route("/")
def get():
    db.drop_all()
    db.create_all()
    author = Author(name='Chuck Paluhniuk')
    book = Book(title='Fight Club', summary='dfjkj')
    book.author.append(author)
    db.session.add(author)
    db.session.add(book)
    db.session.commit()
    return book_schema.dump(book)


@app.route("/v1/author/")
def get_authors():
    authors = Author.query.all()
    result = authors_schema.dump(authors)
    return {"authors": result}


@app.route("/v1/author/<int:pk>")
def get_author(pk):
    try:
        author = Author.query.get(pk)
    except IntegrityError:
        return {"message": "Author could not be found."}, 400
    author_result = author_schema.dump(author)

    return {"author": author_result}


@app.route("/v1/book/", methods=["GET"])
def get_books():
    books = Book.query.all()
    result = books_schema.dump(books, many=True)
    return {"books": result}


@app.route("/v1/book/<int:pk>")
def get_book(pk):
    try:
        book = Book.query.get(pk)
    except IntegrityError:
        return {"message": "Book could not be found."}, 400
    result = book_schema.dump(book)
    return {"book": result}


@app.route("/v1/author/", methods=["POST"])
def add_author():
    name = request.json['name']
    db.session.add(Author(name=name))
    db.session.commit()

    return author_schema.jsonify(new_author)


@app.route("/v1/book/", methods=["POST"])
def add_book():
    data = request.get_json()
    db.session.add(Book(title=data['title'], summary=data['summary']))
    db.session.commit()
    for authors in data['author']:
        if authors not in '':
            details = Book.query.order_by(Book.id.desc()).first()
            db.session.add(assoc_author_book(author_id=authors, book_id=details.id))
            db.session.commit()

    return Response('Book Created', 201)
