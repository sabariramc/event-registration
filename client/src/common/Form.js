import React, { Component } from 'react';

class Form extends Component {
    render() {
        const { onSubmit } = this.props;
        return (
            <form onSubmit={onSubmit}>
                {this.props.children}
            </form>
        );
    }
}

export default Form;