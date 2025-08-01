import { Component } from 'react';
import axios from 'axios';
import Smartcar from '@smartcar/auth';

import Connect from './components/Connect';
import Vehicle from './components/Vehicle';
import AgentInsights from './components/AgentInsights';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      vehicle: {},
    };

    this.authorize = this.authorize.bind(this);
    this.onComplete = this.onComplete.bind(this);

    this.smartcar = new Smartcar({
      clientId: process.env.REACT_APP_CLIENT_ID,
      redirectUri: process.env.REACT_APP_REDIRECT_URI,
      scope: ['read_vehicle_info'],
      onComplete: this.onComplete,
      testMode: true,
    });
  }

  onComplete(err, code, state) {
    return axios
      .get(`${process.env.REACT_APP_SERVER}/exchange?code=${code}`)
      .then(() => {
        return axios.get(`${process.env.REACT_APP_SERVER}/vehicle`);
      })
      .then(res => {
        this.setState({ vehicle: res.data });
      });
  }

  authorize() {
    this.smartcar.openDialog({ forcePrompt: true });
  }

  render() {
    return Object.keys(this.state.vehicle).length !== 0 ? (
      <div>
        <Vehicle info={this.state.vehicle} />
        <AgentInsights />
      </div>
    ) : (
      <Connect onClick={this.authorize} />
    );
  }
}

export default App;
