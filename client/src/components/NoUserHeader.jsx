import React from 'react';
import '../../styles/Headers.css';

const NoUserHeader = (props) => {
  return (
    <div id="no-user-header">
      <h1>Please Login or Register</h1>
      <hr />
      <div>
        <div id="empty-avatar" className="col-3" />
        <h4 id="no-user-message">No User Detected, Please Login</h4>
      </div>
    </div>
  )
}

export default NoUserHeader