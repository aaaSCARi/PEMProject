import requests

def get_data(lat, lon):
  try:  
    k = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?locations="+ str(lat) + "%2C%20" + str(lon) + "&aggregateHours=24&unitGroup=us&shortColumnNames=false&contentType=json&key=39Y3ZFXCHXNS6AVM72F8UDSPP"
    x = requests.get(k).json()['locations']
    for i in x:
        y = x[i]['values']

    final = [0, 0, 0, 0, 0, 0]

    for j in y:
        final[0] += j['temp']
        if j['maxt'] > final[1]:
            final[1] = j['maxt']
        final[2] += j['wspd']
        final[3] += j['cloudcover']
        final[4] += j['precip']
        final[5] += j['humidity']
    final[0] /= len(y)
    final[2] /= len(y)
    final[3] /= len(y)
    final[5] /= len(y)
  except Exception as e:
        print("An error occurred: Wasn't able to retrieve ", str(e))
  return final
