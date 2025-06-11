# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 15:23:13 2020

@author: roysoumy
"""




from flaskblog import app as application
#from flaskblog import app

if __name__ == "__main__":
    application.run(debug = True)

#app.run(debug = True)


#gunicorn --bind 0.0.0.0:8000 run


##tmux new -s <session_name>
##tmux a -t <session_name>
### Ctrl + b  ..... d
###all tmux session here - tmux ls