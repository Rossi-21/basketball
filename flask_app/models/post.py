from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.user import User
from flask_app.models.comment import Comment

db = "sports_schema"

class Post:  
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.image_path = data['image_path']
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
        query = "INSERT INTO posts(content,image_path, created_at, updated_at, user_id) VALUES(%(content)s,%(image_path)s,NOW(),NOW(),%(user_id)s);"
        result = connectToMySQL('sports_schema').query_db(query,data)
        return result
    
    @classmethod
    def get_posts_by_user_id(cls, user_id):
        query = """
            SELECT posts.*, users.first_name AS creator_first_name, users.last_name AS creator_last_name
            FROM posts
            JOIN users ON posts.user_id = users.id
            WHERE posts.user_id = %(user_id)s ORDER BY posts.created_at DESC;
        """

        data = {"user_id": user_id}
        results = connectToMySQL('sports_schema').query_db(query, data)
        posts = []

        for result in results:
            post = cls(result)
            post.creator = User({
                "id": result['user_id'],
                "first_name": result['creator_first_name'],
                "last_name": result['creator_last_name'],
                "email": "",
                "password": "",
                "created_at": result['created_at'],
                "updated_at": result['updated_at']
            })


            post.comments = Comment.get_comments_by_post_id(post.id)

            posts.append(post)
            for post in posts:
                post.comments = Comment.get_comments_by_post_id(post.id)
                print("Post Creator:", post.creator.first_name, post.creator.last_name)
                for comment in post.comments:
                    print("Comment User:", comment.user.first_name, comment.user.last_name)

        return posts

    @classmethod
    def get_post_by_id(cls,data):
        query = "SELECT * FROM posts JOIN users On posts.user_id = users.id WHERE posts.id = %(id)s;"
        results = connectToMySQL('sports_schema').query_db(query,data)
        get_post_by_id = cls(results[0])
        u= {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name':  results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }
        get_post_by_id.user = User(u)
        return get_post_by_id

    @classmethod
    def get_one_post(cls, data):
        query = "SELECT posts.*, users.first_name, users.last_name FROM posts JOIN users ON posts.user_id = users.id WHERE posts.id = %(id)s;"
        results = connectToMySQL('sports_schema').query_db(query, data)
        
        if results:
            post_data = results[0]
            post = cls(post_data)
            post.creator = User({
                "id": post_data['user_id'],
                "first_name": post_data['first_name'],
                "last_name": post_data['last_name'],
                "email": "",
                "password": "",
                "created_at": post_data['created_at'],
                "updated_at": post_data['updated_at']
            })
            return post
        
        return None
    
    @classmethod
    def update_post(cls,data):
        query = "UPDATE posts SET content=%(content)s, updated_at=NOW() WHERE id = %(id)s;"
        result = connectToMySQL('sports_schema').query_db(query,data)
        return result
    
    @classmethod
    def delete_post(cls,data):
        query  = "DELETE FROM posts WHERE id = %(id)s;"
        result = connectToMySQL('sports_schema').query_db(query,data)
        return result

    @staticmethod
    def validate_new_post(data):
        is_valid = True
        if len(data['content']) < 2:
            is_valid = False
            flash("Content must be more than 2 characters.")
        return is_valid