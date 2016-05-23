#!/usr/bin/env python

from screeps import ScreepsConnection
import sys
from twilio.rest import TwilioRestClient
import os
import yaml


def getSettings():
    if not getSettings.settings:
        cwd = os.getcwd()
        path = cwd + '/.settings.yaml'
        if not os.path.isfile(path):
            print 'no settings file found'
            sys.exit(-1)
            return False
        with open(path, 'r') as f:
            getSettings.settings = yaml.load(f)
    return getSettings.settings
getSettings.settings = False

def getScreepsConnection():
    if not getScreepsConnection.sconn:
        settings = getSettings()
        getScreepsConnection.sconn = ScreepsConnection(u=settings['screeps_username'],p=settings['screeps_password'],ptr=settings['screeps_ptr'])
    return getScreepsConnection.sconn
getScreepsConnection.sconn = False

def getNotifications():
    sconn = getScreepsConnection()
    notifications = sconn.memory(path='__notify')
    if 'data' not in notifications:
        return False
    return notifications['data']

def clearNotifications(tick=0):
    print 'clearing sent messages'
    sconn = getScreepsConnection()
    javascript_clear = 'var limit=' + str(tick) + ';'
    javascript_clear += "if(typeof limit == 'undefined') var limit = 0; Memory.__notify = _.filter(Memory.__notify, function(notification){ return notification.tick > this.limit }.bind({'limit':limit}))"
    sconn.console(javascript_clear)

def sendSMS(message):
    settings = getSettings()
    settings['sms_to']
    if not sendSMS.client:
        sendSMS.client = TwilioRestClient(settings['twilio_sid'], settings['twilio_token'])
    message = sendSMS.client.messages.create(
        body=message,
        to=settings['sms_to'],    # Replace with your phone number
        from_=settings['sms_from']) # Replace with your Twilio number
    print(message.sid)
sendSMS.client = False

def main():
    notifications = getNotifications()

    if len(notifications) <= 0:
        print 'No notifications to send.'
        sys.exit(0)

    limit = 0
    print 'Sending notifications.'
    for notification in notifications:
        if notification['tick'] > limit:
            limit = notification['tick']
        sendSMS(notification['message'])
    clearNotifications(limit)

if __name__ == '__main__':
    main()
