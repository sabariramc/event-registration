import React, { Component } from 'react';

class Select extends Component {
    constructor(props) {
        super(props)
        this.state = { options: [] }
    }

    componentDidMount() {
        this.setState({ options: [{ key: "SELF", name: "Self" }] })
    }

    render() {
        const { options } = this.state;
        const { id, name, disbled, displayname } = this.props
        return (
            <>
                <label for={id}>{displayname}</label>
                <select id={id} name={name} disbled={disbled}>
                    {
                        options.map(option => (
                            <option id={options.key}>{option.name}</option>
                        ),
                        )
                    }
                </select>
            </>
        );
    }
}

export default Select;