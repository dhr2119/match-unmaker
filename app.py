from flask import Flask, render_template, request
import json

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app

json_data = open('phones.json').read()
data = json.loads(json_data)

@app.route("/")
def home():
	return render_template("home.html")

def filter_phones(os, size, battery_size):
	filt_phones1 = []
	for phone in data:
		if phone["OS"] == os:
			filt_phones1.append(phone)
	filt_phones2 = []
	for phone in filt_phones1:
		json_size = phone["size_in"]
		if json_size <= size and json_size > size - 0.5:
			filt_phones2.append(phone)
	filt_phones3 = []
	for phone in filt_phones2:
		battery_size = phone["battery_mAh"]
		if battery_size < size and battery_size >= size - 400:
			filt_phones3.append(phone)
	return filt_phones2

@app.route("/questionaire", methods=["GET","POST"])
def questionaire():
	if request.method == "GET":
		return render_template("questionaire.html")
	else:
		size = float(request.form['size_in'])
		os = request.form['OS']
		battery_size = int(request.form['battery_size'])
		phones = filter_phones(os, size, battery_size)
		return render_template("results.html", phones=phones)

if __name__ == "__main__":
    app.run(host="0.0.0.0")