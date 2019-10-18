from flask import Flask,render_template,request,redirect, url_for
from pymongo import MongoClient
# import requests, json, os
import os
# from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient()
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

@app.route('/bars/<newbar_id>')
def single_bar(newbar_id):
    '''Single bar information(R of CRUD)'''
    one_bar = bars.find_one({'_id': ObjectId(newbar_id)})
    return render_template('bar_show.html', one_bar=one_bar)

@app.route('/bars', methods=['POST'])
def bar_form():
    '''Form to submit new bar information(C of CRUD)'''
    new_bar = {
        'name':request.form.get('name'),
        'location':request.form.get('location'),
        'rating':request.form.get('rating'),
        'alias':request.form.get('alias'),
        'img_url':request.form.get('img_url')
    }
    newbar_id = bars.insert_one(new_bar).inserted_id
    return redirect(url_for('single_bar', newbar_id=newbar_id))

@app.route('/bars/<newbar_id>/edit')
def edit_bar(newbar_id):
    '''displays edit form for update_bar function(U of CRUD)'''
    one_bar = bars.find_one({'_id': ObjectId(newbar_id)})
    return render_template('bar_show.html', one_bar=one_bar)

@app.route('/bars/<newbar_id>', methods=['POST'])
def update_bar(newbar_id):
    '''Submits edited version of bar information(U of CRUD)'''
    updated_bar= {
        'name':request.form.get('name'),
        'location':request.form.get('location'),
        'rating':request.form.get('rating'),
        'alias':request.form.get('alias'),
        'img_url':request.form.get('img_url')
    }
    bars.update_one(
        {'_id':ObjectId(newbar_id)},
        {'$set':updated_bar})
    return redirect(url_for('onebar_show',newbar_id=newbar_id))

@app.route('/bars/<newbar_id>/delete', methods=['POST'])
def delete_bar(newbar_id):
    '''Deletes bar information'''
    bars.delete_one({'_id': ObjectId(newbar_id)})
    return redirect(url_for('index'))
        
if __name__ =='__main__':
    app.run(debug=True)