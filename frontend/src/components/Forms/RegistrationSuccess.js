import React from 'react';
import { withRouter } from "react-router-dom";

function RegistrationSuccess(props) {

    const redirectToLogin = () => {
        props.history.push('/login'); 
    }

    return (
        <div align='center'>
            <div>
                <h2>You are now registered!</h2>
            </div>
            <button type="button" className="btn btn-lg btn-primary" onClick={redirectToLogin}> Login </button>
        </div>
    );
}

export default withRouter(RegistrationSuccess);