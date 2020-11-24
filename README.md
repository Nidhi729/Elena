# Elena

Elevation-based Navigation (EleNa) is an application that, given a start and end location, computes a route that maximizes or minimizes the elevation gain and limits the total distance between the locations to x% of the shortest path. 

Maximizing the elevation gain could be useful to joggers/bikers who may be looking for an intense workout. On the other hand, minimizing the elevation gain could be useful for those who don't prefer steep climb in the the route.



# Architecture
![Alt text](files/FinalArchitecture.png?raw=true "Elena")

# Videos
Architecture  


<video width="320" height="240" controls>
	<source src="files/Elena_Architecture_DemoUI.mp4" type="video/mp4">
</video>

```
URL
```

Application Set-up + execution 

```
URL
```

# Installation
The following versions have been used for building and installing the dependencies
* Python 2.7
* npm 6.14.8


Create virtual environment ( This is an optional step, the application can be install using system level python as well)

```
(Optional)
Create a virtual environment : virtualenv virtualenvname
Activate virtual environment : source virtualenvname activate
```
Install dependencies / requirements 

```
pip install -r src/requirements.txt

npm install
```

# Build Application

Use the setup.py to build .whl file for the application

```
python setup.py bdist_wheel
```
Install .whl file

```
pip install dist/src-1.0.0-py2-none-any.whl
```

# Start Application

After installing the required dependencies and building the app server as mentioned above, follow the steps to start the server.


* The flask server server would start by on port ``8080``. Please make sure the port is free for use.



```
python src/App/ElenaApp.py

Configured osmnx
 * Serving Flask app "ElenaApp" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)



```
* npm server would start on port ``3000``. Please make sure the port is free for use

```
npm start
```
