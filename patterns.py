import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from datetime import date, timedelta
from django.core.paginator import Paginator, Page
from google.appengine.ext import db

from db_models import *
import webapp2
from sessions import *

class Skeleton(BaseHandler):
    
    def init_dict(self, title):
        #today = date.today()
        #add market 
        #stat = StatDB.all().filter('market =', market).order('-date').fetch(1)
        stat = StatsDB.all().order('-date').fetch(1)
        logging.info(str(stat))
        logging.info(str(stat[0].combined_degree))
        logging.info(str(stat[0].combined_trend))
        return {'ratio': stat[0].combined_degree, 'trend':stat[0].combined_trend, 'title':title, 'date':stat[0].date}

class NewPatterns(Skeleton):
    
    def get(self):
        
        user = self.current_user()
        new_date = db.GqlQuery("SELECT distinct date from PatternDB order by date desc limit 1")
        pattern_types = PatternTypeDB.all().order('num')
        date = new_date[0].date
        if user:
            #change to true later
            pattern_type = self.request.get('pattern_type_selected')
            position = self.request.get('position_selected')
            if user.paid != False:
                logging.info(pattern_type)
                logging.info(position)
                #date, market, symbol, position, volume, pattern_name, price
                patternString = PatternSearchString(str(date), "", "", position.upper(), "", pattern_type, "")
                patternString1 = patternString.generate_string()
                logging.info(patternString1)
                new_patterns = db.GqlQuery(patternString1)
                prev_page = -1
                next_page = -1
                page_num = self.request.get("page")
                paginator = Paginator(new_patterns, 10)
                page_list = list(range(paginator.num_pages))
                page_list = [x+1 for x in page_list]
                if page_num:
                    page_num = int(page_num)
                    logging.info('total pages')
                    logging.info(str(page_list[len(page_list)-1]))
                    paged_patterns = paginator.page(page_num)
                    logging.info("page num %s", page_num)
                    if int(page_num) != 1:
                        prev_page = int(page_num) -1
                    if int(page_num) != int(page_list[len(page_list)-1]):
                        logging.info("here 17")
                        next_page = int(page_num) + 1
                else:
                    paged_patterns = paginator.page(1)
                    if len(page_list) > 1:
                        next_page = 2
                dict1 = {'user': True, 'patterns': paged_patterns, 'pattern_types':pattern_types,  'pattern_type_selected':pattern_type, 'position_selected':position, 'page_list':page_list, 'current_page':page_num, 'next_page':next_page, 'prev_page':prev_page}
                dict = self.init_dict("New Patterns")
                dict.update(dict1)
                html = template.render('templates/new_patterns.html', dict)
                self.response.write(html)
            else:
                prev_page = -1
                next_page = -1
                logging.info(pattern_type)
                logging.info(position)
                logging.info(date)
                #date, market, symbol, position, volume, pattern_name, price
                patternString = PatternSearchString(str(date), "", "", position, "", pattern_type, "")
                patternString1 = patternString.generate_string()
                patternString1 = patternString1 + " limit 10"
                logging.info(patternString1)
                new_patterns = db.GqlQuery(patternString1)
                dict1 = {'user': True, 'patterns': new_patterns, 'pattern_types':pattern_types, 'next_page':next_page, 'prev_page':prev_page}
                dict = self.init_dict("New Patterns")
                dict.update(dict1)
                html = template.render('templates/new_patterns.html', dict)
                self.response.write(html)
        else:
            prev_page = -1
            next_page = -1
            #new_patterns = PatternDB.all().filter('date =', date2).fetch(10)
            patternString = PatternSearchString(str(date), "", "", "", "", "", "")
            patternString1 = patternString.generate_string()
            patternString1 = patternString1 + " limit 5"
            logging.info(patternString1)
            new_patterns = db.GqlQuery(patternString1)
            html = template.render('templates/new_patterns.html', {'no_user': True, 'patterns': new_patterns, 'pattern_types':pattern_types, 'next_page':next_page, 'prev_page':prev_page})
            self.response.write(html)

    def post(self):
        
        user = self.current_user()
        new_date = db.GqlQuery("SELECT distinct date from PatternDB order by date desc limit 1")
        pattern_types = PatternTypeDB.all().order('num')
        date = new_date[0].date
        if user:
            #change to true later
            if user.paid != False:
                pattern_type = self.request.get('pattern_type_choice')
                position = self.request.get('position_choice')
                logging.info(pattern_type)
                logging.info(position)
                #date, market, symbol, position, volume, pattern_name, price
                patternString = PatternSearchString(str(date), "", "", position.upper(), "", pattern_type, "")
                patternString1 = patternString.generate_string()
                logging.info(patternString1)
                new_patterns = db.GqlQuery(patternString1)
                prev_page = -1
                next_page = -1
                page_num = self.request.get("page")
                paginator = Paginator(new_patterns, 10)
                page_list = list(range(paginator.num_pages))
                page_list = [x+1 for x in page_list]
                if page_num:
                    page_num = int(page_num)
                    logging.info('total pages')
                    logging.info(str(page_list[len(page_list)-1]))
                    paged_patterns = paginator.page(page_num)
                    logging.info("page num %s", page_num)
                    if int(page_num) != 1:
                        prev_page = int(page_num) -1
                    if int(page_num) != int(page_list[len(page_list)-1]):
                        logging.info("here 17")
                        next_page = int(page_num) + 1
                else:
                    paged_patterns = paginator.page(1)
                    if len(page_list) > 1:
                        next_page = 2
                dict1 = {'user': True, 'patterns': paged_patterns, 'pattern_types':pattern_types, 'pattern_type_selected':pattern_type, 'position_selected':position, 'page_list':page_list, 'current_page':page_num, 'next_page':next_page, 'prev_page':prev_page}
                dict = self.init_dict("New Patterns")
                dict.update(dict1)
                html = template.render('templates/new_patterns.html', dict)
                self.response.write(html)
            else:
                prev_page = -1
                next_page = -1
                pattern_type = self.request.get('pattern_type_choice')
                position = self.request.get('position_choice')
                if (pattern_type != "" or position != "") and (pattern_type != "--Pattern Type--" or position != "--Position--"):
                    logging.info("here message")
                    message = True
                else:
                    message = False
                logging.info(pattern_type)
                logging.info(position)
                logging.info(date)
                #date, market, symbol, position, volume, pattern_name, price
                patternString = PatternSearchString(str(date), "", "", "", "", "", "")
                patternString1 = patternString.generate_string()
                patternString1 = patternString1 + " limit 10"
                logging.info(patternString1)
                new_patterns = db.GqlQuery(patternString1)
                dict1 = {'user': True, 'message':message, 'patterns': new_patterns, 'pattern_types':pattern_types, 'next_page':next_page, 'prev_page':prev_page}
                dict = self.init_dict("New Patterns")
                dict.update(dict1)
                html = template.render('templates/new_patterns.html', dict)
                self.response.write(html)
        else:
            prev_page = -1
            next_page = -1
            #new_patterns = PatternDB.all().filter('date =', date2).fetch(10)
            patternString = PatternSearchString(str(date), "", "", "", "", "", "")
            patternString1 = patternString.generate_string()
            patternString1 = patternString1 + " limit 5"
            logging.info(patternString1)
            new_patterns = db.GqlQuery(patternString1)
            logging.info("no user")
            html = template.render('templates/new_patterns.html', {'no_user': True, 'patterns': new_patterns, 'pattern_types':pattern_types, 'next_page':next_page, 'prev_page':prev_page})
            self.response.write(html)
            
class PastPatterns(Skeleton):
    
    def get(self):
        
        user = self.current_user()
        dates = db.GqlQuery("SELECT distinct date from PatternDB order by date desc limit 11")
        #date representation
        dates1 = dates[1:11]
        dates_1 = []
        for date in dates1:
            dates_1.append(str(date.date))
        logging.info(str(dates_1))
        #date representation
        dates2 = dates[6:11]
        dates_2 = []
        for date in dates2:
            dates_2.append(str(date.date))
        logging.info(str(dates_2))
        pattern_types = PatternTypeDB.all().order('num')
        #string representation example: "2013-04-01"
        date1 = dates_1[0]
        date2 = dates_2[0]
        dates__1 = zip(dates1, dates_1)
        dates__2 = zip(dates2, dates_2)
        #total_new_patterns = len(new_patterns)
        if user:
            #change to true later
            pattern_type = self.request.get('pattern_type_selected')
            position = self.request.get('position_selected')
            date_selected = self.request.get('date_selected')
            if user.paid != False:
                logging.info(date_selected)
                if date_selected == "" or date_selected =="--Date--":
                    date_selected = date1
                else:
                    date1 = date_selected
                logging.info("date_selected %s", date_selected)    
                logging.info(pattern_type)
                logging.info(position)
                logging.info(date1)
                #date, market, symbol, position, volume, pattern_name, price
                patternString = PatternSearchString(date1, "", "", position.upper(), "", pattern_type, "")
                patternString1 = patternString.generate_string() + " order by date desc"
                logging.info(patternString1)
                new_patterns = db.GqlQuery(patternString1)
                prev_page = -1
                next_page = -1
                page_num = self.request.get("page")
                paginator = Paginator(new_patterns, 10)
                page_list = list(range(paginator.num_pages))
                page_list = [x+1 for x in page_list]
                if page_num:
                    page_num = int(page_num)
                    logging.info('total pages')
                    logging.info(str(page_list[len(page_list)-1]))
                    paged_patterns = paginator.page(page_num)
                    logging.info("page num %s", page_num)
                    if int(page_num) != 1:
                        prev_page = int(page_num) -1
                    if int(page_num) != int(page_list[len(page_list)-1]):
                        logging.info("here 17")
                        next_page = int(page_num) + 1
                else:
                    paged_patterns = paginator.page(1)
                    if len(page_list) > 1:
                        next_page = 2
                dict1 = {'user': True, 'patterns': paged_patterns, 'pattern_types':pattern_types, 'dates':dates__1, 'pattern_type_selected':pattern_type, 'position_selected':position, 'date_selected':date_selected, 'page_list':page_list, 'current_page':page_num, 'next_page':next_page, 'prev_page':prev_page}
                dict = self.init_dict("Past Patterns")
                dict.update(dict1)
                html = template.render('templates/past_patterns.html', dict)
                self.response.write(html)
            else:
                prev_page = -1
                next_page = -1
                logging.info(date_selected)
                if date_selected == "":
                    date_selected = date2
                else:
                    date2 = date_selected
                logging.info("date_selected get %s", date_selected)    
                logging.info(pattern_type)
                logging.info(position)
                logging.info(date1)
                #date, market, symbol, position, volume, pattern_name, price
                patternString = PatternSearchString(date2, "", "", position, "", pattern_type, "")
                patternString1 = patternString.generate_string() + "order by date desc"
                patternString1 = patternString1 + " limit 5"
                logging.info(patternString1)
                new_patterns = db.GqlQuery(patternString1)
                dict1 = {'user': True, 'patterns': new_patterns, 'pattern_types':pattern_types, 'dates':dates__2, 'pattern_type_selected':pattern_type, 'position_selected':position, 'date_selected':date_selected, 'next_page':next_page, 'prev_page':prev_page}
                dict = self.init_dict(dict1)
                dict.update(dict1)
                html = template.render('templates/past_patterns.html', dict)
                self.response.write(html)
        else:
            prev_page = -1
            next_page = -1
            #new_patterns = PatternDB.all().filter('date =', date2).fetch(10)
            patternString = PatternSearchString(date2, "", "", "", "", "", "")
            patternString1 = patternString.generate_string() 
            patternString1 = patternString1 + " limit 10"
            logging.info(patternString1)
            new_patterns = db.GqlQuery(patternString1)
            html = template.render('templates/past_patterns.html', {'no_user': True, 'patterns': new_patterns, 'pattern_types':pattern_types, 'dates':date2, 'next_page':next_page, 'prev_page':prev_page})
            self.response.write(html)

    def post(self):
        
        user = self.current_user()
        dates = db.GqlQuery("SELECT distinct date from PatternDB order by date desc limit 11")
        #date representation
        dates1 = dates[1:11]
        dates_1 = []
        for date in dates1:
            dates_1.append(str(date.date))
        logging.info(str(dates_1))
        #date representation
        dates2 = dates[6:11]
        dates_2 = []
        for date in dates2:
            dates_2.append(str(date.date))
        logging.info(str(dates_2))
        pattern_types = PatternTypeDB.all().order('num')
        #string representation example: "2013-04-01"
        date1 = dates_1[0]
        date2 = dates_2[0]
        dates__1 = zip(dates1, dates_1)
        dates__2 = zip(dates2, dates_2)
        #total_new_patterns = len(new_patterns)
        if user:
            #change to true later
            if user.paid != False:
                pattern_type = self.request.get('pattern_type_choice')
                position = self.request.get('position_choice')
                date_selected = self.request.get('date_choice')
                logging.info(date_selected)
                if date_selected == "" or date_selected == "--Date--":
                    date_selected = date1
                else:
                    date1 = date_selected
                logging.info("date_selected %s", date_selected)    
                logging.info(pattern_type)
                logging.info(position)
                logging.info(date1)
                #date, market, symbol, position, volume, pattern_name, price
                patternString = PatternSearchString(date1, "", "", position.upper(), "", pattern_type, "")
                patternString1 = patternString.generate_string()
                logging.info(patternString1)
                new_patterns = db.GqlQuery(patternString1)
                prev_page = -1
                next_page = -1
                page_num = self.request.get("page")
                paginator = Paginator(new_patterns, 10)
                page_list = list(range(paginator.num_pages))
                page_list = [x+1 for x in page_list]
                if page_num:
                    page_num = int(page_num)
                    logging.info('total pages')
                    logging.info(str(page_list[len(page_list)-1]))
                    paged_patterns = paginator.page(page_num)
                    logging.info("page num %s", page_num)
                    if int(page_num) != 1:
                        prev_page = int(page_num) -1
                    if int(page_num) != int(page_list[len(page_list)-1]):
                        logging.info("here 17")
                        next_page = int(page_num) + 1
                else:
                    paged_patterns = paginator.page(1)
                    if len(page_list) > 1:
                        next_page = 2
                dict1 = {'user': True, 'patterns': paged_patterns, 'pattern_types':pattern_types, 'dates':dates__1, 'pattern_type_selected':pattern_type, 'position_selected':position, 'date_selected':date_selected, 'page_list':page_list, 'current_page':page_num, 'next_page':next_page, 'prev_page':prev_page}
                dict = self.init_dict("Past Patterns")
                dict.update(dict1)
                html = template.render('templates/past_patterns.html', dict)
                self.response.write(html)
            else:
                prev_page = -1
                next_page = -1
                pattern_type = self.request.get('pattern_type_choice')
                position = self.request.get('position_choice')
                date_selected = self.request.get('date_choice')
                logging.info(date_selected)
                if date_selected == "":
                    date_selected = date2
                else:
                    date2 = date_selected
                if (pattern_type != "" or position != "") and (pattern_type != "--Pattern Type--" or position != "--Position--"):
                    logging.info("here message")
                    message = True
                else:
                    message = False
                logging.info("date_selected %s", date_selected)    
                logging.info(pattern_type)
                logging.info(position)
                logging.info(date1)
                #date, market, symbol, position, volume, pattern_name, price
                patternString = PatternSearchString(date2, "", "", "", "", "", "")
                patternString1 = patternString.generate_string() + " order by date desc"
                patternString1 = patternString1 + " limit 5"
                logging.info(patternString1)
                new_patterns = db.GqlQuery(patternString1)
                dict1 = {'user': True, 'message':message, 'patterns': new_patterns, 'pattern_types':pattern_types, 'dates':dates__2, 'date_selected':date_selected, 'next_page':next_page, 'prev_page':prev_page}
                dict = self.init_dict("Past Patterns")
                dict.update(dict1)
                html = template.render('templates/past_patterns.html', dict)
                self.response.write(html)
        else:
            prev_page = -1
            next_page = -1
            #new_patterns = PatternDB.all().filter('date =', date2).fetch(10)
            patternString = PatternSearchString(date2, "", "", "", "", "", "")
            patternString1 = patternString.generate_string()
            patternString1 = patternString1 + " limit 10"
            logging.info(patternString1)
            new_patterns = db.GqlQuery(patternString1)
            logging.info("no user")
            html = template.render('templates/past_patterns.html', {'no_user': True, 'patterns': new_patterns, 'pattern_types':pattern_types, 'dates':date2, 'next_page':next_page, 'prev_page':prev_page})
            self.response.write(html)
            
class SearchPatterns(Skeleton):
    
    def get(self):
        
        user = self.current_user()
        pattern_types = PatternTypeDB.all().order('num')
        dates_db = db.GqlQuery("SELECT distinct date from PatternDB order by date desc limit 30")
        #date representation
        dates_str = []
        for date in dates_db:
            dates_str.append(str(date.date))
        date = dates_str[0]
        dates = zip(dates_db, dates_str)
        price_list = ["<5", "5-10", "10-20", "20-30", "30-40", "40-50", "50-100", "100-200", "200-300", "300-400", "400-500", ">500"]
        volume_list = ["<1M", "1M-2M", "2M-3M", "3M-4M", "4M-5M", "5M-6M", "6M-7M", "7M-8M", "8M-9M", "9M-10M", ">10M"]
        pattern_type = self.request.get('pattern_type_selected')
        position = self.request.get('position_selected')
        date_selected = self.request.get('date_selected')
        market = self.request.get('market_selected')
        price = self.request.get('price_selected')
        volume = self.request.get('volume_selected')
        if user:
            if user.paid != False:
                if date_selected == "" or "--Date--":
                    date_selected = date
                else:
                    date = date_selected
                logging.info(pattern_type)
                logging.info(position)
                logging.info(date)
                #date, market, symbol, position, volume, pattern_name, price
                patternString = PatternSearchString(date, market, "", position.upper(), volume, pattern_type, price)
                patternString1 = patternString.generate_string()
                logging.info(patternString1)
                new_patterns = db.GqlQuery(patternString1)
                prev_page = -1
                next_page = -1
                page_num = self.request.get("page")
                paginator = Paginator(new_patterns, 10)
                page_list = list(range(paginator.num_pages))
                page_list = [x+1 for x in page_list]
                if page_num:
                    page_num = int(page_num)
                    logging.info('total pages')
                    logging.info(str(page_list[len(page_list)-1]))
                    paged_patterns = paginator.page(page_num)
                    logging.info("page num %s", page_num)
                    if int(page_num) != 1:
                        prev_page = int(page_num) -1
                    if int(page_num) != int(page_list[len(page_list)-1]):
                        logging.info("here 17")
                        next_page = int(page_num) + 1
                else:
                    paged_patterns = paginator.page(1)
                    if len(page_list) > 1:
                        next_page = 2
                dict1 = {'user': True, 'patterns': paged_patterns, 'pattern_types':pattern_types, 'dates':dates, 
                        'price_list':price_list, 'volume_list':volume_list, 'pattern_type_selected':pattern_type, 
                        'position_selected':position, 'date_selected':date_selected, 'market_selected':market,
                        'price_selected':price, 'volume_selected':volume, 'page_list':page_list, 'current_page':page_num, 
                        'next_page':next_page, 'prev_page':prev_page}
                dict = self.init_dict("Search Patterns")
                dict.update(dict1)
                html = template.render('templates/search_patterns.html', dict)
                self.response.write(html)
            else:
                html = template.render('templates/search_patterns.html', {'no_upgrade': True})
                self.response.write(html)
        else:
            html = template.render('templates/search_patterns.html', {'no_user': True})
            self.response.write(html)

    def post(self):
        
        user = self.current_user()
        pattern_types = PatternTypeDB.all().order('num')
        dates_db = db.GqlQuery("SELECT distinct date from PatternDB order by date desc limit 30")
        #date representation
        dates_str = []
        for date in dates_db:
            dates_str.append(str(date.date))
        date = dates_str[0]
        dates = zip(dates_db, dates_str)
        date_selected = self.request.get('date_choice')
        price_list = ["<5", "5-10", "10-20", "20-30", "30-40", "40-50", "50-100", "100-200", "200-300", "300-400", "400-500", ">500"]
        volume_list = ["<1M", "1M-2M", "2M-3M", "3M-4M", "4M-5M", "5M-6M", "6M-7M", "7M-8M", "8M-9M", "9M-10M", ">10M"]
        pattern_type = self.request.get('pattern_type_choice')
        position = self.request.get('position_choice')
        market = self.request.get('market_choice')
        price = self.request.get('price_choice')
        volume = self.request.get('volume_choice')
        symbol = self.request.get('symbol').upper()
        if user:
            #change to true later
            if user.paid != False:
                if date_selected == "":
                    date_selected = date
                else:
                    date = date_selected
                logging.info("date_selected %s", date_selected)    
                logging.info(pattern_type)
                logging.info(position)
                logging.info(date_selected)
                logging.info(symbol)
                #date, market, symbol, position, volume, pattern_name, price
                patternString = PatternSearchString(date, market, symbol, position.upper(), volume, pattern_type, price)
                patternString1 = patternString.generate_string()
                logging.info(patternString1)
                new_patterns = db.GqlQuery(patternString1)
                prev_page = -1
                next_page = -1
                page_num = self.request.get("page")
                paginator = Paginator(new_patterns, 10)
                page_list = list(range(paginator.num_pages))
                page_list = [x+1 for x in page_list]
                if page_num:
                    page_num = int(page_num)
                    logging.info('total pages')
                    logging.info(str(page_list[len(page_list)-1]))
                    paged_patterns = paginator.page(page_num)
                    logging.info("page num %s", page_num)
                    if int(page_num) != 1:
                        prev_page = int(page_num) -1
                    if int(page_num) != int(page_list[len(page_list)-1]):
                        logging.info("here 17")
                        next_page = int(page_num) + 1
                else:
                    paged_patterns = paginator.page(1)
                    if len(page_list) > 1:
                        next_page = 2
                dict1 = {'user': True, 'patterns': paged_patterns, 'pattern_types':pattern_types, 'dates':dates, 
                        'price_list':price_list, 'volume_list':volume_list, 'pattern_type_selected':pattern_type, 
                        'position_selected':position, 'date_selected':date_selected, 'market_selected':market,
                        'price_selected':price, 'volume_selected':volume, 'page_list':page_list, 'current_page':page_num, 
                        'next_page':next_page, 'prev_page':prev_page}
                dict = self.init_dict("Search Patterns")
                dict.update(dict1)
                html = template.render('templates/search_patterns.html', dict)
                self.response.write(html)
            else:
                html = template.render('templates/search_patterns.html', {'no_upgrade':True})
                self.response.write(html)
        else:
            html = template.render('templates/search_patterns.html', {'no_user': True})
            self.response.write(html)

class PatternSearchString:
    
    def __init__(self, date, market, symbol, position, volume, pattern_name, price):
        
        self.search_string = "SELECT * FROM PatternDB"
        self.date = date
        logging.info(str(self.date))
        self.market = market
        logging.info(str(self.market))
        self.symbol = symbol
        logging.info(self.symbol)
        self.type = position
        logging.info(self.type)
        self.volume = volume
        logging.info(str(self.volume))
        self.pattern_name = pattern_name
        logging.info(self.pattern_name)
        self.price = price
        logging.info(str(self.price))
        
    def generate_string(self):
        
        if self.date != "" and self.date != "--Date--":
            self.search_string = self.search_string + " where date = DATE('" + self.date + "')"
        if self.market != "" and self.market != "--Market--":
            if "where" not in self.search_string:
                self.search_string = self.search_string + " where market = '" + str(self.market) + "'"
            else:
                self.search_string = self.search_string + " and market = '" + str(self.market) + "'"
        if self.symbol != "":
            logging.info("find symbol")
            if "where" not in self.search_string:
                self.search_string = self.search_string + " where symbol = '" + str(self.symbol) + "'"
            else:
                self.search_string = self.search_string + " and symbol = '" + str(self.symbol) + "'"
        if self.type != "" and self.type != "--POSITION--":
            if "where" not in self.search_string:
                self.search_string = self.search_string + " where type = '" + str(self.type) + "'"
            else:
                self.search_string = self.search_string + " and type = '" + str(self.type) + "'"
        if self.volume != "" and self.volume != "--Volume--":
            if "where" not in self.search_string:
                self.search_string = self.search_string + " where volumn_range = '" + str(self.volume) + "'"
            else:
                self.search_string = self.search_string + " and volumn_range = '" + str(self.volume) + "'"
        if self.pattern_name != "" and self.pattern_name != "--Pattern Type--":
            if "where" not in self.search_string:
                self.search_string = self.search_string + " where pattern_name = '" + str(self.pattern_name) + "'"
            else:
                self.search_string = self.search_string + " and pattern_name = '" + str(self.pattern_name) + "'"
        if self.price != "" and self.price != "--Price--":
            if "where" not in self.search_string:
                self.search_string = self.search_string + " where price_range = '" + str(self.price) + "'"
            else:
                self.search_string = self.search_string + " and price_range = '" + str(self.price) + "'"
        return self.search_string

def convert_date(date):
    
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    date = date.split(",")
    month_day = date[0].split(" ")
    month = month_day[0]
    day = month_day[1]
    if len(day) == 1:
        day = "0" + str(day)
    else:
        day = str(day)
    for i in range(12):
        if months[i] == month:
            month = str(i+1)
    if len(month) == 1:
        month = "0" + month
    else:
        month = month
    year = date[1]
    year = year[1:]
    date = year + "-" + month + "-" + day
    return date    