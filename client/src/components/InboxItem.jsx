import React, { Component } from "react";
import { connect } from 'react-redux';
import ReactMarkDown from "react-markdown";

// This component is used to display the Post
class InboxItem extends Component {
  state = {
    title: "",
    source: "",
    origin: "",
    description: "",
    contentType: "",
    content: "",
    visibility: "",
    unlisted: false,
  }

  renderPostContent = () => {
    const { contentType } = this.props.post;
    
    switch (contentType) {
      case "text/markdown":
        return <ReactMarkDown>{this.props.post.content}</ReactMarkDown>;
      case "image/png;base64":
      case "image/jpeg;base64":
        return <div><img className="imagePreview" src={this.props.post.content} alt="Unavailable" /></div>
      default:
        return <p>{this.props.post.content}</p>
    }
  }

  render() {
    return (
      <div style={{ border: "solid 1px grey" }}>
        <h1>{this.props.post.title}</h1>
        <h3>{this.props.post.author.displayName}</h3>
        <h3>description: {this.props.post.description}</h3>
        <p id="post-text">{this.renderPostContent()}</p>
        <br/>
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})

export default connect(mapStateToProps)(InboxItem);