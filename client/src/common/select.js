import React, { Component } from 'react';

import Label from './label';

class Select extends Component {

    render() {
        const { id, name, disabled, options, onChange, label } = this.props
        return (
            <div>
                <Label htmlFor={id} >{label}</Label>
                <select id={id} name={name} disabled={disabled} onChange={onChange}>
                    {
                        options.map(option => (
                            <option key={option.key}>{option.value}</option>
                        ),
                        )
                    }
                </select>
            </div>
        );
    }
}

export default Select;