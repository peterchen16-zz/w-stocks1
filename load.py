import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from datetime import date, timedelta
import random
import webapp2

from db_models import *
from users import *

class LoadPrice(webapp2.RequestHandler):

    def get(self):
        
        user = users.get_current_user()
        if user.email() == "peterchen16@gmail.com" or user.email() == "admin@w-stocks.com":       
            html = template.render('templates/upload_price.html', {})
            self.response.write(html)
    
    def post(self):
    
        user = users.get_current_user()
        if user.email() == "peterchen16@gmail.com" or user.email() == "admin@w-stocks.com": 
            logging.info("start")
            month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6, "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12} 
            for file_data in self.request.POST.getall('price_file[]'):
                logging.info(file_data.filename)
                results = file_data.value.split('\n')
                for result in results: 
                    if result == "":
                        break
                    else:
                        result = result.split(',')
                        symbol = result[0].upper()
                        logging.info(str(symbol))
                        date1 = result[1]
                        date_list = date1.split("-")
                        logging.info(str(date_list[1]))
                        month = int(month_dict[str(date_list[1])])
                        logging.info(str(month))
                        date2 = date(int(date_list[2]), int(month), int(date_list[0]))
                        logging.info(str(date))
                        open = result[2]
                        logging.info(str(open))
                        high = result[3]
                        low = result[4]
                        close = result[5]
                        volume = result[6]
                        price_list = [float(low), float(open), float(close), float(high)]
                        dailyPrice = DailyPriceDB(symbol=symbol, date=date2, price_list=price_list, volume=int(volume))
                        dailyPrice.put()
                        break