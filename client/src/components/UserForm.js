import React, { Component } from 'react';

import { Select, Input, Label, Form, Button } from "../common";

class UserForm extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }
    render() {
        const { options, no_of_ticket, name, email_address, mobile_number, registration_type, disableNoOfTickets } = this.props.userData;
        const handleChange = this.props.onChange;
        return (
            <Form onSubmit={this.props.onSubmit}>
                <Input id="name" name="name" type="text" placeholder="Name" value={name} onChange={handleChange} required={true}></Input>
                <Input id="emailAddress" name="email_address" type="email" value={email_address} placeholder="Email Address" onChange={handleChange} required={true}></Input>
                <Input id="mobileNumber" name="mobile_number" type="tel" value={mobile_number} placeholder="Mobile Number" onChange={handleChange} required={true}></Input>
                <Input id="noOfticket" name="no_of_ticket" type="number" value={no_of_ticket} onChange={handleChange} placeholder="No Of Tickets" disabled={disableNoOfTickets} required={true}></Input>
                <Input id="idCard" name="id_card_local_path" type="file" accept='image/*' onChange={handleChange} required={true}></Input>
                <Select label='Registration Type:' options={options} id="registrationType" name="registration_type" value={registration_type} required={true} onChange={handleChange} displayname="Registration Type" />
                <Button type="submit">Confirm</Button>
            </Form>
        );
    }
}

export default UserForm;