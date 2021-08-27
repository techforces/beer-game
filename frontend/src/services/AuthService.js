import Cookies from "js-cookie";
import axios from "axios";


// This class acts as a wrapper for the different calls we make to the Authentication endpoints.
export default class AuthService {

    static authEndpoint = 'http://localhost:8086'

    // Removes the current session from the cookies.
    static signOut() {
        Cookies.remove('SESSION-KEY');
        Cookies.remove('role');
        Cookies.remove('id');
    }

    // Authenticates the given email and password, then sets the corresponding session in the cookies.
    static login(email, password) {
        return new Promise((resolve, reject) => {
            axios.post(this.authEndpoint + '/authenticate', { email: email, passwordHash: password })
                .then(response => {
                    var x = response.data
                    Cookies.set('SESSION-KEY', x['SESSION-KEY']);
                    Cookies.set('id', x['id']);
                    Cookies.set('role', x['role']);
                    resolve();

                })
                .catch((error) => {
                    if (error.response) {
                        console.log(error.response.status);
                        //alert('Response failure');
                    } else if (error.request) {
                        console.log(error.request);
                    }
                    reject();
                })
        })
    }

    static register(email, password, user_type) {
        return new Promise((resolve, reject) => {
            axios.post(this.authEndpoint + '/register',
                {
                    //name: name,
                    email: email,
                    passwordHash: password,
                    role: user_type
                })
                .then(response => {
                    var x = response.data;
                    Cookies.set('SESSION-KEY', x['SESSION-KEY']);
                    this.signOut();
                    resolve();
                })
                .catch((error) => {
                    if (error.response) {
                        console.log(error.response.status);
                        alert('Response failure');
                    } else if (error.request) {
                        console.log(error.request);
                    }
                    reject();
                })
        })
    }
}