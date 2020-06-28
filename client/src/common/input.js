import React, { Component } from 'react';



class Input extends Component {
    render() {
        const { type, placeholder, id, name, required, disabled, onChange, value, children } = this.props;
        return (
            <div>
                <input type={type} placeholder={placeholder} id={id} name={name} value={value} required={required} disabled={disabled} onChange={onChange}>{children}</input>
            </div>
        )
    }
}

export default Input;