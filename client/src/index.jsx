import React, { Component } from 'react';
import ReactDOM from "react-dom";
import { hot } from "react-hot-loader/root";

class Home extends Component {
    render() {
        return (<h1>Hi</h1>);
    }
}

const render = (Component) => ReactDOM.render(<Home />, document.getElementById('container'));

render(hot(Home))