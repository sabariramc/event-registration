import React, { Component } from 'react';

import { Form, Button } from "../common";

class UserForm extends Component {
    render() {
        const { no_of_ticket, name, email_address, mobile_number, registration_type, previewFile } = this.props.userData;

        return (
            <Form onSubmit={this.props.onSubmit}>
                <div>
                    <image src={previewFile} ></image>
                </div>
                <div>
                    <label>Name:</label><span>{name}</span>
                    <label>Email Address:</label><span>{email_address}</span>
                    <label>Mobile Number:</label><span>{mobile_number}</span>
                    <label>Registrataion Type:</label><span>{registration_type}</span>
                    <label>No of Tickets:</label><span>{no_of_ticket}</span>
                </div>
                <Button type="submit">Submit</Button>
            </Form>
        )
    }
};

export default UserForm;