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
from patterns import *
from sessions import *
from candle_patterns import *
from payment import *
from load import *
from chart import *

class MainHandler(BaseHandler):
    
    def get(self):
        
        user = self.current_user()
        example_pattern = PatternDB.all().order('-date').fetch(1)[0]
        yesterday = date.today() - timedelta(days=2)
        if user:
            volumn = self.request.get('volume')
            symbol = self.request.get('symbol')
            logging.info(str(volumn))
            logging.info(str(symbol))
            logging.info('symbol and volumn') 
            if volumn == "" and symbol == "":
                five_days_ago = date.today() - timedelta(days=6)
                patterns_long = PatternDB.all().filter('date <=', yesterday).filter('date >=', five_days_ago).filter('type =', "LONG")
                num_long_five_days = patterns_long.count()
                patterns_short = PatternDB.all().filter('date <=', yesterday).filter('date >=', five_days_ago).filter('type =', "SHORT")
                num_short_five_days = patterns_short.count()
                patterns1_long = PatternDB.all().filter('date =', yesterday).filter('type =', "LONG")
                num_long_yesterday = patterns1_long.count()
                patterns1_short = PatternDB.all().filter('date =', yesterday).filter('type =', "SHORT")
                num_short_yesterday = patterns1_short.count()
                html = template.render('templates/index.html', {'user': True, 'pattern': example_pattern, 'num_long_five_days': num_long_five_days, 'num_short_five_days': num_short_five_days, 'num_long_yesterday': num_long_yesterday, 'num_short_yesterday': num_short_yesterday})
                self.response.write(html)
            else:
                logging.info("single chart")
                html = template.render('templates/single_chart.html', {'symbol': symbol, 'volume': volumn})
                self.response.write(html)
        else:
            five_days_ago = date.today() - timedelta(days=6)
            patterns_long = PatternDB.all().filter('date <=', yesterday).filter('date >=', five_days_ago).filter('type =', "LONG")
            num_long_five_days = patterns_long.count()
            patterns_short = PatternDB.all().filter('date <=', yesterday).filter('date >=', five_days_ago).filter('type =', "SHORT")
            num_short_five_days = patterns_short.count()
            patterns1_long = PatternDB.all().filter('date =', yesterday).filter('type =', "LONG")
            num_long_yesterday = patterns1_long.count()
            patterns1_short = PatternDB.all().filter('date =', yesterday).filter('type =', "SHORT")
            num_short_yesterday = patterns1_short.count()
            html = template.render('templates/index.html', {'pattern': example_pattern, 'num_long_five_days': num_long_five_days, 'num_short_five_days': num_short_five_days, 'num_long_yesterday': num_long_yesterday, 'num_short_yesterday': num_short_yesterday})
            self.response.write(html)

class Classroom(BaseHandler):
    
    def get(self):
        
        user = self.current_user()
        html = template.render('templates/classroom.html', {'user': user})
        self.response.write(html)
        
class AboutUs(BaseHandler):

    def get(self):
        
        user = self.current_user()
        html = template.render('templates/about_us.html', {'user': user})
        self.response.write(html)
        
class PrivacyStatement(BaseHandler):
    
    def get(self):
        
        user = self.current_user()
        html = template.render('templates/privacy_statement.html', {'user': user})
        self.response.write(html)

class Disclaimer(BaseHandler):
    
    def get(self):
        
        user = self.current_user()
        html = template.render('templates/disclaimer.html', {'user': user})
        self.response.write(html)

class FYI(BaseHandler):
    
    def get(self):
    
        user = self.current_user()
        html = template.render('templates/fyi.html', {'user': user})
        self.response.write(html)
        
class Request(BaseHandler):
    
    def get(self):
    
        user = self.current_user()
        html = template.render('templates/request.html', {'user': user})
        self.response.write(html)
        
    def post(self):
        
        user = self.current_user()
        name = self.request.get('name')
        email = self.request.get('email')
        description = self.request.get('pattern_description')
        html = template.render('templates/contact_message.html', {'user':user, 'name':name, 'email':email, 'comments':description})
        subject_line = name + "'s Wanted Pattern"
        email_list = ["W-Stocks Admin <admin@w-stocks.com>"]
        mail.send_mail(sender="W-Stocks <admin@w-stocks.com>", to=email_list, subject=subject_line, body=html, html=html)
        message1 = "Thanks for submitting your pattern description " + name + "!"
        message2 = "We will reply you as soon as possible."
        html = template.render('templates/request.html', {'message1':message1, 'message2':message2})
        self.response.write(html)
        
class PlainDisclaimer(BaseHandler):
    
    def get(self):
        
        html = template.render('templates/disclaimer_plain.html', {})
        self.response.write(html)

class ContactUs(BaseHandler):

    def get(self):
        
        user = self.current_user()
        html = template.render('templates/contact_us.html', {'user':user})
        self.response.write(html)
        
    def post(self):
        
        user = self.current_user()
        name = self.request.get('name')
        email = self.request.get('email')
        comments = self.request.get('comments')
        html = template.render('templates/contact_message.html', {'user':user,'name':name, 'email':email, 'comments':comments})
        subject_line = name + "'s Questions/Suggestions"
        email_list = ["W-Stocks Admin <admin@w-stocks.com>"]
        mail.send_mail(sender="W-Stocks <admin@w-stocks.com>", to=email_list, subject=subject_line, body=html, html=html)
        message1 = "Thanks for submitting your questions/suggestions " + name + "!"
        message2 = "We will reply you as soon as possible(usully within 24hrs)."
        html = template.render('templates/contact_us.html', {'message1':message1, 'message2':message2})
        self.response.write(html)
        
class Chat(BaseHandler):
    
    def get(self):
        
        user = self.current_user()
        html = template.render('templates/chat.html', {'user':user})
        self.response.write(html)

class DetectBrowser(webapp2.RequestHandler):
    
    def get(self):
        
        html = template.render('templates/default_browser.html', {})
        self.response.write(html)
        
class HistoricalTrendicator(BaseHandler):
    
    def get(self):
        
        user = self.current_user()
        if user:
            if user.paid == True:
                stats = StatsDB.all().order('-date').filter('market =', "US").fetch(100)
                market = "US"
                logging.info(str(stats))
                html = template.render('templates/historical_trendicator.html', {'user':user, 'trendicators':stats, 'market':market, 'market_selected':market})
                self.response.write(html)
        else:
            self.redirect('/')
            
    def post(self):
        
        user = self.current_user()
        if user:
            if user.paid == True:
                market = self.request.get('market_choice')
                if market != "" and market != "--Market--":
                    stats = StatsDB.all().order('-date').filter('market =', market).fetch(100)
                else:
                    stats = StatsDB.all().order('-date').filter('market =', "US").fetch(100)
                    market = "US"
                logging.info(str(stats))
                html = template.render('templates/historical_trendicator.html', {'user':user, 'trendicators':stats, 'market':market, 'market_selected':market})
                self.response.write(html)
        else:
            self.redirect('/')

class ChangeStats(webapp2.RequestHandler):
    
    def get(self):
        
        stats = StatsDB.all().order('-date')
        for stat in stats:
            ratio = stat.ratio
            if ratio >= 3: num = 4
            elif 3 >= ratio >=2: num = 3
            elif 2 >= ratio >= 1.5: num = 2
            elif 1.5 >= ratio >= 1.05: num = 1
            elif 0.95 <= ratio <= 1.05: num = 0
            elif 0.667 <= ratio <= 0.95: num = -1
            elif 0.5 <= ratio <= 0.667: num = -2 
            elif 0.333 <= ratio <= 0.5: num = -3
            elif ratio <= 0.333: num = -4
            if num > 0: 
                trend = "Uptrend"
            elif num < 0:
                trend = "Downtrend"
            else:
                trend = "Neutral" 
            stat.degree = num
            stat.trend = trend
            stat.market = "US"
            stat.put()

class GenerateStats(webapp2.RequestHandler):
    
    def get(self):
        
        user = users.get_current_user()
        if user.email() == "peterchen16@gmail.com" or user.email() == "admin@w-stocks.com":   
            today = date.today() - timedelta(days=1)
            logging.info(str(today))
            #long_patterns = db.GqlQuery("SELECT * FROM PatternDB where date = DATE('2013-05-15') and type = 'LONG' and market = 'US'")
            long_patterns_chart = PatternDB.all().filter('type =', 'LONG').filter('date =', today).filter('market =', 'US')
            short_patterns_chart = PatternDB.all().filter('type =', 'SHORT').filter('date =', today).filter('market =', 'US')
            long_patterns_candle = CandlePatternDB.all().filter('type =', 'LONG').filter('date =', today).filter('market =', 'US').filter('pattern_name !=', 'Morning Star')
            short_patterns_candle = CandlePatternDB.all().filter('type =', 'SHORT').filter('date =', today).filter('market =', 'US')
            chart_long_num = long_patterns_chart.count()
            chart_short_num = short_patterns_chart.count()
            candle_long_num = long_patterns_candle.count()
            candle_short_num = short_patterns_candle.count()
            total_longs = chart_long_num + candle_long_num
            total_shorts = chart_short_num + candle_short_num
            logging.info("chart long" + str(chart_long_num))
            logging.info("chart shorts" + str(chart_short_num))
            logging.info("candle long" + str(candle_long_num))
            logging.info("candle shorts" + str(candle_short_num))
            logging.info("total long" + str(total_longs))
            logging.info("total shorts" + str(total_shorts))
            if total_longs != 0 or total_shorts != 0 or chart_long_num != 0 or chart_short_num != 0 or candle_long_num != 0 or candle_short_num != 0:
                stats = StatsDB()
                #for eastern time, subtract one 
                stats.date = today 
                stats.total_num_longs = int(total_longs)
                stats.total_num_shorts = int(total_shorts)
                stats.chart_pattern_long = chart_long_num
                stats.chart_pattern_short = chart_short_num
                stats.candle_pattern_long = candle_long_num
                stats.candle_pattern_short = candle_short_num
                stats.chart_ratio = float(chart_long_num) / float(chart_short_num)
                stats.candle_ratio = float(candle_long_num) / float(candle_short_num)
                stats.combined_ratio = float(total_longs) / float(total_shorts)
                ratios = [stats.chart_ratio, stats.candle_ratio, stats.combined_ratio]
                degrees = [stats.chart_degree, stats.candle_degree, stats.combined_degree]
                trends = [stats.chart_trend, stats.candle_trend, stats.combined_trend]
                for n in range(3):
                    logging.info(str(ratios[n]))
                    if ratios[n] >= 3: degrees[n] = 4
                    elif 3 >= ratios[n] >=2: degrees[n] = 3
                    elif 2 >= ratios[n] >= 1.5: degrees[n] = 2
                    elif 1.5 >= ratios[n] >= 1.05: degrees[n] = 1
                    elif 0.95 <= ratios[n] <= 1.05: degrees[n] = 0
                    elif 0.667 <= ratios[n] <= 0.95: degrees[n] = -1
                    elif 0.5 <= ratios[n] <= 0.667: degrees[n] = -2 
                    elif 0.333 <= ratios[n] <= 0.5: degrees[n] = -3
                    elif ratios[n] <= 0.333: degrees[n] = -4
                    logging.info(str(degrees[n]))
                    if degrees[n] > 0: 
                        trends[n] = "Uptrend"
                    elif degrees[n] < 0:
                        trends[n] = "Downtrend"
                    else:
                        trends[n] = "Neutral" 
                    logging.info(str(trends[n]))
                stats.chart_degree = degrees[0]
                stats.candle_degree = degrees[1]
                stats.combined_degree = degrees[2]
                stats.chart_trend = trends[0]
                stats.candle_trend = trends[1]
                stats.combined_trend = trends[2]
                stats.market = "US"
                stats.put()
        
#for US market
class UploadFile(webapp2.RequestHandler):
    
    def generate_num_longs_shorts_US(self):
        
        today = date.today() - timedelta(days=1)
        logging.info(str(today))
        long_patterns = PatternDB.all().filter('type =', 'LONG').filter('date =', today).filter('market =', 'US')
        short_patterns = PatternDB.all().filter('type =', 'SHORT').filter('date =', today).filter('market =', 'US')
        long_patterns_candle = CandlePatternDB.all().filter('type =', 'LONG').filter('date =', today).filter('market =', 'US').filter('pattern_name !=', 'Morning Star')
        short_patterns_candle = CandlePatternDB.all().filter('type =', 'SHORT').filter('date =', today).filter('market =', 'US')
        num_longs = long_patterns.count() + long_patterns_candle.count()
        num_shorts = short_patterns.count() + short_patterns_candle.count()
        logging.info("num long" + str(num_longs))
        logging.info("num shorts" + str(num_shorts))
        if num_longs != 0 or num_shorts != 0:
            stats = StatsDB()
            #for eastern time, subtract one 
            stats.date = today
            stats.num_longs = int(num_longs)
            stats.num_shorts = int(num_shorts)
            ratio = float(num_longs) / float(num_shorts)
            if ratio >= 3: num = 4
            elif 3 >= ratio >=2: num = 3
            elif 2 >= ratio >= 1.5: num = 2
            elif 1.5 >= ratio >= 1.05: num = 1
            elif 0.95 <= ratio <= 1.05: num = 0
            elif 0.667 <= ratio <= 0.95: num = -1
            elif 0.5 <= ratio <= 0.667: num = -2 
            elif 0.333 <= ratio <= 0.5: num = -3
            elif ratio <= 0.333: num = -4
            if num > 0: 
                trend = "Uptrend"
            elif num < 0:
                trend = "Downtrend"
            else:
                trend = "Neutral" 
            stats.degree = num
            stats.trend = trend
            stats.ratio = float(ratio)
            stats.market = "US"
            logging.info("degree" + str(stats.degree))
            logging.info("trend" + str(stats.trend))
            stats.put()
    
    def get(self):
 
        user = users.get_current_user()
        if user.email() == "peterchen16@gmail.com" or user.email() == "admin@w-stocks.com":       
            html = template.render('templates/upload_file.html', {})
            self.response.write(html)
            
    def post(self):
        user = users.get_current_user()
        if user.email() == "peterchen16@gmail.com" or user.email() == "admin@w-stocks.com": 
            logging.info("start")
            for file_data in self.request.POST.getall('pattern_file[]'):
                logging.info(file_data.filename)
                results = file_data.value.split('\n')
                for result in results: 
                    if result == "":
                        break
                    else:
                        if file_data.filename.find('Long') != -1:
                            type = "long"
                        else: 
                            type = "short"
                        logging.info(str(result))
                        result = result.split(' ')
                        symbol = result[0].upper()
                        volumn = result[1]
                        if int(volumn) < 1000000: volumn_range = "<1M"
                        if 1000000 <= int(volumn) <= 2000000: volumn_range = "1M-2M"
                        if 2000000 <= int(volumn) <= 3000000: volumn_range = "2M-3M"
                        if 3000000 <= int(volumn) <= 4000000: volumn_range = "3M-4M"
                        if 4000000 <= int(volumn) <= 5000000: volumn_range = "4M-5M"
                        if 5000000 <= int(volumn) <= 6000000: volumn_range = "5M-6M"
                        if 6000000 <= int(volumn) <= 7000000: volumn_range = "6M-7M"
                        if 7000000 <= int(volumn) <= 8000000: volumn_range = "8M-9M"
                        if 9000000 <= int(volumn) <= 10000000: volumn_range = "9M-10M"
                        if int(volumn) > 10000000: volumn_range = ">10M"
                        price = result[2]
                        if float(price) < 5.0: price_range = "<5"
                        if 5.0 <= float(price) <= 10.0: price_range = "5-10"
                        if 10.0 <= float(price) <= 20.0: price_range = "10-20"
                        if 20.0 <= float(price) <= 30.0: price_range = "20-30"
                        if 30.0 <= float(price) <= 40.0: price_range = "30-40"
                        if 40.0 <= float(price) <= 50.0: price_range = "40-50"
                        if 50.0 <= float(price) <= 100.0: price_range = "50-100"
                        if 100.0 <= float(price) <= 200.0: price_range = "100-200"
                        if 200.0 <= float(price) <= 300.0: price_range = "200-300"
                        if 300.0 <= float(price) <= 400.0: price_range = "300-400"
                        if 400.0 <= float(price) <= 500.0: price_range = "400-500"
                        if float(price) > 500.0: price_range = ">500"
                        #for eastern US time, collects data at 9pm eastern time which is 2am UTC time next day
                        day = date.today() - timedelta(days=1)
                        pattern = PatternDB()
                        pattern.pattern_name = file_data.filename.split("_")[0]
                        pattern.type = type.upper()
                        pattern.symbol = symbol.upper()
                        pattern.volumn = int(volumn)
                        pattern.volumn_range = volumn_range
                        pattern.price = float(price)
                        pattern.price_range = price_range
                        pattern.date = day
                        pattern.market = "US"
                        pattern.put()
            for file_data in self.request.POST.getall('candle_file[]'):
                logging.info(file_data.filename)
                results = file_data.value.split('\n')
                for result in results: 
                    if result == "":
                        break
                    else:
                        if file_data.filename.find('Long') != -1:
                            type = "long"
                        else: 
                            type = "short"
                        logging.info(str(result))
                        result = result.split(' ')
                        symbol = result[0].upper()
                        volumn = result[1]
                        if int(volumn) < 1000000: volumn_range = "<1M"
                        if 1000000 <= int(volumn) <= 2000000: volumn_range = "1M-2M"
                        if 2000000 <= int(volumn) <= 3000000: volumn_range = "2M-3M"
                        if 3000000 <= int(volumn) <= 4000000: volumn_range = "3M-4M"
                        if 4000000 <= int(volumn) <= 5000000: volumn_range = "4M-5M"
                        if 5000000 <= int(volumn) <= 6000000: volumn_range = "5M-6M"
                        if 6000000 <= int(volumn) <= 7000000: volumn_range = "6M-7M"
                        if 7000000 <= int(volumn) <= 8000000: volumn_range = "8M-9M"
                        if 9000000 <= int(volumn) <= 10000000: volumn_range = "9M-10M"
                        if int(volumn) > 10000000: volumn_range = ">10M"
                        price = result[2]
                        if float(price) < 5.0: price_range = "<5"
                        if 5.0 <= float(price) <= 10.0: price_range = "5-10"
                        if 10.0 <= float(price) <= 20.0: price_range = "10-20"
                        if 20.0 <= float(price) <= 30.0: price_range = "20-30"
                        if 30.0 <= float(price) <= 40.0: price_range = "30-40"
                        if 40.0 <= float(price) <= 50.0: price_range = "40-50"
                        if 50.0 <= float(price) <= 100.0: price_range = "50-100"
                        if 100.0 <= float(price) <= 200.0: price_range = "100-200"
                        if 200.0 <= float(price) <= 300.0: price_range = "200-300"
                        if 300.0 <= float(price) <= 400.0: price_range = "300-400"
                        if 400.0 <= float(price) <= 500.0: price_range = "400-500"
                        if float(price) > 500.0: price_range = ">500"
                        day = date.today() - timedelta(days=1)
                        pattern = CandlePatternDB()
                        pattern.pattern_name = file_data.filename.split("_")[0]
                        pattern.type = type.upper()
                        pattern.symbol = symbol.upper()
                        pattern.volumn = int(volumn)
                        pattern.volumn_range = volumn_range
                        pattern.price = float(price)
                        pattern.price_range = price_range
                        pattern.date = day
                        pattern.market = "US"
                        pattern.put()
            
config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'wreck-it-ralph', 'session_max_age': 3600}

app = webapp2.WSGIApplication([
    ('/sign_out', SignOut),
    ('/skeleton', Skeleton),
    ('/login', SignIn),
    ('/sign_up', SignUp),
    ('/verify', Verify),
    ('/fyi', FYI),
    ('/disclaimer', Disclaimer),
    ('/plain_disclaimer', PlainDisclaimer),
    ('/request', Request),
    ('/privacy_statement', PrivacyStatement),
    ('/about_us', AboutUs),
    ('/chat', Chat),
    ('/historical_trendicator', HistoricalTrendicator),
    ('/default_browser', DetectBrowser),
    ('/contact_us', ContactUs),
    ('/classroom', Classroom),
    ('/new_patterns', NewPatterns),
    ('/past_patterns', PastPatterns),
    ('/search_patterns', SearchPatterns),
    ('/candle_patterns', CandlePatterns),
    ('/my_account', UserAccount),
    ('/upload_file', UploadFile),
    ('/renew_subscriptions_everyday', RenewSubscriptions),
    ('/change_stat', ChangeStats),
    ('/generate_stat', GenerateStats),
    ('/load_daily_price', LoadPrice),
    ('/generate_chart', GenerateChart),
    ('/', MainHandler),
], config=config, debug=True)
        