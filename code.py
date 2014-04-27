#encoding:utf-8
#import os
#os.path.join (os.path.dirname(os.path.abspath(__file__)))

import web

import urls

urls = urls.urls

web.config.debug = False

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'))
    web.config._session = session
else:
    session = web.config._session

def session_hook():
    web.ctx.session = session
app.add_processor(web.loadhook(session_hook))

if __name__ == "__main__":
    app.run()