import React, { Component } from 'react';

import { Form, Button, PreviewLabel } from "../common";

class UserForm extends Component {
    render() {
        const { no_of_ticket, name, email_address, mobile_number, registration_type, previewFile } = this.props.userData;

        return (
            <Form onSubmit={this.props.onSubmit}>
                <div>
                    <img src={previewFile} ></img>
                </div>
                <PreviewLabel name="Name" value={name} />
                <PreviewLabel name="Email Address" value={email_address} />
                <PreviewLabel name="Mobile Number" value={mobile_number} />
                <PreviewLabel name="Registrataion Type" value={registration_type} />
                <PreviewLabel name="No of Tickets" value={no_of_ticket} />
                <Button type="submit">Submit</Button>
            </Form>
        )
    }
};

export default UserForm;