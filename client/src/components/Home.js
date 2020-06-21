import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'semantic-ui-react'



class Home extends Component {
    render() {
        return (
            <>
                <h1>Home Page</h1>
                <Link to="/registration"><Button>Registration</Button></Link>
            </>
        )
    }
}

export default Home;