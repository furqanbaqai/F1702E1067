
"""
Gaia::API engine for aristotle
https://github.com/furqanbaqai/F1702E1067

Distributed under GPLv3 license agreement. Please refere to link:
https://www.gnu.org/licenses/gpl-3.0.en.html for more details.

Pre-requisite:
pip install flask
pip install flask-httpauth
pip install pymysql

Authur: Muhammad Furqan Baqai [MFB]
Change History
[MFB:2018-04-05] Initial checkin

"""
# Global Imports
import os
import logging
from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from AflatunDB import AflatunDB
from flask_cors import CORS


logging.basicConfig(
    format='[%(asctime)s:%(name)s:%(process)d:%(lineno)d %(levelname)s] %(message)s', level=logging.INFO)
app = Flask(__name__)
CORS(app)
afaltunDB = AflatunDB()

# Endpoint for displaying summary of all top news
@app.route('/news/api/v1.0/topnews')
def getTopNews():
    # step#1: open a connection with mysql datbase server
    # return jsonify({'status' : 'done'})
    try:       
        output = afaltunDB.getTopNews()
        if output == None:
            abort(404)
        else:
            return output
    except ValueError:
        abort(404)
    except:        
         abort(500)


# Endpoint for displaying summary of all top news
@app.route('/news/api/v1.0/entities/<string:hashCode>')
def getEntities(hashCode):
    # step#1: open a connection with mysql datbase server
    # return jsonify({'status' : 'done'})
    try:
        output = afaltunDB.getEntities(hashCode)
        if output == None:
            abort(404)
        else:
            return output
    except ValueError:
        abort(404)
    except:
         abort(500)
    

#
# Error Handlers
# ------------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Records not found'}), 404)


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Unknown server error'}), 500)
# ------------------------------------------------------------------------------

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)



