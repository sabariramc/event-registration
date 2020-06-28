import React, { Component } from 'react';


import { Helmet } from "react-helmet";

import UserForm from "./UserForm";

class Registraion extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        console.log(event.target.value)
        
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>Registration</title>
                </Helmet>
                <UserForm onSubmit={this.handleSubmit} ></UserForm>
            </div>

        )
    }
}

export default Registraion;