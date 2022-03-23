import csv
import os
from twilio.rest import Client
from flask import Flask, request
from datetime import datetime
import time
from multiprocessing import Process, Value


app = Flask(__name__)


def menu(ui, note):

    if (ui == "1"):
        writeNote(note, "notes")
    elif (ui == "2"):
        delNote(note, "notes")
    elif (ui == "3"):
        disNotes("notes", 0)
    elif (ui == "4"):
        writeNote(note, "reminder")
    elif (ui == "5"):
        delNote(note, "reminder")
    elif (ui == "6"):
        disNotes("reminder", 3)
    else:
        sendMsg("""
Help Menu

Type the task number, followed by a period then a space. Then finish the note with what you want to add.

1. then your note - to add notes
2. then note id -  to delete notes
3. to display notes
4. to add a reminder in this format "4. 9. 30. am. Reminder"
5. then reminder id - to delete reminders
6. to display reminders
Anything to display the help menu""")


def writeNote(note, file):
    if (file == "reminder"):
        del note[0]
        fields = note
    else:
        note = note[1]
        fields = [note]
    with open(file + '.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)


def delNote(note, whichCsv):
    # Writes to new temporary csv with everything but specified note
    note = note[1]
    with open(whichCsv + '.csv', 'r') as inp, open('temp.csv', 'w') as out:
        writer = csv.writer(out)
        lineCount = 1
        for row in csv.reader(inp):
            if lineCount != int(note):
                writer.writerow(row)
            lineCount += 1
    # Deletes the old file
    file = whichCsv + '.csv'
    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
    # Writes to original file, by creating it, with no new lines
    with open('temp.csv', newline='') as in_file:
        with open(whichCsv + '.csv', 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if any(field.strip() for field in row):
                    writer.writerow(row)
    # Deletes the temporary file
    file = 'temp.csv'
    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)

    return "Note Deleted"


def disNotes(file, rowNum):
    f = open(file + '.csv', 'a')
    f.close()
    with open(file + '.csv', 'r') as read:
        csv_reader = csv.reader(read, delimiter=',')
        allNotes = "These are your notes: \n"
        lineCount = 1
        for row in csv_reader:
            allNotes += str(lineCount) + ". " + row[rowNum] + "\n"
            lineCount += 1

    sendMsg(allNotes)


def sendMsg(msg):
    account_sid = 'ENTER ACCOUNT SID HERE'
    auth_token = 'ENTER AUTHENTICATION TOKEN HERE'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=msg,
            from_='ENTER YOUR TWILIO NUMBER HERE',
            to='ENTER YOUR VERIFIED NUMBER HERE'
        )
    print(message.sid)


def getReminder():

    f = open('reminder.csv', 'a')
    f.close()

    dictionary = {}
    timeList = []

    with open('reminder.csv', 'r') as inp:
        lineCount = 1
        for row in csv.reader(inp):
            timeList = []
            timeList.append(row[0])
            timeList.append(row[1])
            timeList.append(row[2])
            timeList.append(row[3])
            dictionary[lineCount] = timeList
            lineCount += 1

    return dictionary


def secondaryLoop():
    while(True):
        time.sleep(1)
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        hour = current_time.split(":")[0]
        minute = current_time.split(":")[1]
        minute = minute.split(" ")[0]
        amorpm = current_time.split(" ")[1].lower()
        newDictionary = getReminder()
        for key in newDictionary:
            if (newDictionary[key][0] == hour and newDictionary[key][1] == minute and newDictionary[key][2] == amorpm):
                sendMsg(newDictionary[key][3])
                time.sleep(60)


@app.route("/sms", methods=['GET', 'POST'])
def recMsg():
    msg = request.values.get('Body', None)
    try:
        task = msg.split('.')[0]
        if task != "3":
            note = msg.split('. ')
        else:
            note = "0"
        menu(task, note)
    except IndexError:
        menu("0", "0")


if __name__ == "__main__":
    recording_on = Value('b', True)
    p = Process(target=secondaryLoop)
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()
