import React from 'react';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import Button from '@material-ui/core/Button';
import DisplayMap from './DisplayMap';
import TextField from '@material-ui/core/TextField';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Slide from '@material-ui/core/Slide';
import Typography from '@material-ui/core/Typography';

const styles = theme => ({
  MainDisplay: {
    display: 'flex',
  },
  DrawerStyle: {
    position: 'relative',
    width: '20vw',
    backgroundColor: "#0b6b62",
    flexGrow: 1,
    height: '100vh',
    padding: 0,
    background: "#0b6b62"
  },
  MapOutput: {
    flexGrow: 1,
    height: '100vh',
    padding: 0,
    background: "#0b6b62"
  },
  SubmitButton: {
    //margin: '15%',
    position: 'relative',
    padding:  0,
    width: '25%',
    height: '5.2%',
    margin: '0 auto',
    background: "#bdb5bd",
    fontWeight: 'bold',
    marginTop: '20%',
    marginBottom: '10%',
    fontFamily: 'sans-serif',
    fontColor:"#0b6b62"
  },
  TextFieldStyle: {
    position: 'relative',
    marginLeft: '15%',
    marginRight: '15%',
    width: '80%',
    textAlign: 'center',
    marginTop: 30,
    color: "black",
    backgroundColor: "white",
    borderRadius:'16px',
    borderWidth: '5px',
    borderColor: 'black'

  },
  LabelStyle: {
     color : 'black',
     fontFamily: 'cursive'
  },
  OutlineStyle: {
    borderWidth: '5px',
    borderRadius: '16px',
    borderColor: 'black'
  },
  OutputBox: {
      height: 40,
      width: 1035,
      marginTop: 5,
      position: "absolute",
      float: "left",
      background: "black",
    },
    InitialOutputBox: {
      height: 40,
      width: 1035,
      marginTop: 5,
      position: "absolute",
      float: "left",
      background: "grey",
    },
    InitialTextStyle: {
      //fontSize: 16,
      float: "left",
      marginLeft: 300,
      marginTop: -10,
      color: "black",
      fontFamily: 'Arial Black',
      fontWeight:"bold",
      fontSize:"140%",
    },
    textStyle: {
      //fontSize: 16,
      float: "left",
      marginLeft: 20,
      marginTop: -5,
      color: "white",
      fontFamily: 'cursive',
      fontSize:"110%"
    },
    ImageStyle : {
      margin: "0 auto",
      height: "20%",
      width: "60%",
      color: "black",
  }
});

class DisplayUI extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      renderRoute: false
    }
  }

  render() {
    const { classes } = this.props;
    var displayMap;
    var OutputDisplay;

    if(this.state.renderRoute) {
      displayMap = <DisplayMap route={this.state.route}></DisplayMap>
      OutputDisplay = <Slide direction="right" in={true} mountOnEnter unmountOnExit timeout="1000">
            <Card className={classes.OutputBox}>
                <CardContent>
                <Typography className={classes.textStyle} gutterBottom>
                   We found the path !!! Travel a distance of {this.state.distanceMiles.toFixed(2)} miles and an elevation of {this.state.elevation} meters and a time of {this.state.time.toFixed(2)} mins
                </Typography>
                </CardContent>
            </Card>
        </Slide>
    } else {
      displayMap = <DisplayMap></DisplayMap>
      OutputDisplay = <Slide direction="right" in={true} mountOnEnter unmountOnExit timeout="1000">
            <Card className={classes.InitialOutputBox}>
                <CardContent>
                <Typography className={classes.InitialTextStyle} gutterBottom>
                   ELEVATION BASED NAVIGATOR
                </Typography>
                </CardContent>
            </Card>
        </Slide>
    }

    return (
      <div className={classes.MainDisplay}>
        <CssBaseline />
        <main className={classes.MapOutput}>
            {displayMap}
            {OutputDisplay}
        </main>
        <Drawer variant="permanent" classes={{paper: classNames(classes.DrawerStyle),}}>
          <img src={require('../Resources/EleNa-logo.png')} className={classes.ImageStyle} />
          <TextField
          id="origin"
          label="Enter Origin"
          className={classes.TextFieldStyle}
          variant="outlined"
          InputLabelProps={{
            classes: {
              root: classes.LabelStyle,
            },
          }}
          InputProps={{
            classes: {
               notchedOutline: classes.OutlineStyle,
            },
          }}
        />
        <TextField
          id="dest"
          label="Enter Destination"
          className={classes.TextFieldStyle}
          variant="outlined"
          InputLabelProps={{
            classes: {
              root: classes.LabelStyle,
            },
          }}
          InputProps={{
            classes: {
              notchedOutline: classes.OutlineStyle,
            },
          }}
        />

         <TextField
          id="min-max"
          label="Enter min/max"
          className={classes.TextFieldStyle}
          variant="outlined"
          InputLabelProps={{
            classes: {
              root: classes.LabelStyle,
            },
          }}
          InputProps={{
            classes: {
              notchedOutline: classes.OutlineStyle,
            },
          }}
        />

         <TextField
          id="percentage"
          label="Enter Percentage"
          className={classes.TextFieldStyle}
          variant="outlined"
          InputLabelProps={{
            classes: {
              root: classes.LabelStyle,
            },
          }}
          InputProps={{
            classes: {
              notchedOutline: classes.OutlineStyle,
            },
          }}
        />
          <Button variant="contained" className={classes.SubmitButton} onClick={() => { this.sendRequest() }}>
          <span>Submit</span>
          </Button>
        </Drawer>
      </div>
    ); }

    sendRequest() {
        const origin = document.getElementById('origin').value;
        const destination = document.getElementById('dest').value;
        const percentage = Number(document.getElementById('percentage').value);
        if(percentage>200 || percentage < 100){
            alert("please add proper percentage value!")
            return
        }
        const max_min = document.getElementById('min-max').value;
        if(max_min === "min" || max_min === "max"){ }
        else{
            alert("please enter min for Minimum Elevation and max for Maximum Elevation")
            return
        }
        fetch("http://localhost:8080/getRoute", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin':'*'
          },
          body: JSON.stringify({
            Source: origin,
            Destination: destination,
            Max_min: max_min,
            Percentage: percentage
          })
        })
        .then(res => res.json())
        .then(json => {
            this.setState({
              route: json["Route"],
              renderRoute: true,
              distance: json["Distance"],
              distanceMiles: json["Distance"]*0.00062,
              elevation: json["Elevation Gain"],
              elevationMiles: json["Elevation Gain"]*0.00062,
              time : (json["Distance"]*0.00062+ json["Elevation Gain"]*0.00062)*15,
            });
        });
    }
  }

export default withStyles(styles)(DisplayUI);
