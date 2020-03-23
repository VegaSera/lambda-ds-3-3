#

from flask import Blueprint, jsonify, render_template, flash, redirect, request

book_routes = Blueprint("book_routes", __name__)

@book_routes.route("/books")
def about():
    print("Visited book page")
    books = [
        {"id": 1, "title":"Book 1"},
        {"id": 2, "title": "Book 2"},
        {"id": 3, "title": "Book 3"}
    ]
    return render_template("books.html", books=books)

@book_routes.route("/books/new")
def new_book():
    return render_template("new_books.html")

@book_routes.route("/books/create", methods=["POST"])
def create_book():
    print("FORM DATA:", dict(request.form))
    # todo: store in database
    return jsonify({
        "message": "BOOK CREATED OK (TODO)",
        "book": dict(request.form)
    })
    #flash(f"Book '{new_book.title}' created successfully!", "success")
    #return redirect(f"/books")