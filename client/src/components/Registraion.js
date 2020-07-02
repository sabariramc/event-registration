import React, { Component } from 'react';


import { Helmet } from "react-helmet";

import UserForm from "./UserForm";

import UserPreview from './UserPreview'

import { getData, postData, uploadFile } from "../services";

import { Error } from "../common";

class Registraion extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handlePreview = this.handlePreview.bind(this);
        this.state = {
            options: []
            , no_of_ticket: 1
            , name: ''
            , email_address: ''
            , mobile_number: ''
            , id_card_file: ''
            , id_card_local_path: ''
            , registration_type: 'Self'
            , preview: false
            , disableNoOfTickets: true
            , errorMessage: null
            , previewFile: ''
        }
    }

    componentDidMount() {
        getData('/registration/config', (data) => this.setState({ options: data }))
    }

    handleSubmit(e) {
        e.preventDefault();
        const { no_of_ticket, name, email_address, mobile_number, id_card_file, registration_type, options } = this.state;
        var submit_data = { no_of_ticket, name, email_address, mobile_number, id_card_file };
        for (var i in options) {
            if (options[i].value === registration_type) {
                submit_data['registration_type'] = options[i].key;
                break;
            }
        }
        postData('/registration', submit_data, (data) => console.log('Data', data), (error) => this.setState({ preview: false, errorMessage: error.message }))
    }

    handlePreview(e) {
        e.preventDefault();
        const previewFile = API_URL + '/preview/download/' + this.state.id_card_file;
        this.setState({ preview: true, previewFile: previewFile })
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
        const { preview, errorMessage } = this.state;
        return (
            <div>
                <Helmet>
                    <title>Registration</title>
                </Helmet>
                {preview ? <UserPreview userData={this.state} onSubmit={this.handleSubmit} /> : <UserForm onSubmit={this.handlePreview} userData={this.state} onChange={this.handleChange} />}
                {
                    errorMessage != null ? <Error>{errorMessage}</Error> : <span></span>
                }
            </div>
        )
    }
}

export default Registraion;