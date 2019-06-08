import React, {Component, Fragment} from 'react';
import {AllUsers, AllStorages} from "./Queries/index";

class HomePage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            allUsers: false,
            allStorages: false
        };

        this.fetchUsers.bind(this);
    }
    

    fetchUsers() {
        this.setState({
            allUsers: true
        })
    }

    fetchStorages() {
        this.setState({
            allStorages: true
        })
    }

    render() {
        if (this.state.allUsers) {
            return (
                <Fragment>
                    <AllUsers />
                </Fragment>
            )
        }

        if (this.state.allStorages) {
            return (
                <Fragment>
                    <AllStorages />
                </Fragment>
            )
        }

        return (
            <Fragment>
                <button
                    onClick={() => this.fetchUsers()}>
                    GET Users
                </button>
                <button
                    onClick={() => this.fetchStorages()}>
                    Get Storages
                </button>
            </Fragment>
        )
    }
}

export default HomePage;