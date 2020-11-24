# Elena

Elevation-based Navigation (EleNa) is an application that, given a start and end locaton, computes a route that maximizes or minimizes the elevation gain and limits the total distance between the locations to x% of the shortest path. Maximizing the elevation gain could be useful to joggers/bikers who may be looking for an intense workout. On the other hand, minimizing the elevation gain could be useful for those who don't prefer steep climb in the the route.



# Architecture
![Alt text](FinalArchitecture.png?raw=true "Elena")

# Requirements
* Python 2.7
* npm

# Installation

Backend 
```
pip install requirements.txt
```

Frontend
```
npm install
```

# Build
```
python setup.py bdist_wheel
```
```
pip install dist/src-0.0.0-py2-none-any.whl
```

# Running
Backend
```
python src/App/ElenaApp.py
```
Frontend
```
npm start
```
