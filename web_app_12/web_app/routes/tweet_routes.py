from flask import Blueprint, jsonify, request, render_template, flash, redirect
import random

from web_app.models import db, Tweet, User, parse_records

tweet_routes = Blueprint("tweet_routes", __name__)

@tweet_routes.route("/tweets")
def list_tweets():
    tweet_records = Tweet.query.all()
    return render_template("tweets.html", message="Here's some tweets", tweets=tweet_records)

@tweet_routes.route("/tweets/users")
def list_users():
    user_records = User.query.all()
    return render_template("tweet_users.html", message="Here's some twitter users", users=user_records)

@tweet_routes.route("/tweets/new")
def new_tweet():
    return render_template("new_tweet.html")

@tweet_routes.route("/tweets/create", methods=["POST"])
def create_tweet():
    print("FORM DATA:", dict(request.form))

    if db.session.query(User).filter_by(id = request.form["poster_id"]).count() < 1: #Testing if our User already exists
        new_user = User(id = request.form["poster_id"],name=request.form['name'])
        print("New User Added", new_user)
        db.session.add(new_user)
    new_tweet = Tweet(id = random.randint(1,100000), text=request.form["text"], poster_id=request.form["poster_id"])


    print(new_tweet)
    db.session.add(new_tweet)
    db.session.commit()

    # return jsonify({
    #    "message": "BOOK CREATED OK",
    #    "book": dict(request.form)
    # })
    # flash(f"Book '{new_book.title}' created successfully!", "success")
    return redirect("/tweets")
