import React, { Component } from 'react';


import { Helmet } from "react-helmet";

import UserForm from "./UserForm";

class Registraion extends Component {
    render() {
        return (
            <div>
                <Helmet>
                    <title>Registration</title>
                </Helmet>
                <UserForm></UserForm>
            </div>

        )
    }
}

export default Registraion;