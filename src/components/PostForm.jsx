import React, { Component } from "react";
import { Button, TextField } from "@material-ui/core";
import { connect } from "react-redux";
import "../styles/PostForm.css";
import axios from "axios";

class PostForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      show: false,
      title: "",
      description: "",
      contentType: "text/plain",
      category: "WEB TUTORIAL",
      content: "",
      visibility: "PUBLIC",
      unlisted: false,
      imagePreview: null,
      img: null,
      privateToAuthor: ""
    };
    this.onImageChange = this.onImageChange.bind(this);
    this.chooseFile = React.createRef();
  }


  componentDidMount = () => { 
      // console.log( "props: ", this.props)
  }

  onImageChange = event => {
    if (event.target.files && event.target.files[0]) {
      this.setState({ img: event.target.files[0] }, () => {
        this.setState({ imagePreview: URL.createObjectURL(this.state.img) });
      })
    }
  };

  getBase64 = (file) => {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    return new Promise(resolve => {
      reader.onload = e => {
        resolve(e.target.result);
      }
    })
  };

  showOpenFileDlg = () => {
    this.chooseFile.current.click()
  };

  handleShow = () => {
    const { show } = this.state;
    this.setState({ show: !show, visibility: "PUBLIC",description: "",title:"",content: "", unlisted: false, imagePreview:null, img:null});
  }

  sendPost = async (authorID, postID, visibility) => {
    
    // send to another author
    if (visibility === "PRIVATE") {
        let res = await axios.get(`api/author/${this.state.privateToAuthor}/`);
        // console.log(res.data)  
        let post_data = { "type": "post", "post_id": postID };
        let tmp_author_id = res.data.id.split("/");
        let rcver_id = tmp_author_id[tmp_author_id.length - 1];
        axios.post(`api/author/${rcver_id}/inbox/`, post_data);
    }
    else {
        // send to the public
        if (visibility === "PUBLIC") {
          const res = await axios.get(`api/author/`);
        
        } else if (visibility === "FRIEND") {
          // send to friends
            var res = await axios.get(`api/author/${authorID}/friends/`);
            var authors = res.data.items;
        
            for (let author of authors) {
                console.log(author)
                let data = { "type": "post", "post_id": postID };
                console.log(data)
                let tmp_author_id = author.id.split("/");
                let rcver_id = tmp_author_id[tmp_author_id.length - 1];
                console.log(rcver_id)
                if (rcver_id !== this.props.authorID)
                    axios.post(`api/author/${rcver_id}/inbox/`, data);
            }
        }
    }
  }

  handlePost = async () => {
    const { title, description, category, visibility, unlisted } = this.state;
    const { authorID } = this.props;

    if (this.state.contentType === "image") {
      // convert image to base 64
      var base64String = await this.getBase64(this.state.img);
      var contentType = base64String.slice(5).split(",")[0];
      var content = base64String;
    } else if (this.state.contentType === "text/plain" || this.state.contentType === "text/markdown") {
      contentType = this.state.contentType;
      console.log(contentType)
      content = this.state.content;
    }

    if (title && description && content) {
      try {
        // console.log(authorID)
        // console.log( title, source, origin, description, contentType, category, content, visibility, unlisted );
        var res = await axios.post(`api/author/${authorID}/posts/`, 
        { title, description, content, category, visibility, unlisted, contentType});

        this.props.handlePostView()
        // reset post form 
        this.setState({ show: false, visibility: "PUBLIC",description: "",title:"",content: "", unlisted: false, contentType: "text/plain",});
        let tmp_post_id = res.data.id.split("/");
        let resId = tmp_post_id[tmp_post_id.length - 1];
        // console.log("postID:", resId);
        if (!unlisted) { // unlisted === false
          this.sendPost(authorID, resId, visibility);
        }
        else {
          alert("this is the unlisted POST ID: " + resId);
        }

      } catch (err) {
        console.log(err.message);
      }
    } else {
      alert("Invalid Post Form !!!");
    }
  }

  render() {
    const { show, title, description, content, contentType, unlisted, privateToAuthor } = this.state;

    return (
      <div>
        {
          this.props.authorID !== null ?
            <div id="form-control">
              <Button
                variant="outlined" color="primary" onClick={this.handleShow}> {show ? "Cancel" : "Create Post"}
              </Button>
              {
                show ?
                  <div id="post-form">
                    <TextField
                      style={{ width: 300 }} label="Title" value={title}
                      onChange={(e) => this.setState({ title: e.target.value })}
                    /><br />
                    <TextField
                      style={{ width: 300 }} label="Description" value={description}
                      onChange={(e) => this.setState({ description: e.target.value })}/>
                      <br />
                    {
                      contentType === "text/plain" || contentType === "text/markdown" ?
                        <div>
                          <TextField
                            style={{ width: 350 }} label="Content" multiline rows={10} value={content}
                            onChange={(e) => this.setState({ content: e.target.value })}/>
                            <br />
                        </div>
                        :
                        <div>
                          <Button variant="outlined" color="primary" onClick={this.showOpenFileDlg}>Choose Image</Button>
                          <br />
                          <input type="file" ref={this.chooseFile} onChange={this.onImageChange} style={{ display: 'none' }} accept="image/png, image/jpeg" />
                          <div><img className="imagePreview" src={this.state.imagePreview} alt="Unavailable" /></div>
                        </div>
                    }

                    <label>Content Type:</label>
                    <select onChange={(e) => { this.setState({ contentType: e.target.value }) }}>
                      <option value="text/plain">plaintext</option>
                      <option value="text/markdown">markdown</option>
                      <option value="image">image</option>
                    </select>

                    <label>Visibility:</label>
                    <select onChange={(e) => { this.setState({ visibility: e.target.value }) }}>
                      <option value="PUBLIC">PUBLIC</option>
                      <option value="FRIEND">FRIEND</option>
                      <option value="PRIVATE">PRIVATE</option>
                    </select>
                    <p>{this.state.visibility}</p>
                    <label>Unlisted:</label>
                    <input type="checkbox" checked={unlisted} onChange={(e) => this.setState({ unlisted: e.target.checked })} />
                    {
                      this.state.visibility === "PRIVATE" ?
                        <TextField
                          style={{ margin: 10 }} value={privateToAuthor} onChange={(e) => this.setState({ privateToAuthor: e.target.value })} placeholder="private to" variant="filled"/>
                        :
                        null
                    }
                    <Button style={{ marginTop: 15 }} variant="outlined" color="primary" onClick={this.handlePost}>
                      Post
                    </Button>
                  </div>
                  :
                  null
              }
            </div>
            :
            <p>You are not logged in</p>
        }
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  authorID: state.user.authorID
})

export default connect(mapStateToProps)(PostForm);

