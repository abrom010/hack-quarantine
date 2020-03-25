import flask
application = flask.Flask(__name__)

 #WHEN URL IS http://nameofwebsite.com/ DO THIS
@application.route('/')
def main():
    return flask.render_template('index.html')
# ^^^ RETURNS index.html AFTER HAVING PROCESSED IT USING THE render_template() FUNCTION

#ONLY RUNS THE FLASK APPLICATION IF THE APP.PY IS BEING USED AS THE DRIVER
if __name__ == '__main__':
	application.run()
