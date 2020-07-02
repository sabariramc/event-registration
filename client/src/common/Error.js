import React, { Component } from 'react';

import './common.css'

class Error extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }
    render() {
        return (
            <div>
                <span className="errormessage">{this.props.children}</span>
            </div>
        );
    }
}

export default Error;