from flask import Flask, render_template, request
import main
from db import get_database
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        response = main.run_scraper(username, password)

        db = get_database()
        collection = db['trendingX']
        record = collection.find_one({"_id": ObjectId(response.inserted_id)})
        date = record['date']
        time = record['time']
        topics = [record['nameoftrend1'], record['nameoftrend2'], record['nameoftrend3'], record['nameoftrend4'], record['nameoftrend5']]
        ip = record['ip']

        return render_template("result.html", date=date, time=time, topics=topics, ip=ip, record=record)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
