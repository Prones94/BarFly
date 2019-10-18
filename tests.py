from app import app
from unittest import TestCase, main as unittest_main,mock
# from bson.objectid import ObjectId

# sample_newbar_id = ObjectId('5d55cffc4a3d4031f42827a3')
# sample_bar_info = {
#     'name': 'London',
#     'location': '1836 Maryal Drive Sacramento CA 947281',
#     'rating': 4.5,
#     'alias': 'bar',
#     'img_url':'https://i.imgur.com/8Ov8StI.jpg'
# }
# sample_form_data = {
#     'name': sample_bar_info['bar'],
#     'location': sample_bar_info['location'],
#     'rating': sample_bar_info['rating'],
#     'alias': sample_bar_info['alias'],
#     'img_url': sample_bar_info['img_url']
# }

class BarList(TestCase):
    '''Flask Testing'''
    def preWork(self):
        ''''To-do's before all testing starts'''
        self.client = app.test_client() # Flask test client
        app.config['TESTING'] = True

    def indexTest(self):
        '''Test homepage'''
        result = self.client.get('/')
        self.assertEqual(result.status,'200 OK')
        self.assertIn(b'Bars',result.data)

    def createTest(self):
        '''Test page that creates new bar data'''
        result = self.client.get('/bars/new')
        self.assertEqual(result.status,'200 OK')
        self.assertIn(b'New Bars', result.data)

