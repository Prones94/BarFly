from flask import Flask,render_template,request,redirect, url_for
from pymongo import MongoClient
# import requests, json, os
import os
# from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Bars')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.Bars
bars = db.Bar


@app.route('/')
def index():
    '''HomePage'''
    return render_template('homepage.html')

@app.route('/barlist')
def bar_index():
    '''Shows list of all bars'''
    return render_template('barlist.html', bars=bars.find())

@app.route('/bars/new')
def newbar():
    '''Provde a new bar information(C of CRUD)'''
    return render_template('bar_form.html', bar= {}, title = "New Bar")

@app.route('/bars', methods=['POST'])
def bar_form():
    '''Form to submit new bar information(C of CRUD)'''
    bar = {
        'name':request.form.get('name'),
        'location':request.form.get('location'),
        'rating':request.form.get('rating'),
        'alias':request.form.get('alias'),
        'img_url':request.form.get('img_url')
    }
    newbar_id = bars.insert_one(bar).inserted_id
    return redirect(url_for('single_bar', newbar_id=newbar_id))
    
@app.route('/bars/<newbar_id>')
def single_bar(newbar_id):
    '''Single bar information(R of CRUD)'''
    bar = bars.find_one({'_id': ObjectId(newbar_id)})
    return render_template('bar_show.html', bars=bar)


@app.route('/bars/<newbar_id>/edit')
def edit_bar(newbar_id):
    '''displays edit form for update_bar function(U of CRUD)'''
    bar = bars.find_one({'_id': ObjectId(newbar_id)})
    return render_template('edit_bar.html', bars=bar, title = 'Edit Bar')

@app.route('/bars/<newbar_id>', methods=['POST'])
def update_bar(newbar_id):
    '''Submits edited version of bar information(U of CRUD)'''
    new_bar= {
        'name':request.form.get('name'),
        'location':request.form.get('location'),
        'rating':request.form.get('rating'),
        'alias':request.form.get('alias'),
        'img_url':request.form.get('img_url')
    }
    bars.update_one(
        {'_id':ObjectId(newbar_id)},
        {'$set':new_bar})
    return redirect(url_for('single_bar',newbar_id=newbar_id))

@app.route('/bars/<newbar_id>/delete', methods=['POST'])
def delete_bar(newbar_id):
    '''Deletes bar information(D of CRUD)'''
    bars.delete_one({'_id': ObjectId(newbar_id)})
    return redirect(url_for('index'))
        
if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))