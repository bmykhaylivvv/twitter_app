from flask import Flask, redirect, url_for, render_template, request
import folium
import back_end

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST", "GET"])
def gen_map():
    if request.method == "POST":
        nickname = str(request.form["nickname"])
        access_token = str(request.form["bearer_token"])
        markers = back_end.main(nickname, access_token)
        friends_map = folium.Map(location = (51, 0), zoom_start=3, tiles="cartodbdark_matter")

        friends = folium.FeatureGroup(name="friends")

        for usr in markers:
            name = usr[0]
            coordinates = usr[1]

            friends.add_child(folium.Marker(location=coordinates,
                                            popup=f"Name: {name}",
                                            icon=folium.Icon(color='lightgray')))
        friends_map.add_child(friends)

        return friends_map._repr_html_()


if __name__ == "__main__":
    app.run(debug=True)

