import React, { Component } from "react";
import { connect } from 'react-redux';
import axios from 'axios';
import { Button } from "@material-ui/core"
import ReactMarkDown from "react-markdown";

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
    showComments: false,
    showEditForm: false,
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

  ShowEdit = () => {
    const { showEditForm } = this.state;
    this.setState({ showEditForm: !showEditForm });
  }

  handleShowComments = () => {
    const { showComments } = this.state;
    this.setState({ showComments: !showComments })
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
        console.log(err.response.status)
      }
    }
  }

  render() {
    
  

    return (
      <div style={{ border: "solid 1px grey" }}>
        <h1>Title: {this.props.post.title}</h1>
        <h2>{this.props.post.author.displayName}</h2>
        <h2>Description: {this.props.post.description}</h2>
        <p>{this.renderPostContent()}</p>
        {/* <Button color="primary" variant="outlined" style={{ margin: 5 }} onClick={this.ShowEdit}>edit post</Button> */}
        {/* <Button color="primary" variant="outlined" style={{ margin: 5 }} onClick={this.handleShowComments}>{this.state.showComments ? "Close" : "Show Comments"}</Button> */}
        <Button color="primary" variant="outlined" style={{ margin: 5 }} onClick={this.deletepostClick}>Delete</Button>
        <br />
        {
          this.state.showComments ?
            "show comments"
            :
            "not show comments"
        }
        {/* {
          this.state.showEditForm ? <PostEditForm postID={this.props.post.postID} /> : null
        } */}

      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})


export default connect(mapStateToProps)(PostItem);