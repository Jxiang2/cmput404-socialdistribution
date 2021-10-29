import React from "react";
import { Route, BrowserRouter, Switch } from "react-router-dom";

import Register from "./pages/Register";
import Login from "./pages/Login";
import Friends from "./pages/friends";

function App() {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/register" component={Register} />
        <Route exact path="/login" component={Login} />
        <Route exact path="/friends" component={Friends} />
      </Switch>
    </BrowserRouter>
  );
}

export default App;
