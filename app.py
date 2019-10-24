from flask import Flask, render_template, jsonify, redirect
#from flask_pymongo import PyMongo
import pymongo
import scrape_mars
import sys

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(conn)
db = client.mars
mars_collection = db.scrape_mars


@app.route('/')
def index():
    mars = mars_collection.find_one()
    return render_template("index.html", mars=mars)


@app.route('/scrape')
def scrape():
    #mars = mars_collection.scrape_mars
    mars_data = scrape_mars.scrape()
    mars_collection.replace_one(
        {},
        mars_data,
        upsert=True
    )
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)
