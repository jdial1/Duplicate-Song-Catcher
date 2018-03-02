
import smtplib
import json
from urllib import request
import time
import datetime
import sys
from twilio.rest import Client


prev_song =''
new_song = ''
song_dict = {}
repeat_dict = {}
dup_songs = {}
start_date = {}
stop_date = {}

def send_sms(msg,song_len=0):
    sid = "XX"
    auth = "XX"
    phone = "XX"
    client = Client(sid, auth)
    client.api.account.messages.create(
        to="+XX",
        from_=phone,
        body=msg+':'+str(song_len))
    print('Sending sms to XX, message is '+msg)


def send_email(song='',option='',song_len=0):
    now = datetime.datetime.now()
    gmail_user = "X.com"
    gmail_pwd = "XX"
    FROM = "XX.com"
    TO = "XX.com"
    
    if option == 'dup' and song not in dup_songs:
        SUBJECT = "Duplicate Call XX"
        TEXT = "Call XX Duplicate found "+song
        print("\nDUP SONGS "+song)
        dup_songs[song]=song;
        
    elif option == 'start' and now.strftime("%m-%d") not in start_date:
        SUBJECT = "Starting at "+now.strftime("%m-%d %I:%M %p")
        TEXT = "Starting at "+now.strftime("%I:%M %p")
        print("\nStarting Script "+now.strftime("%m-%d %I:%M %p"))
        start_date[now.strftime("%m-%d")]=now.strftime("%m-%d")
        
    elif option == 'stop' and now.strftime("%m-%d") not in stop_date:
        SUBJECT = "Stopping at"+now.strftime("%m-%d %I:%M %p")
        TEXT = "Stopping at "+now.strftime("%m-%d %I:%M %p")+" Played "+str(song_len)+" Songs today"
        print("\nStopping Script "+now.strftime("%m-%d %I:%M %p"))
        stop_date[now.strftime("%m-%d")]=now.strftime("%m-%d")
        
    
        
    else:
        return
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, TO, SUBJECT, TEXT)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()


def getSong():
    try:
        url = 'XX'
        response = request.urlopen(url)
        data = json.loads(response.read().decode("utf-8"))
        return data[9]['TPE1']+" "+data[9]['TIT2']
    except:
        print('URL FAILURE')
        return ''
        

print('------------------------------------')

send_sms('launching script')
while True:
    new_song = getSong()
    now = datetime.datetime.now()
    if now.hour >= 9  and now.hour <= 16 and len(song_dict) < 1:
        send_email(option='starting scanner at '+now.strftime("%I:%M %p"))
        send_sms('starting scanner at '+now.strftime("%I:%M %p"))
    if prev_song != new_song and new_song != "Today's Best Variety" and now.hour >= 9  and now.hour <= 16 and new_song!=" " and new_song!="  " and new_song!="   " and new_song!="    ":
        if new_song in song_dict:
            send_email(option='dup',song=new_song +" \n Played first at "+ str(song_dict[new_song]['time'])+"\n Played now at "+ now.strftime("%I:%M %p"))
            send_sms(new_song +" \n Played first at "+ str(song_dict[new_song]['time'])+"\n Played now at "+ now.strftime("%I:%M %p"))
        else:
            song_dict[new_song] = {'time' : now.strftime("%I:%M %p")}
            print("Added "+new_song+" at "+ now.strftime("%I:%M %p"))
            print('Song dict length is '+str(len(song_dict)))
            print('------------------------------------')
            prev_song = new_song
    if now.hour > 17 and len(song_dict) > 1:
        send_email(option='stop',song_len=len(song_dict))
        send_sms('stopping scanner at '+now.strftime("%I:%M %p"))
        song_dict.clear()
    time.sleep(30)