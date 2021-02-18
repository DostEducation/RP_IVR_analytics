from __future__ import absolute_import
from api import app
from api import views

# The routes will be going it's specific directory/files

# if __name__ =="__main__":
# app.run(debug=True);
app.run(host='0.0.0.0', debug=True, use_reloader=True)
