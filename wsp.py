#!/usr/bin/env python3
"""
Polyglot v2 node server prototype weather service.
Copyright (C) 2018 Robert Paauwe
"""
import polyinterface
import sys
import time
import datetime
import urllib3
import socket
import math
import json

LOGGER = polyinterface.LOGGER

class Controller(polyinterface.Controller):
    id = 'weather'
    hint = [0,0,0,0]
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'WSPrototype'
        self.address = 'weather'
        self.primary = self.address
        self.myConfig = {}

        self.poly.onConfig(self.process_config)

    # Process changes to customParameters
    def process_config(self, config):
        if 'customParams' in config:
            # Check if anything we care about was changed...
            if config['customParams'] != self.myConfig:
                LOGGER.info('TODO: handle configuration change')
                self.myConfig = config['customParams']

    def start(self):
        LOGGER.info('Starting node server')
        # TODO: Process configuration
        # TODO: Discovery
        LOGGER.info('Node server started')

    weather_condition_codes = {
            200 : 'thunderstorm with light rain',
            201 : 'thunderstorm with rain',
            202 : 'thunderstorm with heavy rain',
            210 : 'light thunderstorm',
            211 : 'thunderstorm',
            212 : 'heavy thunderstorm',
            221 : 'ragged thunderstorm',
            230 : 'thunderstorm with light drizzle',
            231 : 'thunderstorm with drizzle',
            232 : 'thunderstorm with heavy drizzle',
            300 : 'light intensity drizzle',
            301 : 'drizzle',
            302 : 'heavy intensity drizzle',
            310 : 'light intensity drizzle rain',
            311 : 'drizzle rain',
            312 : 'heavy intensity drizzle rain',
            313 : 'shower rain and drizzle',
            314 : 'heavy shower rain and drizzle',
            321 : 'shower drizzle',
            500 : 'light rain',
            501 : 'moderate rain',
            502 : 'heavy intensity rain',
            503 : 'very heavy rain',
            504 : 'extreme rain',
            511 : 'freezing rain',
            520 : 'light intensity shower rain',
            521 : 'shower rain',
            522 : 'heavy intensity shower rain',
            531 : 'ragged shower rain',
            600 : 'light snow',
            601 : 'snow',
            602 : 'heavy snow',
            611 : 'sleet',
            612 : 'shower sleet',
            615 : 'light rain and snow',
            616 : 'rain and snow',
            620 : 'light shower snow',
            621 : 'shower snow',
            622 : 'heavy shower snow',
            701 : 'mist',
            711 : 'smoke',
            721 : 'haze',
            731 : 'sand, dust whirls',
            741 : 'fog',
            751 : 'sand',
            761 : 'dust',
            762 : 'volcanic ash',
            771 : 'squalls',
            781 : 'tornado',
            800 : 'clear sky',
            801 : 'few clouds',
            802 : 'scattered clouds',
            803 : 'broken clouds',
            804 : 'overcast clouds'
            }

    def longPoll(self):
        # TODO: poll weather service
        LOGGER.info('TODO: Poll server here')
        # by default JSON is returned
        # http://api.openweathermap.org/data/2.5/weather?zip=95762,us&units=metric&appid=
        # key = a209f3e46e2bc8ee4c75db4c3ef188dd
        request = 'http://api.openweathermap.org/data/2.5/weather'
        request += '?zip=95762,us'
        request += '&units=metric'
        request += '&appid=7b2d3e47f59d0cc115edb018797ca798'
        LOGGER.debug('request = %s' % request)
        http = urllib3.PoolManager()
        c = http.request('GET', request)
        wdata = c.data
        c.close()

        jdata = json.loads(wdata.decode('utf-8'))

        LOGGER.info(jdata)
        # 2018-10-31 14:26:15,960 INFO     b'{
        #  "coord":{"lon":-121.07,"lat":38.69},
        #  "weather":[
        #    {"id":800,
        #     "main":"Clear",
        #     "description":"clear sky",
        #     "icon":"01d"}],
        #  "base":"stations",
        #  "main":{"temp":22.03,
        #          "pressure":1020,
        #          "humidity":26,
        #          "temp_min":19,
        #          "temp_max":24.4},
        #  "visibility":16093,
        #  "wind":{"speed":1.28,
        #          "deg":225.001},
        #  "clouds":{"all":1},
        #  "dt":1541019600,
        #  "sys":{"type":1,"id":422,"message":0.0042,"country":"US","sunrise":1540996267,"sunset":1541034241},
        #  "id":420003069,
        #  "name":"El Dorado Hills",
        #  "cod":200
        # }'

        LOGGER.info('** temperature = %s' % jdata['main']['temp'])


        # TODO: Won't always have everything, need to check if 
        # data exist before trying to use it.
        self.setDriver('CLITEMP', float(jdata['main']['temp']), report=True, force=True)
        self.setDriver('CLIHUM', float(jdata['main']['humidity']), report=True, force=True)
        self.setDriver('BARPRES', float(jdata['main']['pressure']), report=True, force=True)
        self.setDriver('GV0', float(jdata['main']['temp_max']), report=True, force=True)
        self.setDriver('GV1', float(jdata['main']['temp_min']), report=True, force=True)
        self.setDriver('GV4', float(jdata['wind']['speed']), report=True, force=True)
        self.setDriver('WINDDIR', float(jdata['wind']['deg']), report=True, force=True)
        if jdata['rain']:
            self.setDriver('GV6', float(jdata['rain']['3h']), report=True, force=True)
        if jdata['clouds']:
            self.setDriver('GV14', float(jdata['clouds']['all']), report=True, force=True)

        # current conditions, actually might want to look at id instead since
        # that will map to weather condition codes above
        if jdata['weather']:
            self.setDriver('GV13', jdata['weather'][0]['id'], report=True, force=True)

    def query(self):
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        # Create any additional nodes here
        LOGGER.info("In Discovery...")
        self.setDriver('CLITEMP', 100.0, report=True, force=True)

    # Delete the node server from Polyglot
    def delete(self):
        LOGGER.info('Removing node server')

    def stop(self):
        LOGGER.info('Stopping node server')

    def update_profile(self, command):
        st = self.poly.installprofile()
        return st

    def remove_notices_all(self, command):
        self.removeNoticesAll()


    commands = {
            'DISCOVER': discover,
            'UPDATE_PROFILE': update_profile,
            'REMOVE_NOTICES_ALL': remove_notices_all
            }

    drivers = [
            {'driver': 'ST', 'value': 0, 'uom': 2},   # node server status
            {'driver': 'CLITEMP', 'value': 0, 'uom': 4},   # temperature
            {'driver': 'CLIHUM', 'value': 0, 'uom': 22},   # humidity
            {'driver': 'BARPRES', 'value': 0, 'uom': 117}, # pressure
            {'driver': 'WINDDIR', 'value': 0, 'uom': 76},  # direction
            {'driver': 'LUMIN', 'value': 0, 'uom': 36},    # luminins
            {'driver': 'DEWPT', 'value': 0, 'uom': 4},     # dew point
            {'driver': 'GV0', 'value': 0, 'uom': 4},       # max temp
            {'driver': 'GV1', 'value': 0, 'uom': 4},       # min temp
            {'driver': 'GV2', 'value': 0, 'uom': 4},       # feels like
            {'driver': 'GV3', 'value': 0, 'uom': 4},       # average temp
            {'driver': 'GV4', 'value': 0, 'uom': 48},      # wind speed
            {'driver': 'GV5', 'value': 0, 'uom': 48},      # gust speed
            {'driver': 'GV6', 'value': 0, 'uom': 25},      # rain
            {'driver': 'GV7', 'value': 0, 'uom': 82},      # evapotranspiration
            {'driver': 'GV8', 'value': 0, 'uom': 82},      # irrigation req.
            {'driver': 'GV9', 'value': 0, 'uom': 82},      # water deficite
            {'driver': 'GV10', 'value': 0, 'uom': 25},     # elevation
            {'driver': 'GV11', 'value': 0, 'uom': 25},     # climate coverage
            {'driver': 'GV12', 'value': 0, 'uom': 25},     # climate intensity
            {'driver': 'GV13', 'value': 0, 'uom': 25},     # climate conditions
            {'driver': 'GV14', 'value': 0, 'uom': 25},     # cloud conditions
            ]


    
if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('WSP')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
        

