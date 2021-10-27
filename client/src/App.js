import React, {Component} from 'react';
import {Route,BrowserRouter,Switch,Redirect} from 'react-router-dom';

import Register from './pages/Register';
import Login from './pages/Login';
import HomePage from './pages/HomePage';
import Inbox from './pages/Inbox';
import NavBar from './components/NavBar';

class App extends Component {
  render () {
      return (
        <><div>
          <NavBar />
        </div>
        <BrowserRouter>
            <Switch>
              <Route exact path="/"><Redirect to="/home"/></Route>
              <Route exact path="/register" component={Register} />
              <Route exact path="/login" component={Login} />
              <Route exact path="/home" component={HomePage} />
              <Route exact path="/inbox" component={Inbox} />
              <Route exact path="/friends" component={HomePage}/>
            </Switch>
          </BrowserRouter></>
    );
  }
}

export default App;
