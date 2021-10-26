import React, { Component } from 'react';
import axios from "axios";

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
            const res = await axios.post("/api/register/", { email, username, github, password }, {
                auth: {
                username: "socialdistribution_t21",
                password: "c404t21"
                }
            });
            console.log(res)

            if (res.status === 201) {
                // this.props.setCurrentUser(res.data);
                window.location = '/login'
            }

        } catch (e) {
            console.log('error', e);
        }
        
    }

    render() {
        return (
            <div>
                <i className="fas fa-id-card fa-1x"></i>
                <input type="text" id="username" placeholder='your username' value={this.state.username} onChange={(e)=> this.setState({username:e.target.value})} />
                <br/>
                <i className="fas fa-envelope-open-text"></i>
                <input type="email" id="email" placeholder='your email' value={this.state.email} onChange={(e)=> this.setState({email:e.target.value})} />
                <br/>
                <i className="fas fa-key"></i>
                <input type="password" id="pwd" placeholder='your passowrd' value={this.state.password} onChange={(e)=> this.setState({password:e.target.value})} />
                <br/>
                <i className="fab fa-github"></i>
                <input type="text" id="github" placeholder='your github' value={this.state.github} onChange={(e)=> this.setState({github:e.target.value})} />
                <br/>
                <button id="" onClick={this.handleRegister}>submit</button>
            </div>
        )
    }
}

// wirte to redux
// const mapDispatchToProps = (dispatch) => ({
//     setCurrentUser: user => {
//         dispatch(setCurrentUser(user))
//     }
// })

// first param -- read
// second param -- write
// export default connect(null, mapDispatchToProps)(Register);
export default (Register);
