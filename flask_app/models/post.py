from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.user import User
from flask_app.models.comment import Comment

class Post:
    db = "sports_schema"
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data.get('updated_at', '')
        self.user_id = data.get('user_id', '')
        self.comments = []
        self.creator = None
    
    @classmethod
    def get_all_posts(cls):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC;"
        results = connectToMySQL('sports_schema').query_db(query)
        posts = []
        for row in results:
            this_post = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                'password' : row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_post.creator = User(user_data)

            comment_query = "SELECT * FROM comments JOIN users ON comments.user_id = users.id WHERE post_id = %(post_id)s;"
            comment_data = {'post_id': this_post.id}
            comment_results = connectToMySQL('sports_schema').query_db(comment_query, comment_data)

            for comment_row in comment_results:
                comment_data = {
                    'content': comment_row['content'],
                    'created_at': comment_row['created_at'],
                    'updated_at': comment_row['updated_at'],
                    'user_id': comment_row['user_id'],
                    'post_id': comment_row['post_id']
                }
                user_data = {
                    'id': comment_row['id'],
                    'first_name': comment_row['first_name'],
                    'last_name': comment_row['last_name'],
                    'email': comment_row['email'],
                    'password' : comment_row['password'],
                    'created_at': comment_row['created_at'],
                    'updated_at': comment_row['updated_at']
                }
                comment = Comment(comment_data)
                comment.user = User(user_data)
                this_post.comments.append(comment)

            posts.append(this_post)
        return posts

    @classmethod
    def save_post(cls, data):
        query = "INSERT INTO posts(content, created_at, updated_at, user_id) VALUES(%(content)s,NOW(),NOW(),%(user_id)s);"
        result = connectToMySQL('sports_schema').query_db(query,data)
        return result

    @staticmethod
    def validate_new_post(data):
        is_valid = True
        if len(data['content']) < 2:
            flash("Content must be more than 2 characters.")
            is_valid = False
        return is_valid