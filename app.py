from flask import Flask,render_template,request,redirect, url_for
from pymongo import MongoClient
# import requests, json, os
import os
# from bson.json_util import dumps
# from bson.objectid import ObjectId

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
    '''Provde a new bar location'''
    return render_template('bar_form.html', bar= {}, title = "New Bar")

@app.route('/bars', methods=['POST'])
def bar_form():
    '''Form to submit new bar information'''
    new_bar = {
        'name':request.form.get('name'),
        'location':request.form.get('location'),
        'rating':request.form.get('rating'),
        'alias':request.form.get('alias'),
        'img_url':request.form.get('img_url')
    }
    newbar_id = bars.insert_one(new_bar).inserted_id
    return redirect(url_for('single_bar', newbar_id=newbar_id))

@app.route('/bars/<newbar_id>', methods=['POST'])
def update_bar(newbar_id):
    '''Submits edited version of bar information'''
    updated_bar= {
        'name':request.form.get('name'),
        'location':request.form.get('location'),
        'rating':request.form.get('rating'),
        'alias':request.form.get('alias'),
        'img_url':request.form.get('img_url')
    }
    bars.update_one(
        {'_id':ObjectID(newbar_id)},
        {'$set':updated_bar})
    return redirect(url_for('onebar_show',newbar_id=newbar_id))
    )
# @app.route('/barlist', methods = ['GET'])
# def show_beans():
#     # R of CRUD
#     bar_info = db.bars.find()
#     return render_template('barlist.html', bar_info=bar_info.find())

# @app.route('/bean/new')
# def create_list():
#     # C of CRUD
#     all_beans = db.coffee_beans.find({})
#     return render_template('newform.html',coffee_beans=all_beans)

# @app.route('/beans', methods = ['POST'])
# def submit_new():
#     #submits new information; works w/ '/beans/new'
#     bean_list = {
#         'name': request.form.get('name'),
#         'location': request.form.get('location'),
#         'smell': request.form.get('smell'),
#         'taste': request.form.get('taste')
#     }
#     coffee_beans.insert_one(bean_list)
#     return redirect(url_for('show_beans'))

# @app.route('/coffee_beans/<beans_id>')
# def show_list(coffee_id):
#     '''Shows individual bean information'''
#     onebean = coffee_beans.find_one({'_id': ObjectId(coffee_id)})
#     # return redirect(url_for('edit_info', new_bean=new_bean))
#     return render_template('show_one.html', onebean=onebean)


# @app.route('/show_bars')
# def bar_name():
#     '''Shows list of bars in area'''
#     PARAMETERS = {
#         'term': 'bar',
#         'limit': 50,
#         'radius': 3300,
#         'location': 'san Francisco',
#         'sort-by': 'distance'
#     }
#         # Make request to yelp API
#     response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
#         # convert JSON string to a dictionary
#     biz_data = response.json()
#     businesses = biz_data['businesses']

#     clean_data = []
#     for b in businesses:
#         placeholder = []
#         placeholder.append(b['name'])
#         placeholder.append(b['location']['display_address'])
#         placeholder.append(b['transactions'])
#         placeholder.append(b['categories'])
#         clean_data.append(placeholder)

#     print(clean_data)
#     print('-----------')
#     print(businesses)
#     print('*******************************************************')
#     return str(clean_data)
        
if __name__ =='__main__':
    app.run(debug=True)