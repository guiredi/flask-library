from flask import request, jsonify, Blueprint, Response
from library import app, db
from .models import Author, Book
from .serializer import AuthorSchema, BookSchema
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

views = Blueprint('view_page',__name__)

@app.route("/book")
def get_book_test():
    db.drop_all()
    db.create_all()
    author = Author(name='Chuck Paluhniuk')
    author_2 = Author(name="Chuck Norris")
    book = Book(name='Fight Club', summary='summary')
    book.author.append(author)
    book.author.append(author_2)
    db.session.add(author)
    db.session.add(book)
    db.session.commit()
    return book_schema.dump(book)

@app.route("/author")
def get_author_test():
    # db.drop_all()
    # db.create_all()
    author = Author(name='Calango')
    author_2 = Author(name="Joy lele")
    book = Book(name='Salve', summary='summaro')
    book.author.append(author)
    # book.author.append(author_2)
    db.session.add(author)
    db.session.add(author)
    db.session.add(book)
    db.session.commit()
    return author_schema.dump(author)


@app.route("/v1/author/", methods=["GET", "POST"])
def get_authors_test():
    if request.method == "GET":
        try:
            authors = Author.query.all()
        except IntegrityError:
            return {"message" : "Authors could not be found"}
        result = authors_schema.dump(authors)
        return {"results": result}
    elif request.method == "POST":
        json_data =  request.json['name']
        if not json_data:
            return jsonify({"message": "No Input data provided"}), 400
        new_author = Author(name=json_data)
        db.session.add(new_author)
        db.session.commit()
        return jsonify({"message": "Created new author.", "author": author_schema.dump(new_author)})

@app.route("/v1/author/<int:pk>/", methods=["GET", "PUT", "DELETE"])
def get_author(pk):
    try:
        author = Author.query.get(pk)
    except IntegrityError:
        return jsonify({"message" : "Author could not be found."}), 400
    if request.method == "GET":
        result = author_schema.dump(author)
        return result
    elif request.method == "PUT":
        json_data = request.json['name']
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400
        author.name = json_data
        db.session.commit()
        return jsonify({"message" : "Author Update", "author": author_schema.dump(author)})
    elif request.method == "DELETE":
        db.session.delete(author)
        db.session.commit()
        return jsonify({"message" : "Author deleted", "author": author_schema.dump(author)})


@app.route("/v1/book/", methods=["GET", "POST"])
def get_books():
    if request.method == "GET":
        try:
            books = Book.query.all()
        except IntegrityError:
            return {"message" : "Authors could not be found"}
        result = books_schema.dump(books)
        return {"results" : result}
    if request.method == "POST":
        name = request.json['name']
        summary = request.json['summary']
        authors = request.json['author']
        new_book = Book(name=name, summary=summary)
        for author in authors:
            author_insert = Author.query.filter_by(name=author).first()
            new_book.author.append(author_insert)
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Created new book.", "book" : book_schema.dump(new_book)})

@app.route("/v1/book/<int:pk>/", methods=["GET", "PUT", "DELETE"])
def get_book(pk):
    try:
        book = Book.query.get(pk)
    except IntegrityError:
        return jsonify({"message" : "Book could not be found."}), 400
    if request.method == "GET":
        result = book_schema.dump(book)
        return result
    elif request.method == "PUT":
        name = request.json['name']
        summary = request.json['summary']
        authors = request.json['author']

        book.name = name
        book.summary = summary
        # NEED FIX
        book.author = authors
        db.session.commit()
        return jsonify({"message" : "Book Update", "book": book_schema.dump(book)})
    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message" : "Author deleted", "author": book_schema.dump(book)})
