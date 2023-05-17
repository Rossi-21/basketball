from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Comment:
    def __init__(self, data):
        self.id = data.get('id')
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data.get('updated_at', '')
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.user = None


    @classmethod
    def get_comments_by_post_id(cls, post_id):
        query = """
            SELECT comments.*, users.first_name AS comment_user_first_name, users.last_name AS comment_user_last_name
            FROM comments
            JOIN users ON comments.user_id = users.id
            WHERE comments.post_id = %(post_id)s;
        """

        data = {"post_id": post_id}
        results = connectToMySQL('whats_the_issue').query_db(query, data)
        comments = []

        for result in results:
            comment = cls(result)
            comment.user = User({
                "id": result['user_id'],
                "first_name": result['comment_user_first_name'],
                "last_name": result['comment_user_last_name'],
                "email": "",
                "password": "",
                "created_at": result['created_at'],
                "updated_at": result['updated_at']
            })
            comments.append(comment)

        return comments
