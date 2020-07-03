import React, { Component } from 'react';



class Input extends Component {
    render() {
        const { type, placeholder, id, name, required, disabled, onChange, value, children, accept } = this.props;
        return (
            <div>
                <input type={type} placeholder={placeholder} accept={accept} id={id} name={name} value={value} required={required} disabled={disabled} onChange={onChange}>{children}</input>
            </div>
        )
    }
}

export default Input;