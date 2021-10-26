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
        // retrieve authorID form redux
        const res = await axios.get(`/api/author/${this.props.authorID}`, {
            auth: {
                username: "socialdistribution_t21",
                password: "c404t21"
                }
        });

        await this.handlePostView();

        this.setState({currentUser: res.data});
    }

    handlePostView = async () => {
        if (this.props.authorID !== null) {
            try {
            const res = await axios.get("/api/posts/", {
                auth: {
                    username: "socialdistribution_t21",
                    password: "c404t21"
                    } 
            });
            
            this.setState({publicPosts: res.data.posts});
        } catch (e) {
            console.log(e);
            }   
        } else {
            alert('Not Logged In!');
        }   
    }

    refreshInbox = async () => {
        if (this.props.authorID !== null) {
            try {
            const res = await axios.get(`/api/author/${this.props.authorID}/inbox/`, {
                auth: {
                    username: "socialdistribution_t21",
                    password: "c404t21"
                    }
            });
            } catch (e) {
                console.log(e);
            }
        } else {
            alert('Not Logged In!');
        }
    }

    clearInbox = async () => {
        if (this.props.authorID !== null) {
            try {
                const res = await axios.delete(`/api/author/${this.props.authorID}/inbox/`, {
                    auth: {
                        username: "socialdistribution_t21",
                        password: "c404t21"
                    }
                });
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
                        : "No posts"
                    }
                </div>

                <PostForm/>
            </>
        )
    }
}

const mapStateToProps = (state) => ({
    authorID: state.user.authorID
})

export default connect(mapStateToProps)(HomePage);
