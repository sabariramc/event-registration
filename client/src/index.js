import React, { Component } from 'react';
import ReactDOM from "react-dom";
import App from "./components/App";
import { hot } from "react-hot-loader/root";

import './index.css';

const render = (Component) => ReactDOM.render(<Component />, document.getElementById('container'));

render(hot(App))