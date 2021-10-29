import React, {Component} from 'react'
import {connect} from "react-redux";
import axios from "axios";
import UserHeader from '../components/UserHeader';
import PostItem from '../components/PostItem';
import PostForm from '../components/PostForm';
import LogOutButton from '../components/LogOutButton';

class HomePage extends Component {
    state = {
        currentUser: null,
        publicPosts: []
    }

    componentDidMount = async () => {
        console.log(this.props.authorID);
        // retrieve authorID form redux
        const res = await axios.get(`/api/author/${this.props.authorID}/`);

        await this.handlePostView();
        this.setState({currentUser: res.data});
    }

    handlePostView = async () => {
        if (this.props.authorID !== null) {
            try {
            const res = await axios.get("/api/posts/");
            console.log(res.data.posts);
            this.setState({publicPosts: res.data.posts.filter((post)=>{
                // only show the public posts
                return post.visibility === "PUBLIC" && post.unlisted  === false;
            })});
            } catch (e) {
                console.log(e);
            }   
        } else {
            alert('Not Logged In!');
        }   
    }

    // get the inbox content
    showInbox = async () => {
        if (this.props.authorID !== null) {
            try {
            const res = await axios.get(`/api/author/${this.props.authorID}/inbox/`);
            } catch (e) {
                console.log(e);
            }
        } else {
            alert('Not Logged In!');
        }
    }

    // clear the inbox content
    clearInbox = async () => {
        if (this.props.authorID !== null) {
            try {
                const res = await axios.delete(`/api/author/${this.props.authorID}/inbox/`);
            } catch (e) {
                console.log(e)
            }
        } else {
            alert('Not Logged In!');
        }
    }

    renderHeader =  () => {
        const {currentUser} = this.state;
        switch (currentUser) {
            case null:
                return "";
            default:
                return <UserHeader currentUser={currentUser} />
        }
    }

    render() {
        return (
            <>
                <LogOutButton />
                <div>
                    {this.renderHeader()}
                </div>
                <div>
                    {
                    this.state.publicPosts.length !== 0 ?
                        this.state.publicPosts.map((p, i) => 
                            <PostItem post={p} key={i} handlePostView={this.handlePostView} />
                        )
                        : <h1 style={{display:"flex", justifyContent:"center"}}>No Posts</h1>
                    }
                </div>
                <div>
                    <PostForm handlePostView={this.handlePostView}/>
                </div>
            </>
        )
    }
}

// write to redux
const mapStateToProps = (state) => ({
    authorID: state.user.authorID
})
export default connect(mapStateToProps)(HomePage);
