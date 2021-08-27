import './App.css';
import LoginForm from './components/Forms/LoginForm';
import RegistrationForm from './components/Forms/RegistrationForm';
import RegistrationSuccess from "./components/Forms/RegistrationSuccess";
import React from 'react';


import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import Dashboard from './components/Dashboard';


function App() {

  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact={true}>
            <LoginForm/>
          </Route>
          <Route path="/register">
            <RegistrationForm/>
          </Route>
          <Route path="/login">
            <LoginForm/>
          </Route>
          <Route path="/registerSuccess">
            <RegistrationSuccess/>
          </Route>
          <Route path="/dashboard">
            <Dashboard/>
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;

// "/" is for home
