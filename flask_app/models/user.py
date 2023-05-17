from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#from flask_app.models import #import other models

db = 'sports_schema'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users 
        
    @classmethod
    def get_one(cls,data):
        query = "Select * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = """SELECT * FROM users
        WHERE email = %(email)s;
        """
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return None
        return cls(result[0])

    @staticmethod
    def validate_user(request):
        is_valid = True
        if len(request['first_name']) < 1:
            is_valid = False
            flash('First Name Required', 'regError')
        elif not request['first_name'].isalpha():
            is_valid = False
            flash('First Name can only contain letters', 'regError')
        elif len(request['first_name']) < 3:
            is_valid = False
            flash('First Name must be at least 3 characters', 'regError')
        if len(request['last_name']) < 1:
            is_valid = False
            flash('Last Name Required', 'regError')
        elif len(request['last_name']) < 3:
            is_valid = False
            flash('Last Name must be at least 3 characters', 'regError')
        if len(request['email']) < 1:
            is_valid = False
            flash('Email Required', 'regError')
        elif not EMAIL_REGEX.match(request['email']):
            is_valid = False
            flash('Invalid Email', 'regError')
        if len(request['password']) < 1:
            is_valid = False
            flash('Password Required', 'regError')
        elif len(request['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters long', 'regError')
        elif not any(char.isdigit() for char in request['password']):
            is_valid = False
            flash('Password must contain at least one number', 'regError')
        elif not any(char.isupper() for char in request['password']):
            is_valid = False
            flash('Password must contain at least one uppercase letter', 'regError')
        if (request['passConf']) != (request['password']) :
            is_valid = False
            flash('Passwords do not Match', 'regError')         
        elif User.get_by_email(request):
            is_valid = False
            flash('This email is already taken', 'regError')
        return is_valid
    
    # class method that joins two tables in your DB
    # @classmethod
    # def get_authors_with_books(cls,data):
    #     query = """
    #     SELECT * FROM users
    #     LEFT JOIN favorites ON users.id = favorites.user_id
    #     LEFT JOIN books ON books.id = favorites.book_id
    #     WHERE users.id = %(id)s;
    #     """
    #     results = connectToMySQL(db).query_db(query, data)
    #     user = cls( results[0] )S
    #     for db_row in results:
    #         book_data = {
    #             "id" : db_row["books.id"],
    #             "title" : db_row["title"],
    #             "num_of_pages": db_row["num_of_pages"],
    #             "created_at" : db_row["books.created_at"],
    #             "updated_at" :db_row["books.updated_at"]
    #         }

    #         user.books.append( book.Book( book_data) )
    #     return user