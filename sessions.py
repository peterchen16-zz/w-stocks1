import webapp2
from webapp2_extras import sessions
from google.appengine.api import users
from datetime import datetime

from db_models import *


class BaseHandler(webapp2.RequestHandler):
    
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
 
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
 
    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
    
    def current_user(self):
        
        user_auth = users.get_current_user()
        user_login_key = self.session.get('user_key')
        
        if user_auth:
            user_db_verified = UserDB.all().filter('email =', user_auth.email()).filter('verified =', True).fetch(1)
            user_db_not_verified = UserDB.all().filter('email =', user_auth.email()).filter('verified =', False).fetch(1)
            if user_db_verified != []:
                return user_db_verified[0]
            elif user_db_not_verified != []:
                user_db_not_verified.verified = True
                user_db_not_verified.put()
                return user_db_not_verified[0]
            else:
                new_user = UserDB()
                new_user.email = user_auth.email()
                new_user.name = user_auth.nickname()
                new_user.joined_date_time = datetime.utcnow()
                new_user.paid = False
                new_user.verified = True
                new_user.put()
                return new_user
        elif user_login_key:
            user = db.get(user_login_key)
            return user
        else:
            return None
