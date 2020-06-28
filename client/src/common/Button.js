import React, { Component } from 'react';


class Button extends Component {
    render() {
        const { type, children } = this.props;
        return (
            <div>
                <button type={type}> {children} </button>
            </div>
        );
    }
}

export default Button;