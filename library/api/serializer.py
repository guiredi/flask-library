from library import db, ma
from .models import Author, Book
from marshmallow import Schema, fields, ValidationError, pre_load


# class AuthorSchema(ma.ModelSchema):
#     class Meta:
#         model = Author
#
#
# class BookSchema(ma.ModelSchema):
#     author = ma.Nested(AuthorSchema, many=True)
#
#     class Meta:
#         model = Book
#


#
# class AuthorSchema(Schema):
#     # Make sure to use the 'only' or 'exclude' params
#     # to avoid infinite recursion
#     books = fields.Nested("BookSchema", many=True, exclude=("author",))
#
#     class Meta:
#         fields = ("id", "name", "books")
#
#
# class BookSchema(Schema):
#     author = fields.Nested(AuthorSchema, only=("id", "name"))
#
#     class Meta:
#         fields = ("id", "title", "author")
#


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()



class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    summary = fields.Str()
    author = fields.Nested(AuthorSchema(), many=True, only=("id", "name"))
