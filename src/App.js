import React, { Component } from "react";
import Manage from "./pages/views/Manage";
// import Welcome from "./pages/views/Welcome";
import { BrowserRouter, Route } from "react-router-dom";
// import NavBar from "./components/NavBar";
// import { DailyWeather, WeekWeather } from "./components/Weather";
// import Leaderboard from "./pages/views/Leaderboard";
// import Overview from "./pages/views/Overview";
import Weather from "./pages/views/WeatherView";

class App extends Component {
  state = {
    color: [],
    country: null,
    city: "",
    zip: null,
    timeZone: "",
    State: "",
    storeName: ""
  };

  setLocation = (city, country, zip, timeZone) => {
    this.setState({
      city: city,
      country: country,
      zip: zip,
      timeZone: timeZone
    });
  };

  setStore = (storeName, colorPattern) => {
    this.setState({
      storeName: storeName,
      color: colorPattern
    });
  };

  setColor = color => {
    this.setState({ color: color }, () => {});
  };

  render() {
    return (
      <BrowserRouter>
        <div className="App">
          <Route
            exact={true}
            path="/"
            render={() => (
              <div className="MangageScreen">
                <Manage
                  setLocation={this.setLocation}
                  setColor={this.setColor}
                  setStore={this.setStore}
                  {...this.state}
                />
              </div>
            )}
          />
          <Route
            exact={true}
            path="/weather"
            render={() => (
              <div className="Weather">
                <Weather
                  city={this.state.city}
                  country={this.state.country}
                  zip={this.state.zip}
                />
              </div>
            )}
          />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
