import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import importedComponent from "react-imported-component";


import Home from './Home';
import Registration from './Registraion';

class App extends Component {
    render() {
        return (
            <Router>
                <div>
                    <Switch>
                        <Route path="/registration" component={Registration}></Route>
                        <Route path="/" component={Home}></Route>
                    </Switch>
                </div>
            </Router>
        );
    }

};


export default App;