import React, { Component } from 'react';
import axios from "axios";
import "../styles/Register.css";

class Register extends Component {
    state ={
        username:'',
        email:'',
        password:'',
        github:''
    }
    
    componentDidMount = () => {
        console.log();
    }

    handleRegister = async () => {
        const {email, username, github, password} = this.state;
        try {
            const res = await axios.post("/api/register/", { email, username, github, password });
            console.log(res)

            if (res.status === 201) {
                // this.props.setCurrentUser(res.data);
                window.location = '/login'
            }

        } catch (e) {
            console.log('error', e);
            alert("Invalid Inputs!")
        }
        
    }

    render() {
        return (
            <div id="register-page">
                <h1>CMPUT404 Social Distribution</h1>
                <i className="fas fa-id-card fa-1x"></i>
                <input type="text" id="username" placeholder='your username' value={this.state.username} onChange={(e)=> this.setState({username:e.target.value})} />
                <i className="fas fa-envelope-open-text"></i>
                <input type="email" id="email" placeholder='your email' value={this.state.email} onChange={(e)=> this.setState({email:e.target.value})} />
                <i className="fas fa-key"></i>
                <input type="password" id="pwd" placeholder='your passowrd' value={this.state.password} onChange={(e)=> this.setState({password:e.target.value})} />
                <i className="fab fa-github"></i>
                <input type="text" id="github" placeholder='your github' value={this.state.github} onChange={(e)=> this.setState({github:e.target.value})} />
                <button id="register-btn" onClick={this.handleRegister}>submit</button>
            </div>
        )
    }
}

export default (Register);
