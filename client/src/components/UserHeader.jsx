import React from 'react';
import '../styles/Headers.css';
import Avatar from '@material-ui/core/Avatar';


const UserHeader = (props) => {
  // console.log(props);
  return (
    <div id="user-header">
      <h1>Welcome To Social Distribution,  {props.currentUser.displayName} </h1>
      <hr />
      <div>
        <Avatar id="user-avatar">{props.currentUser.displayName.slice(0, 1)}</Avatar>
        <div id="user-info">
          <h2>Email: {props.currentUser.email}</h2>
          <h2>Github: {props.currentUser.github}</h2>
        </div>

      </div>
    </div>
  );
}
export default UserHeader;