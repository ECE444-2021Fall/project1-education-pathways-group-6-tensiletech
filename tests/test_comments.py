import unittest

from app import create_app, dbsql
from app.db.db_models import CourseComments

class CommentsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        dbsql.create_all()

        self.app.config['USERNAME'] = 'admin'
        self.app.config['PASSWORD'] = 'admin'

        self.client.post('/login', data = {
            'username': self.app.config['USERNAME'],
            'password': self.app.config['PASSWORD']
        })
    
    def test_response(self):
        response = self.client.get('/course/ECE444H1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('There are no comments yet.' in response.get_data(as_text=True))

        TEST_COMMENT_TEXT = 'Test comment'
        response = self.client.post('/course/ECE444H1/add_comment', data = {
            'text': TEST_COMMENT_TEXT
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(TEST_COMMENT_TEXT in response.get_data(as_text=True))

        dbsql.session.query(CourseComments).filter_by(userId=self.app.config['USERNAME']).delete()
        dbsql.session.commit()
        

if __name__ == '__main__':
    unittest.main()
