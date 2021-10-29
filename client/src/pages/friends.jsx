import React, { Component } from "react";

class Friends extends Component {
  state = {
    count: 0,
    friends: ["user1", "user2", "user3"],
    searchResults: ["searchUser1", "searchUser2", "serachUser3"],
  };

  renderFriends() {
    if (this.state.friends.length === 0) return <p>There are no tags!</p>;

    return (
      <ul>
        {this.state.friends.map((friend) => (
          <li key={friend}>
            {friend}
            <button>Unfollow</button>
          </li>
        ))}
      </ul>
    );
  }

  renderSearchResults() {
    return (
      <ul>
        {this.state.searchResults.map((searchResult) => (
          <li key={searchResult}>
            {searchResult}
            <button>Follow</button>
          </li>
        ))}
      </ul>
    );
  }

  render() {
    return (
      <div>
        <h4>Search</h4>
        <form>
          <label>
            <input type="text" name="Search" />
          </label>
          <input type="submit" value="Search" />
        </form>
        {this.renderSearchResults()}
        <h4>My Friends</h4>
        {this.state.friends.length === 0 && "Plase make new friends!"}
        {this.renderFriends()}
      </div>
    );
  }
}

export default Friends;
