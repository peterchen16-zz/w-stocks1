from google.appengine.ext import db

class UserDB(db.Model):
    
    name = db.StringProperty()
    password = db.StringProperty()
    email = db.EmailProperty()
    avatar = db.BlobProperty()
    joined_date_time = db.DateTimeProperty()
    paid = db.BooleanProperty()
    verified = db.BooleanProperty()
    verification_code = db.IntegerProperty()
    subscription_start = db.DateProperty()
    subscription_end = db.DateProperty()
    current_plan = db.StringProperty(default=None)
    customer_id = db.StringProperty()
    automatic_renew = db.BooleanProperty(default=False)
    trial_used = db.BooleanProperty(default=False)
    accept_disclaimer = db.BooleanProperty(default=False)
    
class TransactionDB(db.Model):

    date = db.DateProperty()
    plan = db.StringProperty()
    order_id = db.StringProperty()
    email = db.EmailProperty()
    price = db.FloatProperty()
    
class PatternDB(db.Model):
    
    date = db.DateProperty()
    symbol = db.StringProperty()
    type = db.StringProperty()
    price = db.FloatProperty()
    pattern_name = db.StringProperty()
    volumn = db.IntegerProperty()
    market = db.StringProperty()
    price_range = db.StringProperty()
    volumn_range = db.StringProperty()
    
class CandlePatternDB(db.Model):
    
    date = db.DateProperty()
    symbol = db.StringProperty()
    type = db.StringProperty()
    price = db.FloatProperty()
    pattern_name = db.StringProperty()
    volumn = db.IntegerProperty()
    market = db.StringProperty()
    price_range = db.StringProperty()
    volumn_range = db.StringProperty()
    
class PatternTypeDB(db.Model):
    
    name = db.StringProperty()
    num = db.IntegerProperty()
    
class CandlePatternTypeDB(db.Model):
    
    name = db.StringProperty()
    num = db.IntegerProperty()
    
class StatsDB(db.Model):
    
    total_num_longs = db.IntegerProperty()
    total_num_shorts = db.IntegerProperty()
    chart_pattern_long = db.IntegerProperty()
    chart_pattern_short = db.IntegerProperty()
    candle_pattern_long = db.IntegerProperty()
    candle_pattern_short = db.IntegerProperty()
    market = db.StringProperty()
    date = db.DateProperty()
    chart_ratio = db.FloatProperty()
    candle_ratio = db.FloatProperty()
    combined_ratio = db.FloatProperty()
    chart_degree = db.IntegerProperty()
    candle_degree = db.IntegerProperty()
    combined_degree = db.IntegerProperty()
    chart_trend = db.StringProperty()
    candle_trend = db.StringProperty()
    combined_trend = db.StringProperty()
    
class DailyPriceDB(db.Model):
    
    symbol = db.StringProperty()
    price_list = db.ListProperty(float)
    volume = db.IntegerProperty()
    date = db.DateProperty()
    
class TradingDiaryDB():
    
    email = db.EmailProperty()
    datetime = db.DateTimeProperty()
    text = db.StringProperty()
    image = db.BlobProperty()