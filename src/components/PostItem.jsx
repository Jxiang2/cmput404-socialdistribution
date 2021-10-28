import React, { Component } from "react";
import { connect } from 'react-redux';
import axios from 'axios';
import { Button } from "@material-ui/core"
import ReactMarkDown from "react-markdown";
import '../styles/PostItem.css'

// This component is used to display the Post
class PostItem extends Component {
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
    const { visibility } = this.props.post;
    console.log(visibility)
    console.log(contentType)
    if (visibility === "PUBLIC") {
      // console.log("I am Here")
      switch (contentType) {
      case "text/markdown":
        return <ReactMarkDown>{this.props.post.content}</ReactMarkDown>;
      case "text/plain":
        return <p>{this.props.post.content}</p>;
      case "image/png;base64":
      case "image/jpeg;base64":
        return <div><img className="imagePreview" src={this.props.post.content} alt="Unavailable" /></div>
      default:
        return <p>{this.props.post.content}</p>;
      }
    }
  }


  deletepostClick = async () => {
    var login_author_id = this.props.authorID
    var post_author_id = this.props.post.author_id
    var post_id = this.props.post.id
    let tmp_post_id = post_id.split("/");

    let resId = tmp_post_id[tmp_post_id.length - 1];
    if (login_author_id !== post_author_id) {
      window.alert("you cannot delete this post")
    } else {
      try {
        const res = await axios.delete(`api/author/${post_author_id}/posts/${resId}/`, { 
            auth:{
             username: "socialdistribution_t21", 
             password: "c404t21" } 
            })
        if (res.status === 200) {
        //   window.location = '/home'
            this.props.handlePostView();
        }
      } catch (err) {
        // console.log(err.response.status)
      }
    }
  }

  render() {

    var login_id = this.props.post.author.authorID;
    var author_id = this.props.authorID.authorID;

    if (this.props.post.visibility === "FRIEND") {
      if (login_id === author_id) {
        var visible = true;
      } else {
        var visible = false;
      }
    } else {
      var visible = true;
    }

    return (
      <div style={{ border: "solid 1px grey" }}>
        <h1>{this.props.post.title}</h1>
        <h3>{this.props.post.author.displayName}</h3>
        <h3>description: {this.props.post.description}</h3>
        <p id="post-text">{this.renderPostContent()}</p>
        <Button style={{color:"black", backgroundColor:"grey"}} 
        onClick={this.deletepostClick}>Delete</Button>
        <br/>
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})

export default connect(mapStateToProps)(PostItem);