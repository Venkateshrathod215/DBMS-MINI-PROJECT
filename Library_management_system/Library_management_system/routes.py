from flask import Flask, request, jsonify
from models import db, Book, User, Borrow, Staff
from schema import book_schema, books_schema, user_schema, users_schema, borrow_schema, borrows_schema

app = Flask(__name__)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/books', methods=['POST'])
def add_book():
    title = request.json['title']
    author = request.json['author']
    copies = request.json['copies']
    
    new_book = Book(title=title, author=author, copies=copies)
    db.session.add(new_book)
    db.session.commit()
    
    return book_schema.jsonify(new_book)

@app.route('/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    return books_schema.jsonify(all_books)

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    
    book.title = request.json.get('title', book.title)
    book.author = request.json.get('author', book.author)
    book.copies = request.json.get('copies', book.copies)
    
    db.session.commit()
    return book_schema.jsonify(book)

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"})

@app.route('/users', methods=['POST'])
def add_user():
    name = request.json.get('name')
    email = request.json.get('email')
    address = request.json.get('address')

    if not name or not email or not address:
        return jsonify({"error": "Name, email, and address are required"}), 400

    new_user = User(name=name, email=email, address=address)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    return users_schema.jsonify(all_users)

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    user.name = request.json.get('name', user.name)
    user.email = request.json.get('email', user.email)
    
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

@app.route('/borrow', methods=['POST'])
def borrow_book():
    book_id = request.json['book_id']
    user_id = request.json['user_id']
    
    book = Book.query.get(book_id)
    if not book or book.copies < 1:
        return jsonify({"message": "Book not available"}), 400
    
    new_borrow = Borrow(book_id=book_id, user_id=user_id)
    book.copies -= 1
    
    db.session.add(new_borrow)
    db.session.commit()
    return borrow_schema.jsonify(new_borrow)

@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrow = Borrow.query.get(borrow_id)
    if not borrow:
        return jsonify({"message": "Borrow record not found"}), 404
    
    book = Book.query.get(borrow.book_id)
    book.copies += 1
    
    db.session.delete(borrow)
    db.session.commit()
    return jsonify({"message": "Book returned successfully"})