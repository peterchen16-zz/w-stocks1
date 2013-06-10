import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from datetime import date, timedelta
import random
import webapp2
from google.appengine.ext import db

class GenerateChart(webapp2.RequestHandler):
    
    def get(self):
        
        chart_info_list = []
        info_lists = db.GqlQuery("SELECT date, price_list FROM DailyPriceDB where symbol = 'A' limit 60")
        logging.info(str(info_lists))
        for info_list in info_lists:
            logging.info(str(info_list.date))
            date = info_list.date
            prices = info_list.price_list
            prices.insert(0, date)
            chart_info_list.append(prices)
        html = template.render('templates/candle_chart.html', {'info_list': chart_info_list})
        self.response.write(html)
    
    
    