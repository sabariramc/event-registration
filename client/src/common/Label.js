import React, { Component } from 'react';


class Label extends Component {
    render() {
        const { htmlFor, children } = this.props;
        return (
            <label htmlFor={htmlFor}>{children}</label>
        );
    }
}

export default Label;