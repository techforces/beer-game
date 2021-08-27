import React, { useState } from 'react';
import './Forms.css';
import logo from './beergamelogo.png';
import { withRouter, useHistory } from "react-router-dom";
import Cookies from 'js-cookie';
import AuthService from "../../services/AuthService";

// https://getbootstrap.com/docs/4.3/components/forms/
// in react we use className to give class to certain tag instead of class since it follows the rules of jsx code not HTML

function LoginForm(props) {

    const history = useHistory();

    React.useEffect(() => {
        if (Cookies.get('SESSION-KEY') !== undefined) {
            props.history.push('/dashboard');
        }
    })

    const [state, setState] = useState({
        email: "",
        password: "",
        error_message: ""
    })

    const handleChange = (e) => {
        const { name, value } = e.target
        setState(prevState => ({
            ...prevState,
            [name]: value
        }))
    }
    function loginfailed(){
        setState(prevState => ({
            ...prevState,
            password: "",
            error_message: 'error: invalid email / password. Please try again'
        }))
    }

    function handleLogin(e){
        e.preventDefault();
        AuthService.login(state.email, state.password)
        .then(() => {
           history.push('/dashboard')
        })
        .catch((e) =>{
            loginfailed();
        })
        
    }

    const redirectToRegistration = () => {
        props.history.push('/register'); 
    }

    return (
        <div align="center">
            <form className="form-signin">
                <img className="mb-4" src={logo} alt="" width="72" height="72"/>
                <h1 className="h3 mb-3 font-weight-normal">Please sign in</h1>

                <div>
                    <label htmlFor="InputEmail1" className="sr-only" >Email address</label>
                    <input type="email" className="form-control" id="email" name="email" aria-describedby="emailHelp" placeholder="Enter email" value={state.email} onChange={handleChange} required/>
                </div>

                <div>
                    <label htmlFor="InputPassword1" className="sr-only">Password</label>
                    <input type="password" className="form-control" id="password" name="password" placeholder="Password" value={state.password} onChange={handleChange} required/>
                </div>
                { state.error_message &&
                        <span className="error"> { state.error_message } </span> }
                <div className="checkbox mb-3">
                    <input type="checkbox" value="remember-me"/> 
                    <label> Remember me </label>
                </div>

                <button type="submit" className="btn btn-lg btn-primary btn-block" onClick={handleLogin}> Login </button>

                <div className="mt-2">
                    <span>Do not have an account? </span>
                    <span className="RegisterHere" onClick={() => redirectToRegistration()}>Register here</span>
                </div>

            </form>
        </div>
    )
}
export default withRouter(LoginForm);