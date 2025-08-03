import { Component } from 'react';
import Smartcar from '@smartcar/auth';
import Connect from './components/Connect';
import Dashboard from './components/Dashboard';
import { exchangeCode } from './api';

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
      scope: [
        'read_vehicle_info', 
        'read_location', 
        'read_odometer', 
        'read_tires', 
        'read_vin', 
        'read_engine_oil',
        'read_battery'
    ],
      onComplete: this.onComplete,
      testMode: true,
    });
  }

  onComplete(err, code, state) {
    exchangeCode(code).then(() => {
      this.setState({ vehicle: { connected: true } });
    });
  }

  authorize() {
    this.smartcar.openDialog({ forcePrompt: true });
  }

  render() {
    return this.state.vehicle.connected ? (
      <Dashboard />
    ) : (
      <Connect onClick={this.authorize} />
    );
  }
}

export default App;
