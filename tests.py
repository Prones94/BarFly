from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_newbar_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_bar_info = {
    'name': 'London',
    'location': '1836 Maryal Drive Sacramento CA 947281',
    'rating': 4.5,
    'alias': 'bar',
    'img_url':'https://i.imgur.com/8Ov8StI.jpg'
}
sample_form_data = {
    'name': sample_bar_info['bar'],
    'location': sample_bar_info['location'],
    'rating': sample_bar_info['rating'],
    'alias': sample_bar_info['alias'],
    'img_url': sample_bar_info['img_url']
}

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
    
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_bar(self, mock_find):
        """Tests who function"""
        mock_find.return_value = sample_bar_info

        result = self.client.get(f'/bars/{sample_newbar_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'London', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_playlist(self, mock_find):
        """Tests edit bar information"""
        mock_find.return_value = sample_bar_info

        result = self.client.get(f'/bars/{sample_newbar_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'London', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_playlist(self, mock_insert):
        """Test submitting a new playlist."""
        result = self.client.post('/bars', data=sample_form_data)

        # After submitting, should redirect to that playlist's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_bar_info)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_playlist(self, mock_update):
        result = self.client.post(f'/bars/{sample_newbar_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_newbar_id}, {'$set': sample_bar_info})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_playlist(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/bars/{sample_newbar_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_newbar_id})

    


