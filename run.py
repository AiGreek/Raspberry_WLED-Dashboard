#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import json
from datetime import datetime
import os


from flask import Flask, flash, render_template, redirect, url_for
from flask_appconfig import AppConfig

def create_app(configfile='config.cfg'):
    app = Flask(__name__)
    AppConfig(app, configfile)
    app.debug = app.config['DEBUG']

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/switch')
    def switch():
        templateData = {
            'B_Lights': app.config['BIG_LIGHTS'],
            'S_Lights': app.config['SMALL_LIGHTS'],
            'R_Lights': app.config['RGB_LIGHTS'],            
        }
        return render_template('switch.html', **templateData)

    @app.route('/switch/b/status/<changePin>/<action>')
    def status_b(changePin, action):
        B_Lights    =   app.config['BIG_LIGHTS']
        changePin   =   int(changePin)
        deviceName  =   B_Lights[changePin]['name']

        if action == 'on':
            flash('Turned '+deviceName+' On !')
            os.system('curl '+B_Lights[changePin]['ip']+'/cm?cmnd=Power%20On')
            B_Lights[changePin]['state'] = 'on'
        else:
            flash('Turned '+deviceName+' Off !')
            os.system('curl '+B_Lights[changePin]['ip']+'/cm?cmnd=Power%20Off')
            B_Lights[changePin]['state'] = 'off'

        return redirect(url_for('switch'))

    @app.route('/switch/s/status/<changePin>/<action>')
    def status_s(changePin, action):
        S_Lights    =   app.config['SMALL_LIGHTS']
        changePin   =   int(changePin)
        deviceName  =   S_Lights[changePin]['name']

        if action == 'on':
            flash('Turned '+deviceName+' On !')
            os.system('curl '+S_Lights[changePin]['ip']+'/cm?cmnd=Power%20On')
            S_Lights[changePin]['state'] = 'on'
        else:
            flash('Turned '+deviceName+' Off !')
            os.system('curl '+S_Lights[changePin]['ip']+'/cm?cmnd=Power%20Off')
            S_Lights[changePin]['state'] = 'off'

        return redirect(url_for('switch'))


    @app.route('/switch/rgb/status/<changePin>/<action>')
    def status(changePin, action):
        R_Lights    =   app.config['RGB_LIGHTS']
        changePin   =   int(changePin)
        deviceName  =   R_Lights[changePin]['name']
        l_action    =   ['off','on']
        oscommand   =   ["{'on':'false'}","{'on':'true'}"]
        i           =   l_action.index(action)

        flash('Turned '+deviceName+' '+l_action[i]+' !')
        os.system('curl -X POST -H "Content-Type: application/json" -d'+str(oscommand[i])+' '+R_Lights[changePin]['ip']+'/json/state')
        R_Lights[changePin]['state'] = l_action[i]
               
        return redirect(url_for('switch'))

    @app.route('/switch/rgb/effect/<changePin>/<action>')
    def effect(changePin, action):
        R_Lights =  app.config['RGB_LIGHTS']
        changePin = int(changePin)
        deviceName = R_Lights[changePin]['name']

        l_action = ['1','2','3','4','5','6','7','8','9','10','11']
        oscommand = [
            "{'seg':{'fx':'9'}}","{'seg':{'fx':'88'}}","{'seg':{'fx':'8'}}",
            "{'seg':{'fx':'42'}}","{'seg':{'fx':'101'}}","{'seg':{'fx':'63'}}",
            "{'seg':{'fx':'5'}}","{'seg':{'fx':'60'}}","{'seg':{'fx':'92'}}",
            "{'seg':{'fx':'104'}}","{'seg':{'fx':'3'}}"
        ]
        l_effects = [
            'Rainbow','Candle','ColorLoop','Firework','Pacifica','Pride 2015',
            'Random Color','Scanne Dual','Wipe','Sinelon','Sunrise'
        ]
        i = l_action.index(action)
        flash('Changed '+deviceName+'\'s effect to '+l_effects[i]+' ')
        os.system('curl -X POST -H "Content-Type: application/json" -d'+str(oscommand[i])+' '+R_Lights[changePin]['ip']+'/json/state')
        R_Lights[changePin]['effect'] = l_effects[i]

        return redirect(url_for('switch'))

    @app.route('/switch/rgb/brightness/<changePin>/<action>')
    def brightness(changePin, action):
        R_Lights    =   app.config['RGB_LIGHTS']
        changePin   =   int(changePin)
        deviceName  =   R_Lights[changePin]['name']
        l_action    =   ['12','25','50', '75', '100']
        oscommand   =   ["{'bri':'32'}","{'bri':'64'}","{'bri':'128'}","{'bri':'189'}","{'bri':'255'}"]
        i           =   l_action.index(action)

        flash('Changed '+deviceName+'\'s brightness to '+l_action[i]+' %')
        os.system('curl -X POST -H "Content-Type: application/json" -d'+str(oscommand[i])+' '+R_Lights[changePin]['ip']+'/json/state')
        R_Lights[changePin]['brightness'] = l_action[i]

        return redirect(url_for('switch'))

    @app.route('/switch/rgb/speed/<changePin>/<action>')
    def speed(changePin, action):
        R_Lights    =   app.config['RGB_LIGHTS']
        changePin   =   int(changePin)
        deviceName  =   R_Lights[changePin]['name']
        l_action    =   ['25','50', '75', '100']
        oscommand   =   ["{'seg':{'sx':'64'}}","{'seg':{'sx':'128'}}","{'seg':{'sx':'189'}}","{'seg':{'sx':'255'}}"]
        i           =   l_action.index(action)

        flash('Changed '+deviceName+'\'s speed to '+l_action[i]+' %')
        os.system('curl -X POST -H "Content-Type: application/json" -d'+str(oscommand[i])+' '+R_Lights[changePin]['ip']+'/json/state')
        R_Lights[changePin]['speed'] = l_action[i]

        return redirect(url_for('switch'))

    @app.route('/background')
    def background():
        templateData = {
            'SQUARE_Lights': app.config['RGB_SQUARE']
        }
        return render_template('background.html', **templateData)

    @app.route('/background/status_q/<changePin>/<action>')
    def status_q(changePin, action):
        SQUARE_Lights    =   app.config['RGB_SQUARE']
        changePin   =   int(changePin)
        deviceName  =   SQUARE_Lights[changePin]['name']
        l_action    =   ['off','on']
        oscommand   =   ['{"on":"false"}','{"on":"true"}']
        i           =   l_action.index(action)

        flash('Turned '+deviceName+' '+l_action[i]+' !')
        os.system('curl -X POST -H "Content-Type: application/json" -d'+str(oscommand[i])+' '+SQUARE_Lights[changePin]['ip']+'/json/state')
        SQUARE_Lights[changePin]['state'] = l_action[i]
        
        return redirect(url_for('background'))

    @app.route('/background/color_q/<changePin>/<action>')
    def color_q(changePin, action):
        SQUARE_Lights    =   app.config['RGB_SQUARE']
        changePin   =   int(changePin)
        deviceName  =   SQUARE_Lights[changePin]['name']
        l_action    =   ['1','2', '3', '4','5','6']
        oscommand   =   ['{"seg":[{"col":[[253,0,76]]}]}','{"seg":[{"col":[[254,144,0]]}]}','{"seg":[{"col":[[255,240,32]]}]}','{"seg":[{"col":[[62,223,75]]}]}','{"seg":[{"col":[[51,99,255]]}]}','{"seg":[{"col":[[177,2,183]]}]}']
        i           =   l_action.index(action)

        flash('Turned '+deviceName+' '+l_action[i]+' !')
        os.system('curl -X POST -H "Content-Type: application/json" -d'+str(oscommand[i])+' '+SQUARE_Lights[changePin]['ip']+'/json/state')
        SQUARE_Lights[changePin]['state'] = l_action[i]
        
        return redirect(url_for('background'))

    @app.route('/switch/brightness_q/<changePin>/<action>')
    def brightness_q(changePin, action):
        SQUARE_Lights    =   app.config['RGB_SQUARE']
        changePin   =   int(changePin)
        deviceName  =   SQUARE_Lights[changePin]['name']
        l_action    =   ['12','25','50', '75', '100']
        oscommand   =   ['{"bri":"32"}','{"bri":"64"}','{"bri":"128"}','{"bri":"189"}','{"bri":"255"}']
        i           =   l_action.index(action)

        flash('Changed '+deviceName+'\'s brightness to '+l_action[i]+' %')
        os.system('curl -X POST -H "Content-Type: application/json" -d'+str(oscommand[i])+' '+SQUARE_Lights[changePin]['ip']+'/json/state')
        SQUARE_Lights[changePin]['brightness'] = l_action[i]

        return redirect(url_for('background'))

    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000)