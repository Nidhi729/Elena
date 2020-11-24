# EleNA : Elevation Based Navigation

Elevation-based Navigation (EleNa) is an application that, given a start and end location, computes a route that maximizes or minimizes the elevation gain and limits the total distance between the locations to x% of the shortest path. 

Maximizing the elevation gain could be useful to joggers/bikers who may be looking for an intense workout. On the other hand, minimizing the elevation gain could be useful for those who don't prefer steep climb in the the route.



# Architecture
![Alt text](files/FinalArchitecture.png?raw=true "Elena")


# UI
![Alt text](files/ElenaUI.png?raw=true "ElenaUI")

# Videos

Watch [ EleNA Architecture Explanation ](https://youtu.be/fBHZz_ati1U)


Watch [ EleNA Application Demo ](https://youtu.be/wjJv7FNBlyI)

#  Instructions for application setup and execution 

## How to install ?
The following versions have been used for building and installing the dependencies
* Python 2.7
* npm 6.14.8


Create virtual environment ( This is an optional step, the application can be install using system level python as well)

```
(Optional)
Create a virtual environment : virtualenv virtualenvname
Activate virtual environment : source virtualenvname activate
```
Install dependencies / requirements using the command

```
pip install -r src/requirements.txt

npm install
```

## How to build and install ?

Use the setup.py to build .whl file for the application. Build the application using the command

```
python setup.py bdist_wheel
```
Install the build file using the command

```
pip install dist/src-1.0.0-py2-none-any.whl
```

## How to run app ?

After installing the required dependencies and building the app server as mentioned above, follow the steps to start the server.


* The flask server server would start by on port ``8080``. Please make sure the port is free for use.
* Flask server URL ``http://127.0.0.1:8080/`` 
* Start the flask server using the command


```
python src/App/ElenaApp.py

```

* npm server would start on port ``3000``. Please make sure the port is free for use
* npm server URL : ``http://127.0.0.1:3000/``
* Start the npm server using the command

```
npm start
```
# Test Suites

Unit test have been added for our application.

Unit test location : `` src/TestFiles/UnitTest.py``

The following test suite have been included:
* Test Location is Valid
* Test Location is InValid
* Test For Path Elevation
* Test For Path Length
* Test For location coordinates
* Test Get Nearest Node in graph
* Test Djikstra Path Finding Algo
* Test A* Path Finding Algo
