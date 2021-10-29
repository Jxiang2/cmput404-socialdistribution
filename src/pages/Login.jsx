import React, { Component } from 'react';
import {connect} from "react-redux";
import axios from "axios";
import {setCurrentUser} from "../redux/user/actions"
import "../styles/Login.css";


class Login extends Component {

    state ={
        email:'',
        password:''
    }

    handelLogin = async () => {
        const {email, password} = this.state;
        try {
            const res = await axios.post("/api/login/", { email, password }, {
                auth: {
                username: "socialdistribution_t21",
                password: "c404t21"
                }
            });
            console.log(res);
            // with mapDispatchToProps, I can write to redux
            this.props.setCurrentUser(res.data.authorID);
            // with mapStateToProps, I can pull from redux
            console.log('redux store:',this.props.authorID);
            //redirect to homepage
            window.location = '/home';

            
        } catch (e) {
            console.log(e);
            alert("invalid data!")
        }
    }

    componentDidMount = () => {
        console.log('props in Login:',this.props);
    }

    render() {
        return (
            <div id="login-page">
                <h1>CMPUT404 Social Distribution</h1>
                <i className="fas fa-envelope-open-text"></i>
                <input type="email" id="login-email" placeholder='your email' value={this.state.email} onChange={(e)=> this.setState({email:e.target.value})} />
                <i className="fas fa-key"></i>
                <input type="password" id="login-pwd" placeholder='your passowrd' value={this.state.password} onChange={(e)=> this.setState({password:e.target.value})} />
                <button id="login-btn" onClick={this.handelLogin}>Login</button>
            </div>
        )
    }
}

// Read From Redux
const mapStateToProps = (state) => ({
    authorID: state.user.authorID
})

// write to redux
const mapDispatchToProps = (dispatch) => ({
    setCurrentUser: user => {
        dispatch(setCurrentUser(user))
    }
})

// export the login page with redux feature (state feature)
export default connect(mapStateToProps, mapDispatchToProps)(Login);