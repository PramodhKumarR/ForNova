#importing necessary libraries
import pandas as pd
import requests
import json
#function to extract the required information from the JSON data
def extract_rate_information(room_type, offer):
    return {
        "Room_name": room_type.get("name"),
        "Rate_name": offer.get("name"),
        "Number_of_Guests": room_type.get("maxOccupantCount"),
        "Cancellation_Policy": offer.get("cancellationPolicy", {}).get("description"),
        "Price": offer.get("charges", {}).get("total", {}).get("amount"),
        "Top_Deal": offer.get("promotion") is not None and offer.get("promotion").get("name", "") == "Top Deal",
        "Currency": offer.get("charges", {}).get("total", {}).get("currency")
    }
#To read CSV file to the pandas dataframe
df = pd.read_csv(r'C:\pramo\Downloads\Details.csv')
#Empty list to store the extracted rates
rates = []
#Empty dictionary to store captured JSON
json_data = {}
#to iterate through the dataframe
for _, row in df.iterrows():
    hotels_id = row['hotels_id']
    check_in = row['check-in']
    check_out = row['check-out']
#URL construction which is derived from web page inspection
    url = f"https://www.qantas.com/hotels/api/ui/properties/{hotels_id}/availability?checkIn={check_in}&checkOut={check_out}&adults=2&children=0&infants=0&payWith=cash"
    print(f"Constructed URL: {url}")
#Defining headers for the get request
    headers = {'Referer': url}
    response = requests.get(url, headers=headers)
#Response code to check if the request was successful
    if response.status_code == 200:
        json_data = response.json()
#iteration over room type and offer and calling the function to extract the required data
        for room_type in json_data['roomTypes']:
            for offer in room_type.get('offers', []):
                rate = extract_rate_information(room_type, offer)
                rates.append(json.dumps(rate))
                print(json.dumps(rate, indent=4, sort_keys=True))#printing data output in JASON Format
    else:
        print(f"Error: Unable to fetch data. Status code {response.status_code}")#incase if the data extraction fails due to an error
