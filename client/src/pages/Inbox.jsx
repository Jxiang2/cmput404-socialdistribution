import React, { Component } from 'react';
import {connect} from "react-redux";
import axios from "axios";
import {setCurrentUser} from "../redux/user/actions"
import "../styles/Inbox.css";
import InboxItem from '../components/InboxItem';

class Inbox extends Component {

    state = {
        currentUser: null,
        inboxItems: []
    }

    // This retreives the logged in user?
    componentDidMount = async () => {
        // retrieve authorID form redux
        const res = await axios.get(`/api/author/${this.props.authorID}`, {
            auth: {
                username: "socialdistribution_t21",
                password: "c404t21"
                }
        });

        await this.refreshInbox();
        this.setState({currentUser: res.data});
    }

    // This gets the logged in users inbox?
    refreshInbox = async () => {
        if (this.props.authorID !== null) {
            try {
            const res = await axios.get(`/api/author/${this.props.authorID}/inbox/`, {
                auth: {
                    username: "socialdistribution_t21",
                    password: "c404t21"
                    }
            });
            this.setState({inboxItems: res.data.items})
            console.log(res.data.items)
            } catch (e) {
                console.log(e);
            }
        } else {
            alert('Not Logged In!');
        }
    }

    populateInbox(items) {
        if (items) {
            return items.map(item => <div key={item.id}>{`${item.content}`}</div>)
        }
        return '';
    }

    render() {
        return(
            <div id="inbox-page">
                <h1>Inbox</h1>    
                {
                    this.state.inboxItems.length !== 0 ?
                        this.state.inboxItems.map((p, i) => 
                            <InboxItem post={p} key={i}/>
                        )
                        : <h1 style={{display:"flex", justifyContent:"center"}}>No Posts</h1>
                }
            </div>
        )
    }

}

// write to redux
const mapStateToProps = (state) => ({
    authorID: state.user.authorID
})
export default connect(mapStateToProps)(Inbox);