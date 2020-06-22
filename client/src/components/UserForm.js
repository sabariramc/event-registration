import React, { Component } from 'react';

import { Form, Grid } from "semantic-ui-react";

import { Select } from "../common";


class UserForm extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <Form>
                <Form.Input id="fullname" name="full_name" type="text" placeholder="Full Name" required></Form.Input>
                <Form.Input id="mobilenumber" name="mobile_number" placeholder="Mobile Number" required></Form.Input>
                <Form.Input id="emailaddress" name="email_address" type="email" placeholder="Email Address" required></Form.Input>
                <Form.Input id="registrationtype" name="registration_type" required></Form.Input>
                <Form.Input id="noOfTickets" name="no_of_ticket" placeholder="No Of Tickets" required></Form.Input>
                <Form.Input id="idCard" name="id_card_file" type="file" accept='image/*' required></Form.Input>
                <Form.Field>
                    <Select id="registrationType" name="registration_type" required={true} displayname="Registration Type" />
                </Form.Field>
                <Form.Button type="submit">Register</Form.Button>
            </Form>
        )
    }
};

export default UserForm;