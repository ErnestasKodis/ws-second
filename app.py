from urllib import response
from flask import Flask, request, jsonify, abort, Response
import json
import requests

application = Flask(__name__)

current_id = 5

@application.route('/')
def init():
    return 'Hello'

URL = "http://web:6969/api/"

movies = [
    {"id" : 1,
    "title" : "Uncharted",
    "director" : "Ruben Fleischer",
    "rating" : 6.6,
    "release_year" : 2022,
    "genre" : "Adventure",
    "vehicles" : "1"
    },
    {"id" : 2,
    "title" : "Fight Club",
    "director" : "David Fincher",
    "rating" : 8.8,
    "release_year" :1999,
    "genre" : "Drama",
    "vehicles" : "2"
    },
    {"id" : 3,
    "title" : "The Godfather",
    "director" : "Francis Ford Coppola",
    "rating" : 9.2,
    "release_year" : 1972,
    "genre" : "Crime",
    "vehicles" : "1"
    },
    {"id" : 4,
    "title" : "The Dark Knight",
    "director" : "Christopher Nolan",
    "rating" : 9.0,
    "release_year" : 2008,
    "genre" : "Action",
    "vehicles" : "3"
    }]

@application.route('/api/movies', methods = ["GET"])  # Returns full movie list
def movieList():
    return jsonify (movies)

@application.route('/api/movies/<int:movieId>', methods = ["GET"])
def get_movie_byID(movieId):
    for movie in movies:
        if movie["id"] == movieId:
            return jsonify(movie)
    error = "Movie with ID: " + str(movieId) + " wasn't found"
    return Response(json.dumps({"Failure": error}), status=404, mimetype="application/json")

@application.route('/api/movies', methods = ["POST"])
def add_movie():
    new_movie_data = request.get_json()
    if "title" in new_movie_data and "director" in new_movie_data and "rating" in new_movie_data and "release_year" in new_movie_data:
        global current_id
        new_movie ={
            "id" : current_id,
            "title" : new_movie_data["title"],
            "director" : new_movie_data["director"],
            "rating" : new_movie_data["rating"],
            "release_year" : new_movie_data["release_year"]
        }
        if  "genre" in new_movie_data:
            new_movie["genre"] = new_movie_data["genre"]
        else:
            new_movie["genre"] = ""
        movies.append(new_movie)
        current_id += 1
        return Response(json.dumps(new_movie), status = 201, headers={"location": "/api/movies/"+str(new_movie["id"] )}, mimetype="application/json")
    else:
        error = "Missing "
        if "title" not in new_movie_data:
            error += "title; "
        if "director" not in new_movie_data:
            error += "director; "
        if "rating" not in new_movie_data:
            error += "rating; "
        if "release_year" not in new_movie_data:
            error += "release year; "
        return Response(json.dumps({"Failure" : error}, status=400, mimetype="application/json"))

@application.route("/api/movies/<int:movieId>", methods = ["PUT"])
def put_movie(movieId):
    movie = [movie for movie in movies if movie["id"] == movieId]
    if len(movie) == 0:
        return Response(json.dumps({"Error": "Movie doesn't exist"}), status=404, mimetype="application/json")
    new_movie_data = request.get_json()
    if "title" not in new_movie_data or "director" not in new_movie_data or "rating" not in new_movie_data or "release_year" not in new_movie_data:
        error = "Missing "
        if "title" not in new_movie_data:
            error += "title; "
        if "director" not in new_movie_data:
            error += "director; "
        if "rating" not in new_movie_data:
            error += "rating; "
        if "release_year" not in new_movie_data:
            error += "release year; "
        error += ". Please specify Body"
        return Response(json.dumps({"Failure" : error}),status=400, mimetype="application/json")
    message = ""
    if "title" in new_movie_data:
        movie[0]["title"] = new_movie_data["title"]
        message += "title; "
    if "director" in new_movie_data:
        movie[0]["director"] = new_movie_data["director"]
        message += "Director; "
    if "rating" in new_movie_data:
        movie[0]["rating"] = new_movie_data["rating"]
        message  += "Rating; "
    if "release_year" in new_movie_data:
        movie[0]["release_year"] = new_movie_data["release_year"]
        message += "Release year; "
    if "genre" in new_movie_data:
        movie[0]["genre"] = new_movie_data["genre"]
        message += "genre; "
    else:
        movie[0]["genre"] = ""
    message += "have been changed"
    return Response(json.dumps(movie), status=200, mimetype="application/json")

@application.route("/api/movies/<int:movieId>", methods = ["PATCH"])
def patch_movie(movieId):
    movie = [movie for movie in movies if movie["id"] == movieId]
    if len(movie) == 0:
        return Response(json.dumps({"Error": "Movie doesn't exist"}), status=404, mimetype="application/json")
    new_movie_data = request.get_json()
    if "title" not in new_movie_data and "director" not in new_movie_data and "rating" not in new_movie_data and "release_year" not in new_movie_data and "genre" not in new_movie_data:
        error = "Wrong request body"
        return Response(json.dumps({"Failure" : error}),status=400, mimetype="application/json")
    message = ""
    if "title" in new_movie_data:
        movie[0]["title"] = new_movie_data["title"]
        message += "title; "
    if "director" in new_movie_data:
        movie[0]["director"] = new_movie_data["director"]
        message += "Director; "
    if "rating" in new_movie_data:
        movie[0]["rating"] = new_movie_data["rating"]
        message  += "Rating; "
    if "release_year" in new_movie_data:
        movie[0]["release_year"] = new_movie_data["release_year"]
        message += "Release year; "
    if "genre" in new_movie_data:
        movie[0]["genre"] = new_movie_data["genre"]
        message += "genre; "
    message += "have been changed"
    return Response(json.dumps(movie), status=200, mimetype="application/json")

@application.route("/api/movies/<int:movieId>", methods = ["DELETE"])
def delete_movie(movieId):
    for movie in movies:
        if movie["id"] == movieId:
            movies.remove(movie)
            return Response(response=(json.dumps({"Success" : "Deleted"})), status=204, mimetype="application/json")
    error = "Movie with ID: " + str(movieId) + " wasn't found"
    return Response(json.dumps({"Failure": error}), status=404, mimetype="application/json")

@application.route("/api/vehicles", methods = ["GET"])
def GetVehicle():
    try:
        req = requests.get(URL + "vehicles")
    except requests.exceptions.RequestException as e:
        return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
    return jsonify(req.json())

@application.route("/api/vehicles", methods = ["Post"])
def PostVehicle():
    body = request.get_json()
    try:
        post = requests.post(URL + "vehicles", json=body)
    except requests.exceptions.RequestException as e:
        return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
    return post.text

@application.route('/api/extendedMovies', methods = ["GET"])
def test2():
    temp_movies = []
    for movie in movies:
        temp = movie.copy()
        try:
            req = requests.get(URL + "vehicles/" + str(temp["vehicles"]))
            temp["vehicles"] = (req.json())
        except requests.exceptions.RequestException as e:
            return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
        temp_movies.append(temp)
    return jsonify(temp_movies)

@application.route('/api/extendedMovies/<int:movieId>', methods = ["GET"])
def GetMovieVechicleById(movieId):
    for movie in movies:
        if movie["id"] == movieId:
            temp_movie = movie.copy()
            try:
                req = requests.get(URL + "vehicles/" + str(movie["vehicles"]))
            except requests.exceptions.RequestException as e:
                return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
            temp_movie["vehicles"] = (req.json())
            return jsonify(temp_movie)
                
    error = "Movie with ID: " + str(movieId) + " wasn't found"
    return Response(json.dumps({"Failure": error}), status=404, mimetype="application/json")

@application.route('/api/extendedMovies/<int:movieId>/vehicles', methods = ["GET"])
def GetMovieVechicle(movieId):
    for movie in movies:
        if movie["id"] == movieId:
            try:
                req = requests.get(URL + "vehicles/" + str(movie["vehicles"]))
            except requests.exceptions.RequestException as e:
                return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
            return jsonify(req.json())
                
    error = "Movie with ID: " + str(movieId) + " wasn't found"
    return Response(json.dumps({"Failure": error}), status=404, mimetype="application/json")


@application.route('/api/extendedMovies', methods = ["POST"])
def PostFullMovieWithVehicle():
    body = request.get_json()
    try:
        post = requests.post(URL + "vehicles", json=body["vehicles"])
    except requests.exceptions.RequestException as e:
        return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
    if "title" in body and "director" in body and "rating" in body and "release_year" in body and "vehicles" in body:
        global current_id
        new_movie ={
            "id" : current_id,
            "title" : body["title"],
            "director" : body["director"],
            "rating" : body["rating"],
            "release_year" : body["release_year"],
            "vehicles" : post.json().get("id")
        }
        if  "genre" in body:
            new_movie["genre"] = body["genre"]
        else:
            new_movie["genre"] = ""
        movies.append(new_movie)
        current_id += 1
        return Response(json.dumps(new_movie), status = 201, headers={"location": "/api/movies/"+str(new_movie["id"] )}, mimetype="application/json")
    else:
        error = "Missing "
        if "title" not in body:
            error += "title; "
        if "director" not in body:
            error += "director; "
        if "rating" not in body:
            error += "rating; "
        if "release_year" not in body:
            error += "release year; "
        if "vehicles" not in body:
            error += "vehicle; "
        return Response(json.dumps({"Failure" : error}), status=400, mimetype="application/json")

@application.route('/api/extendedMovies/<int:movieId>', methods = ["PUT"])
def PutFullMovieWithVehicle(movieId):
    movie = [movie for movie in movies if movie["id"] == movieId]
    if len(movie) == 0:
        return Response(json.dumps({"Error": "Movie doesn't exist"}), status=404, mimetype="application/json")
    new_movie_data = request.get_json()
    if "title" not in new_movie_data or "director" not in new_movie_data or "rating" not in new_movie_data or "release_year" not in new_movie_data or "vehicles" not in new_movie_data:
        error = "Missing "
        if "title" not in new_movie_data:
            error += "title; "
        if "director" not in new_movie_data:
            error += "director; "
        if "rating" not in new_movie_data:
            error += "rating; "
        if "release_year" not in new_movie_data:
            error += "release year; "
        if "vehicles" not in new_movie_data:
            error += "vehicle; "
        error += ". Please specify Body"
        return Response(json.dumps({"Failure" : error}),status=400, mimetype="application/json")
    message = ""
    if "title" in new_movie_data:
        movie[0]["title"] = new_movie_data["title"]
        message += "title; "
    if "director" in new_movie_data:
        movie[0]["director"] = new_movie_data["director"]
        message += "Director; "
    if "rating" in new_movie_data:
        movie[0]["rating"] = new_movie_data["rating"]
        message  += "Rating; "
    if "release_year" in new_movie_data:
        movie[0]["release_year"] = new_movie_data["release_year"]
        message += "Release year; "
    if "genre" in new_movie_data:
        movie[0]["genre"] = new_movie_data["genre"]
        message += "genre; "
    else:
        movie[0]["genre"] = ""
    if "vehicles" in new_movie_data:
        try:
            requests.put(URL + "vehicles/" + str(movie[0]["vehicles"]), json = new_movie_data["vehicles"])
        except requests.exceptions.RequestException as e:
            return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
        message += "Vehicle "
    message += "have been changed"
    return Response(json.dumps(movie), status=200, mimetype="application/json")

@application.route('/api/extendedMovies/<int:movieId>', methods = ["PATCH"])
def PatchFullMovieWithVehicle(movieId):
    movie = [movie for movie in movies if movie["id"] == movieId]
    if len(movie) == 0:
        return Response(json.dumps({"Error": "Movie doesn't exist"}), status=404, mimetype="application/json")
    new_movie_data = request.get_json()
    if "title" not in new_movie_data and "director" not in new_movie_data and "rating" not in new_movie_data and "release_year" not in new_movie_data and "genre" not in new_movie_data and "vehicles" not in new_movie_data:
        error = "Wrong request body"
        return Response(json.dumps({"Failure" : error}),status=400, mimetype="application/json")
    message = ""
    if "title" in new_movie_data:
        movie[0]["title"] = new_movie_data["title"]
        message += "title; "
    if "director" in new_movie_data:
        movie[0]["director"] = new_movie_data["director"]
        message += "Director; "
    if "rating" in new_movie_data:
        movie[0]["rating"] = new_movie_data["rating"]
        message  += "Rating; "
    if "release_year" in new_movie_data:
        movie[0]["release_year"] = new_movie_data["release_year"]
        message += "Release year; "
    if "genre" in new_movie_data:
        movie[0]["genre"] = new_movie_data["genre"]
        message += "genre; "
    if "vehicles" in new_movie_data:
        try:
            requests.patch(URL + "vehicles/" + str(movie[0]["vehicles"]), json = new_movie_data["vehicles"])
        except requests.exceptions.RequestException as e:
            return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
        message += "Vehicle "
    message += "have been changed"
    return Response(json.dumps(movie), status=200, mimetype="application/json")

@application.route("/api/extendedMovies/<int:movieId>", methods = ["DELETE"])
def DeleteFullMovie(movieId):
    for movie in movies:
        if movie["id"] == movieId:
            movies.remove(movie)
            return Response(response=(json.dumps({"Success" : "Deleted"})), status=204, mimetype="application/json")
    error = "Movie with ID: " + str(movieId) + " wasn't found"
    return Response(json.dumps({"Failure": error}), status=404, mimetype="application/json")
    

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=True)