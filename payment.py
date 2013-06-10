import logging
from sessions import *
from datetime import date
from db_models import *
import stripe
import webapp2
from google.appengine.api import mail
from google.appengine.ext.webapp import template

class RenewSubscriptions(webapp2.RequestHandler):
    
    def get(self):
        
        today = date.today()
        users = UserDB.all().filter('subscription_end <', today)
        stripe.api_key = "sk_live_dwY0WcfeSXVlmXLobOqwnX24"
        for user in users:
            logging.info(str(user))
        for user in users:
            try:
                if user.current_plan != None:
                    if user.current_plan == '1W':
                        charge = stripe.Charge.create(
                            amount=700, # in cents
                            currency="usd",
                            customer=user.customer_id
                        )
                        price1 = 7.00
                        plan1 = "One Week Plan"
                    elif user.current_plan == '1M':
                        charge = stripe.Charge.create(
                            amount=1400, # in cents
                            currency="usd",
                            customer=user.customer_id
                        )
                        price1 = 14.00
                        plan1 = "One Month Plan"
                    elif user.current_plan == '1Y':
                        charge = stripe.Charge.create(
                            amount=10000, # in cents
                            currency="usd",
                            customer=user.customer_id
                        )
                        price1 = 100.00
                        plan1 = "One Year Plan"
                    transaction = TransactionDB(date=today, email=user.email, order_id=charge.id, plan=plan1, price=price1)
                    email_message = "Thank you for renewing your latest plan with W-stocks Community. Please visit your account page for more information.Your current plan is " + str(transaction.plan) + "." 
                    html = template.render('templates/renew_email.html', {'email_message':email_message})
                    email_list = ["<" + str(user.email) + ">"]
                    subject_line = "W-Stocks Community Plan Renewed"
                    mail.send_mail(sender="W-Stocks <admin@w-stocks.com>", to=email_list, subject=subject_line, body=html, html=html)
            except stripe.CardError:
                logging.info("card error")
                email_message = "Sorry, your card was declined while we were trying to renew your latest plan. Please go to your account page and re-enter your credit card by selecting the plan you want. If you have any questions regarding re-entering your card info or your plan, please don't hesitate to contact us. Thank you."
                html = template.render('templates/renew_email.html', {'email_message':email_message})
                self.response.write(html)
                user.paid = False
                user.put()
                continue
            except stripe.APIError:
                logging.info("api error")
                user.subscription_end = date.today()
                user.put()
                continue
                