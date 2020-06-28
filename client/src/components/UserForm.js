import React, { Component } from 'react';

import { Select, Input, Label, Form, Button } from "../common";

import { getData, postData, uploadFile } from "../services";


class UserForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            options: [], disableNoOfTickets: true, no_of_ticket: 1
            , name: ''
            , email_address: ''
            , mobile_number: ''
            , id_card_file: ''
            , id_card_local_path: ''
            , registration_type: 'Self'
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    componentDidMount() {
        getData('/registration/config', (data) => this.setState({ options: data }))
    }

    handleSubmit(e) {
        event.preventDefault();
        const { no_of_ticket, name, email_address, mobile_number, id_card_file, registration_type, options } = this.state;
        var submit_data = { no_of_ticket, name, email_address, mobile_number, id_card_file };
        for (var i in options) {
            if (options[i].value === registration_type) {
                submit_data['registration_type'] = options[i].key;
                break;
            }
        }
        postData('/registration', submit_data, (data) => console.log('Data', data), (error) => console.error(error))

    }

    handleChange(e) {
        if (e.target.name === 'id_card_local_path') {
            var fileData = e.target.files[0]
            uploadFile('/upload', fileData, (data) => this.setState({ id_card_file: data.upload_file }), (error) => console.error(error));
        }

        var stateUpdate = {
            [e.target.name]: e.target.value
        }
        if (e.target.name === "registration_type") {
            if (e.target.value === 'Self') {
                stateUpdate['disableNoOfTickets'] = true;
                stateUpdate['no_of_ticket'] = 1;
            }
            else {
                stateUpdate['disableNoOfTickets'] = false;
            }
        }
        this.setState(stateUpdate)
    }

    render() {
        const { options, disableNoOfTickets, no_of_ticket, name, email_address, mobile_number, registration_type } = this.state;

        return (
            <Form onSubmit={this.handleSubmit}>
                <Input id="name" name="name" type="text" placeholder="Name" value={name} onChange={this.handleChange} required={true}></Input>
                <Input id="emailAddress" name="email_address" type="email" value={email_address} placeholder="Email Address" onChange={this.handleChange} required={true}></Input>
                <Input id="mobileNumber" name="mobile_number" type="tel" value={mobile_number} placeholder="Mobile Number" onChange={this.handleChange} required={true}></Input>
                <Input id="noOfticket" name="no_of_ticket" type="number" value={no_of_ticket} onChange={this.handleChange} placeholder="No Of Tickets" disabled={disableNoOfTickets} required={true}></Input>
                <Input id="idCard" name="id_card_local_path" type="file" accept='image/*' onChange={this.handleChange} required={true}></Input>
                <Select label='Registration Type:' options={options} id="registrationType" name="registration_type" value={registration_type} required={true} onChange={this.handleChange} displayname="Registration Type" />
                <Button type="submit">Register</Button>
            </Form>
        )
    }
};

export default UserForm;