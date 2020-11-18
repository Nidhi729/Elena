import React from 'react';
import L from 'leaflet';
import Routing from 'leaflet-routing-machine';

export default class DisplayMap extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state =
        {
          renderRoute: false,
          mapCenter: [42.37, -72.51],   // Amherst Town Common
        };
    }

    componentWillReceiveProps(props)
    {
        var route = props["route"];
        this.setState(
        {
          renderRoute: true,
          mapCenter: route[0],
          route: route,
        });
    }

    GenerateMap()
    {
        var mapObj = L.map('map',
        {
          center: this.state.mapCenter,
          zoom: 14,
          layers: [
            L.tileLayer("https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png")
          ]
        });
        this.initMarker = L.marker(this.state.mapCenter)
        return mapObj;
    }

    setPath(mapObj)
    {
        this.routingControl = L.Routing.control({itineraryClassName: "routing-directions"});
        this.routingControl.addTo(mapObj);
        this.routingControl.hide();
    }

    componentDidMount()
    {
        this.mapObj = this.GenerateMap();
        this.setPath(this.mapObj)
    }

    reduceWaypoints()
    {
        var markers = this.state.route.map(coordinates => {
            return L.latLng(coordinates[0], coordinates[1])
          });
        var reducedMarkers = markers.filter(function(value, index, arr)
        {
           return index % 7 === 0;
        });
        return reducedMarkers
    }

    render()
    {
        if(this.state.renderRoute)
        {
          this.mapObj.removeLayer(this.initMarker);
          var reducedMarkers = this.reduceWaypoints();
          this.routingControl.getPlan().setWaypoints(reducedMarkers);
          var midX = this.state.route[0][0]+this.state.route[this.state.route.length-1][0]/2
          var midY = this.state.route[0][1]+this.state.route[this.state.route.length-1][1]/2
          this.mapObj.panTo(new L.LatLng(midX, midY));
        } else {
        }

        return (
          <div id="map"></div>
        );
    }
}
