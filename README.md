## PyData Meetup talk on [Bokeh](https://bokeh.pydata.org/en/latest/)
### April 2019

1. clone the repository:
```
git clone https://github.com/RhDm/pydata_bokeh.git
```
2. cd to `pydata_bokeh`

4. create a new python environment (very much recommended; you can also try it with Python 3.7):
```
virtualenv --python=python3.6 venv
```

5. activate the environment:
```
source venv/bin/activate
```

6. install packages:
```
pip install -r requirements.txt
```

7. **start jupyter:**
```
jupyter notebook
```
and open the `bokeh.ipynb` notebook


it is possible that the plots with interactions (sliders and buttons) will not work and Bokeh will complain, to fix it try executing:
```
export BOKEH_ALLOW_WS_ORIGIN=*
```
as an alternative, you can add this line to your `.bash_profile` for the permanent effect

8. **start Flask app:**
```
python flask_app.py
```
and open `http://127.0.0.1:5000/` in your browser

8. **start Bokeh server**

cd to `bokeh_server` and start the server:
```
python flask_bokeh_server.py
```
check the data at `http://localhost:5000/plot`

NB! this repository does not include the basic React app which accepts the data from the `bokeh_server` and creates the actual plot
please let me know if you want it to be included!
