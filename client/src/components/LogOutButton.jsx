import { Button } from '@material-ui/core'
import React, { Component } from 'react'

import {connect} from "react-redux";
import {setCurrentUser} from "../redux/user/actions"


class LogOutButton extends Component {

    handleLogout = () => {
        this.props.setCurrentUser(null);
        window.location = '/login';
    }

    render() {
        return (
            <div style={{ display:'flex', justifyContent:'right', height:20}}>
                <Button onClick={this.handleLogout}>Log out</Button>
            </div>
        )
    }
}


// write to redux
const mapDispatchToProps = (dispatch) => ({
    setCurrentUser: user => {
        dispatch(setCurrentUser(user))
    }
})

export default connect(null, mapDispatchToProps)(LogOutButton);