import React, {Component} from 'react';
import {Route,BrowserRouter,Switch} from 'react-router-dom';

import Register from './pages/Register';
import Login from './pages/Login';
import HomePage from './pages/HomePage';

class App extends Component {
  render () {
      return (
      <BrowserRouter>
      
        <Switch>
          <Route exact path="/" component={Register} />
          <Route exact path="/login" component={Login} />
          <Route exact path="/home" component={HomePage} />
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
