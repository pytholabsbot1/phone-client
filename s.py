from flask import Flask, render_template, jsonify, request
import csv, os, requests, json

app = Flask(__name__)

data = []
current_record = 0
main_server = "https://ascentbuildhome.com"
wa_endpoint = "http://18.216.242.238:8000/warmup"


def read_data():
    global data
    res = requests.post(
        f"{main_server}/fetch_leads",
        data={"pass": "JMGHJSDGJHkjshakjha0989y87mnasVNVasdjkh"},
    )
    data = res.json()["data"]


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/get_record", methods=["GET"])
def get_record():
    global current_record
    if current_record >= len(data):
        return jsonify({"error": "No more records"})

    record = data[current_record]
    return jsonify(record)


@app.route("/next", methods=["POST"])
def next_record():
    global current_record
    if current_record >= len(data):
        return jsonify({"error": "No more records"})

    current_record += 1
    record = data[current_record]
    return jsonify(record)


@app.route("/data", methods=["POST"])
def fetch_data():
    try:
        global current_record

        read_data()

        current_record = 0
        record = data[current_record]
        print(record)
        return jsonify(record)

    except Exception as e:
        print(e)


@app.route("/prev", methods=["POST"])
def prev_record():
    global current_record
    if current_record <= 0:
        return jsonify({"error": "Already at the first record"})

    current_record -= 1
    record = data[current_record]
    return jsonify(record)


@app.route("/call", methods=["POST"])
def make_call():
    # Run code for making a call
    record = data[current_record]["mobile"]

    res = requests.post(
        f"{main_server}/mcll",
        data={"mobile": record, "pass": "JMGHJSDGJHkjshakjha0989y87mnasVNVasdjkh"},
    )
    os.system(f"termux-telephony-call {record}")
    return jsonify({"message": "Call initiated"})


@app.route("/lead", methods=["POST"])
def make_lead():
    # Run code for making a call
    record = data[current_record]["mobile"]
    os.system(
        f"termux-open-url https://ascentbuildhome.com/controlshit/projects/lead/?q={record}"
    )
    return jsonify({"message": "Lead initiated"})


@app.route("/sms", methods=["POST"])
def send_sms():
    # Run code for sending an SMS
    record = data[current_record]["mobile"]
    os.system(
        f'termux-sms-send -n {record} "Greetings from Airport Enclave Jharsuguda.\nWe called you regarding your enquiry for 1/2/3/4 BHK Flats & Duplex Villas. If you have a moment, please give us a call back at 8249544034."'
    )
    return jsonify({"message": "SMS sent"})


@app.route("/wa", methods=["POST"])
def send_wa():
    try:
        # Run code for sending an SMS
        record = data[current_record]["mobile"].replace("+", "")
        res = requests.post(
            wa_endpoint,
            data=json.dumps({"mobile": record}),
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        print(e)

    return jsonify({"message": "WA sent"})


if __name__ == "__main__":
    read_data()
    app.run(host="0.0.0.0", port=5000, debug=True)
