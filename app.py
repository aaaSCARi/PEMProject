from flask import Flask, render_template, request
import pickle
import prediction
import csv

app = Flask(__name__)


cities = [{'name':'Delhi', "sel": "selected"}, {'name':'Mumbai', "sel": ""}, {'name':'Kolkata', "sel": ""}, {'name':'Bangalore', "sel": ""}, {'name':'Chennai', "sel": ""}, {'name':'New York', "sel": ""}, {'name':'Los Angeles', "sel": ""}, {'name':'London', "sel": ""}, {'name':'Paris', "sel": ""}, {'name':'Sydney', "sel": ""}, {'name':'Beijing', "sel": ""}]

model = pickle.load(open("model1.pickle", 'rb'))

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route('/predicts.html')
def predicts():
    return render_template('predicts.html', cities=cities, cityname="Information about the city")

@app.route('/predicts.html', methods=["GET", "POST"])
def get_predicts():
    try:
        model = pickle.load(open("model1.pickle", 'rb'))
        cityname = request.form["city"]
        print(cityname)
        csv_file_path = "training/cities.csv"
        cities_data = read_cities_csv(csv_file_path)
        latitude, longitude = get_latitude_longitude(cityname, cities_data)
        if latitude is None or longitude is None:
            return render_template('predicts.html', cities=cities, cityname="Oops, we weren't able to retrieve data for that city.")
        final = prediction.get_data(latitude, longitude)
        final[4] *= 15
      
        if str(model.predict([final])[0]) == "0":
       
            pred = "Safe"

        else:
            pred = "Unsafe"
        return render_template('predicts.html', cityname="Information about " + cityname, cities=cities, temp=round(final[0], 2), 
                               maxt=round(final[1], 2), wspd=round(final[2], 2), cloudcover=round(final[3], 2),
                                 percip=round(final[4], 2), humidity=round(final[5], 2), pred = pred)
    except:
        
        return render_template('predicts.html', cities=cities, cityname="Oops, we weren't able to retrieve data for that city.")

def read_cities_csv(file_path):
    cities_data = []
    try:
        with open(file_path, newline='',encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                city = row[0]
                latitude = float(row[1])
                longitude = float(row[2])
                cities_data.append({'city': city, 'latitude': latitude, 'longitude': longitude})
    except Exception as e:
        print("An error occurred:", str(e))
    return cities_data

def get_latitude_longitude(city_name, cities_data):
    for city_data in cities_data:
        if city_data['city'].lower() == city_name.lower():
            return city_data['latitude'], city_data['longitude']
    return None, None


if __name__ == "__main__":
    app.run()