import React, { Component } from 'react'

class Register extends Component {
    state ={
        username:'',
        email:'',
        password:'',
        github:'',

    }
    
    componentDidMount = () => {

    }

    render() {
        return (
            <div>
                <p>{this.state.username}</p>
                <input type="text" name="" id="" placeholder='your username' value={this.state.username} onChange={(e)=> this.setState({username:e.target.value})} />
            </div>
        )
    }
}

export default Register;
