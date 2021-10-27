import React, {Component} from 'react';

class NavBar extends Component {

    render() {
        return (
            <div id='nav-bar'>
            <a href='/home'>Home</a><a href='/friends'>Friends</a><a href='/inbox'>Inbox</a><a href='/logout'>Logout</a><a href='/login'>Login</a>
            </div>
        )     
    }
}

export default NavBar;