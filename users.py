import logging
import wsgiref.handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users, mail
from datetime import date, timedelta
import random
import webapp2


from db_models import *
from sessions import *
import stripe


class UserAccount(BaseHandler):
    
    def get(self):
        
        user = self.current_user()
        if user:
            transactions = TransactionDB().all().filter('email =', user.email).order("-date")
            html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions})
            self.response.write(html)
        else:
            self.redirect('/')
    
    def post(self):
        
        user = self.current_user()
        transaction = TransactionDB()
        transactions = TransactionDB().all().filter('email =', user.email).order("-date")
        if user:
            action = self.request.get('action')
            if user.accept_disclaimer == True:
                logging.info("accept disclaimer")
                if action == "1w":
                    logging.info("1w")
                    # Set your secret key: remember to change this to your live secret key in production
                    # See your keys here https://manage.stripe.com/account
                    stripe.api_key = "sk_live_dwY0WcfeSXVlmXLobOqwnX24"
                    # Get the credit card details submitted by the form
                    token = self.request.POST['stripeToken']
                    try:
                        # Create a Customer
                        customer = stripe.Customer.create(
                          card=token,
                          email=str(user.email)
                        )
                        charge = stripe.Charge.create(
                            amount=700, # in cents
                            currency="usd",
                            customer=customer.id
                        )
                        transaction.order_id = charge.id
                        transaction.date = date.today()
                        transaction.email = user.email
                        transaction.plan = "One Week Plan"
                        transaction.price = 7.00
                        transaction.put()
                        logging.info(str(customer.id))
                        user.customer_id = customer.id #this will be the newest customer id with the newest credit card info
                        if user.subscription_end != None:
                            if date.today() > user.subscription_end:
                                user.subscription_start = date.today()
                                user.subscription_end = date.today() + timedelta(days=7)
                            else:
                                user.subscription_end = user.subscription_end + timedelta(days=7)
                        else:
                            user.subscription_start = date.today()
                            user.subscription_end = date.today() + timedelta(days=7)
                        user.paid = True
                        user.current_plan = "1W"
                        user.put()
                        message = "Thank you for subscribing to the 1 Week Plan " + str(user.name) + "!"
                        transactions = TransactionDB().all().filter('email =', user.email).order("-date")
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                    except stripe.CardError:
                        logging.info("card error")
                        message = "Sorry, your card was declined. Please use another card."
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                    except stripe.APIError:
                        logging.info("api error")
                        message = "Sorry, Our Server is experiencing some difficulties, please try again in 5 minutes."
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                    
                if action == "1m":
                    logging.info("1m")
                    # Set your secret key: remember to change this to your live secret key in production
                    # See your keys here https://manage.stripe.com/account
                    stripe.api_key = "sk_live_dwY0WcfeSXVlmXLobOqwnX24"
                    # Get the credit card details submitted by the form
                    token = self.request.POST['stripeToken']
                    try:
                        # Create a Customer
                        customer = stripe.Customer.create(
                          card=token,
                          email=str(user.email)
                        )
                        charge = stripe.Charge.create(
                            amount=1700, # in cents
                            currency="usd",
                            customer=customer.id
                        )
                        transaction.order_id = charge.id
                        transaction.date = date.today()
                        transaction.email = user.email
                        transaction.plan = "One Month Plan"
                        transaction.price = 17.00
                        transaction.put()
                        logging.info(str(customer.id))
                        user.customer_id = customer.id #this will be the newest customer id with the newest credit card info
                        if user.subscription_end != None:
                            if date.today() > user.subscription_end:
                                user.subscription_start = date.today()
                                user.subscription_end = date.today() + timedelta(days=31)
                            else:
                                user.subscription_end = user.subscription_end + timedelta(days=31)
                        else:
                            user.subscription_start = date.today()
                            user.subscription_end = date.today() + timedelta(days=31)
                        user.paid = True
                        user.current_plan = "1M"
                        user.put()
                        message = "Thank you for subscribing to the 1 Month Plan " + str(user.name) + "!"
                        transactions = TransactionDB().all().filter('email =', user.email).order("-date")
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                    except stripe.CardError:
                        logging.info("card error")
                        message = "Sorry, your card was declined. Please use another card."
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                    except stripe.APIError:
                        logging.info("api error")
                        message = "Sorry, Our Server is experiencing some difficulties, please try again in 5 minutes."
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                    
                if action == "1y":
                    logging.info("1y")
                    # Set your secret key: remember to change this to your live secret key in production
                    # See your keys here https://manage.stripe.com/account
                    stripe.api_key = "sk_live_dwY0WcfeSXVlmXLobOqwnX24"
                    # Get the credit card details submitted by the form
                    token = self.request.POST['stripeToken']
                    try:
                        # Create a Customer
                        customer = stripe.Customer.create(
                          card=token,
                          email=str(user.email)
                        )
                        charge = stripe.Charge.create(
                            amount=10000, # in cents
                            currency="usd",
                            customer=customer.id
                        )
                        transaction.order_id = charge.id
                        transaction.date = date.today()
                        transaction.email = user.email
                        transaction.plan = "One Year Plan"
                        transaction.price = 100.00
                        transaction.put()
                        logging.info(str(customer.id))
                        user.customer_id = customer.id #this will be the newest customer id with the newest credit card info
                        if user.subscription_end != None:
                            if date.today() > user.subscription_end:
                                user.subscription_start = date.today()
                                user.subscription_end = date.today() + timedelta(days=366)
                            else:
                                user.subscription_end = user.subscription_end + timedelta(days=366)
                        else:
                            user.subscription_start = date.today()
                            user.subscription_end = date.today() + timedelta(days=366)
                        user.paid = True
                        user.current_plan = "1Y"
                        user.put()
                        message = "Thank you for subscribing to the 1 Year Plan " + str(user.name) + "!"
                        transactions = TransactionDB().all().filter('email =', user.email).order("-date")
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                    except stripe.CardError:
                        logging.info("card error")
                        message = "Sorry, your card was declined. Please use another card."
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                    except stripe.APIError:
                        logging.info("api error")
                        message = "Sorry, Our Server is experiencing some difficulties, please try again in 5 minutes."
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                if action == "change_name":
                    logging.info('change name')
                    new_name = self.request.get('new_name')
                    user.name = new_name
                    user.put()
                    message = "You have changed your name, " + str(user.name) + "."
                    html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                    self.response.write(html)
                if action == "change_password":
                    new_password = self.request.get('new_password')
                    user.password = new_password
                    user.put()
                    message = "You have changed your password, " + str(user.name) + "."
                    html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                    self.response.write(html)
                if action == "start_trial":
                    logging.info("start trial")
                    if user.trial_used == False:
                        user.trial_used = True
                        user.paid = True
                        user.put()
                        if user.subscription_end != None:
                            user.subscription_end = user.subscription_end + timedelta(days=7)
                        else:
                            user.subscription_start = date.today()
                            user.subscription_end = date.today() + timedelta(days=7)
                        message = "You have started your 7 days trial, " + str(user.name) + ". Enjoy!"
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                    else:
                        message = "You have used/are using your 7 days trial. Please select one of the following plans to continue enjoying our service."
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                if action == "auto_renew":
                    value = self.request.get('auto_renew')
                    logging.info(str(value))
                    if value == "on":
                        user.automatic_renew = True
                        user.put()
                        message = "You have turned on automatic renew for your latest plan, " + str(user.name) + "!"
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                    else:
                        user.automatic_renew = False
                        user.put()
                        message = "You have turned off automatic renew for your latest plan, " + str(user.name) + "!"
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                if action == "renew_plan":
                    stripe.api_key = "sk_live_dwY0WcfeSXVlmXLobOqwnX24"
                    if user.current_plan == None:
                        message = "You currently have no plan to renew. Please select one of the plans below"
                        html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                        self.response.write(html)
                    else:
                        if user.current_plan == '1W':
                            price = 700
                        elif user.current_plan == '1M':
                            price = 1700
                        elif user.current_plan == '1Y':
                            price = 10000
                        try:
                            charge = stripe.Charge.create(
                                amount=price, # in cents
                                currency="usd",
                                customer=user.customer_id
                            )
                            transaction.order_id = charge.id
                            transaction.date = date.today()
                            transaction.email = user.email
                            if user.current_plan == '1W':
                                transaction.plan = "One Week Plan"
                                transaction.price = 7.00
                                if user.subscription_end != None:
                                    if date.today() > user.subscription_end:
                                        user.subscription_start = date.today()
                                        user.subscription_end = date.today() + timedelta(days=7)
                                    else:
                                        user.subscription_end = user.subscription_end + timedelta(days=7)
                                else:
                                    user.subscription_start = date.today()
                                    user.subscription_end = date.today() + timedelta(days=7)
                            elif user.current_plan == '1M':
                                transaction.plan = "One Month Plan"
                                transaction.price = 17.00
                                if user.subscription_end != None:
                                    if date.today() > user.subscription_end:
                                        user.subscription_start = date.today()
                                        user.subscription_end = date.today() + timedelta(days=31)
                                    else:
                                        user.subscription_end = user.subscription_end + timedelta(days=31)
                                else:
                                    user.subscription_start = date.today()
                                    user.subscription_end = date.today() + timedelta(days=31)
                            elif user.current_plan == '1Y':
                                transaction.plan = "One Year Plan"
                                transaction.price = 100.00
                                if user.subscription_end != None:
                                    if date.today() > user.subscription_end:
                                        user.subscription_start = date.today()
                                        user.subscription_end = date.today() + timedelta(days=366)
                                    else:
                                        user.subscription_end = user.subscription_end + timedelta(days=366)
                                else:
                                    user.subscription_start = date.today()
                                    user.subscription_end = date.today() + timedelta(days=366)
                            user.put()
                            transaction.put()
                            logging.info(str(charge.id))
                            message = "Thank You. You have renewed your latest plan, " + str(user.name) + "."
                            transactions = TransactionDB().all().filter('email =', user.email).order("-date")
                            html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                            self.response.write(html)
                        except stripe.CardError:
                            logging.info("card error")
                            message = "Sorry, your old card was declined. Please use another card and select one of the plans below."
                            html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                            self.response.write(html)
                        except stripe.APIError:
                            logging.info("api error")
                            message = "Sorry, Our Server is experiencing some difficulties, please try again in 5 minutes."
                            html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                            self.response.write(html)
            else:
                if action == "accept_disclaimer":
                    logging.info("accept disclaimer")
                    user.accept_disclaimer = True
                    user.put()
                    message = "Welcome to your account page, and thank you for accepting our disclaimer, " +  str(user.name) + "!"
                    html = template.render('templates/my_account.html', {'user':user, 'transactions':transactions, 'message':message})
                    self.response.write(html)
                else:
                    html = template.render('templates/my_account.html', {'user':user})
                    self.response.write(html)
        else:
            self.redirect('/')
           
    
class SignIn(BaseHandler):
    
    def get(self):
        
        google_login = "www.google.com/accounts/o8/id"
        yahoo_login = "yahoo.com"
        google_login_url = users.create_login_url(federated_identity=google_login)
        yahoo_login_url = users.create_login_url(federated_identity=yahoo_login)
        html = template.render('templates/signin.html', {'user': False, 'gmail_login': google_login_url, 'yahoo_login': yahoo_login_url})
        self.response.write(html)
    
    def post(self):
        
        email = self.request.get('email')
        password = self.request.get('password')
        if email.find('@') == -1:
            email_message = "Incorrect Email Format, Please input something like example@example.com"
            html = template.render('templates/signin.html', {'email_message':email_message})
            self.response.write(html)
        else:
            user_exist = UserDB.all().filter('email =', email).filter('verified =', True).fetch(1)
            if user_exist == []:
                web_message = "Your email is either not registered or not verified. Please register or verify your email first."
                html = template.render('templates/signin.html', {'web_message':web_message})
                self.response.write(html)
            else:
                if user_exist[0].password == password:
                    self.session['user_key'] = str(user_exist[0].key())
                    logging.info(str(self.session['user_key']))
                    self.redirect('/')
                else:
                    password_message = "Your password is incorrect."
                    html = template.render('templates/signin.html', {'password_message':password_message})
                    self.response.write(html)
                    
class SignOut(BaseHandler):
    
    def get(self):
        
        logging.info("sign out")
        user = users.get_current_user()
        self.session.clear()
        if user:
            logout_url = users.create_logout_url('/')
            html = template.render('templates/logout.html', {'logout_url': logout_url})
            self.response.write(html)
        else:
            self.redirect('/')

class SignUp(webapp2.RequestHandler):
    
    def get(self):
        google_login = "www.google.com/accounts/o8/id"
        yahoo_login = "yahoo.com"
        google_login_url = users.create_login_url(federated_identity=google_login)
        yahoo_login_url = users.create_login_url(federated_identity=yahoo_login)
        html = template.render('templates/signup.html', {'user': False, 'gmail_login': google_login_url, 'yahoo_login': yahoo_login_url})
        self.response.write(html)

    def post(self):
        new_user = UserDB()
        name = self.request.get('name')
        password = self.request.get('password')
        email = self.request.get('email')
        if email.find('@') == -1:
            email_message = "Incorrect Email Format, Please input something like example@example.com"
            html = template.render('templates/signup.html', {'email_message':email_message})
            self.response.write(html)
        else:
            #user_db = UserDB.all().filter('email =', email)
            user_exist = UserDB.all().filter('email =', email).filter('verified =', True).fetch(1)
            #user_exist = db.GqlQuery("Select * from UserDB where email = :1 and verified = :2", str(email), True)
            logging.info(str(user_exist))
            user_pending = UserDB.all().filter('email =', email).filter('verified =', False).fetch(1)
            #user_pending = db.GqlQuery("Select * from UserDB where email = :1 and verified = :2", str(email), False)
            logging.info(str(user_pending))
            if user_exist != []:
                email_message = "Email already exist. Please contact admin to reset password."
                html = template.render('templates/signup.html', {'email_message':email_message})
                self.response.write(html)
            elif user_pending != []:
                email_message = "Please check your email for verification email and verify your account within 24 hours."
                html = template.render('templates/signup.html', {'email_message':email_message})
                self.response.write(html)
            else:
                verification_code = random.randrange(1, 100000000)
                new_user.email = email
                new_user.password = password
                new_user.name = name
                new_user.verification_code = verification_code
                new_user.verified = False
                new_user.paid = False
                new_user.joined_date_time = datetime.utcnow()
                new_user.put()
                web_message = "Your verification code is sent to your email inbox, please verify your account within 24 hours. Thank You"
                html1 = template.render('templates/signup.html', {'web_message':web_message})
                verification_link = "www.w-stocks.com/verify?email=" + str(email)
                email_message = "Your verification code is " + str(verification_code) + ". Your password is " + str(password) + ". Please click this link to activate your account " + verification_link
                html2 = template.render('templates/verify_email.html', {'email_message':email_message})
                email_list = ["<" + str(email) + ">"]
                subject_line = "W-Stocks Community Verification Code"
                mail.send_mail(sender="W-Stocks <admin@w-stocks.com>", to=email_list, subject=subject_line, body=html2, html=html2)
                self.response.write(html1)

class Verify(BaseHandler):
    
    def get(self):
        
        email = self.request.get('email')
        user = UserDB.all().filter('email =', email).fetch(1)
        if user == None:
            email_message = "No Such Email in Database. "
            html = template.render('templates/verify.html', {'email_message':email_message})
            self.response.write(html)
        else:
            html = template.render('templates/verify.html', {'email':email})
            self.response.write(html)
    
    def post(self):
        
        email = self.request.get('email')
        password = self.request.get('password')
        verification_code = self.request.get('verification code')
        user = UserDB.all().filter('email =', email).fetch(1)
        logging.info(email)
        if user[0].password != password or str(user[0].verification_code) != verification_code:
            logging.info("here")
            logging.info(password)
            logging.info(verification_code)
            message = "Your verification code and password did not match your record in database. Please try or register again after 24 hours or register with a different email. Thank You. "
            html = template.render('templates/verify.html', {'web_message': message})
            self.response.write(html)
        else:
            user[0].verified = True
            user[0].put()
            #sets the session for user
            self.session['user_key'] = str(user[0].key())
            #logging.info(str(self.session['user']))
            self.redirect('/new_patterns')
            