import React, { Component } from 'react';


class PreviewLabel extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        const { name, value } = this.props;
        return (
            <div>
                <label>{name}</label>:<span>{value}</span>
            </div>
        );
    }
}

export default PreviewLabel;