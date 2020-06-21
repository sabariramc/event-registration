import React, { Component } from 'react';

import { Form, Grid } from "semantic-ui-react";
import { Helmet } from "react-helmet";

class RegistrationType extends Component {
    constructor(props) {
        super(props)
        this.state = { options: [] }
    }

    componentDidMount() {
        this.setState({ options: [{ key: "SELF", name: "Self" }] })
    }

    render() {
        const { options } = this.state;
        const { id, name } = this.props
        return (
            <select id={id} name={name}>
                {
                    options.map(option => (
                        <option id={options.key}>{option.name}</option>
                    ),
                    )
                }
            </select>
        );
    }
}

class Registraion extends Component {
    render() {
        return (
            <div>
                <Helmet>
                    <title>Registration</title>
                </Helmet>
                <Form>
                    <input id="fullname" name="full_name" type="text" placeholder="Full Name" required></input>
                    <input id="mobilenumber" name="mobile_number" placeholder="Mobile Number" required></input>
                    <input id="emailaddress" name="email_address" type="email" placeholder="Email Address" required></input>
                    <input id="registrationtype" name="registration_type" required></input>
                    <input id="noOfTickets" name="no_of_ticket" placeholder="No Of Tickets" required></input>
                    <input id="idCard" name="id_card_file" type="file" accept='image/*' required></input>
                    <RegistrationType id="registrationType" name="registration_type" />
                    <button type="submit">Register</button>
                </Form>
            </div>

        )
    }
}

export default Registraion;