from flask_marshmallow import Marshmallow
from models import Book, User, Borrow, Staff

ma = Marshmallow()

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book 
        load_instance = True 

book_schema = BookSchema() 
books_schema = BookSchema(many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class BorrowSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Borrow 
        load_instance = True

borrow_schema = BorrowSchema()
borrows_schema = BorrowSchema(many=True)


class StaffSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Staff
        load_instance = True

staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)
