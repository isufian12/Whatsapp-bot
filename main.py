from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse
from gsheet_func import *

from dateutil.parser import parse

app = Flask(__name__)
count = 0


@app.route('/sms', methods=['POST'])
def replay():
    ...

    incoming_msg = request.form.get('Body','').lower()
    resp = MessagingResponse()
    print(incoming_msg)
    msg = resp.message()
    responded = False
    words = incoming_msg.split('@')
    if "hello" in incoming_msg:
        replay = "hello \nهل تل تريد وضع تذكير؟"
        msg.body(replay)
        responded = True
    if len(words) == 1 and "yes" in incoming_msg:
        reminder_string = " please provide the date like the folowing format.\n\n" \
                          "*Date @*_type the date_"
        msg.body(reminder_string)
        responded = True

    if len(words) == 1 and "no" in incoming_msg:
        reminder_string = " ok have a nice day!\n\n"
        msg.body(replay)
        responded = True
    elif len(words) != 1:
        input_type = words[0].strip().lower()
        input_string = words[1].strip()
        if input_type == "Date":
            replay = "please enter reminder message in the folowing.\n\n" \
                     "*Reminder @*_type the message_"
            set_reminder_date(input_string)
            msg.body(replay)
            responded = True
        if input_type == "responded":
            replay = "your reminder is set "
            set_reminder_body(input_string)
            msg.body(replay)
            responded = True
        if not responded:
            msg.body("not good format")
        return str(resp)


def set_reminder_date(msg):
    p = parse(msg)
    date = p.strftime('%d/%m/%Y')
    save_reminder_date(date)
    return 0


def set_reminder_body(msg):
    save_reminder_body(msg)
    return 0


if __name__ == "__main__":
    app.run(debug=True)
