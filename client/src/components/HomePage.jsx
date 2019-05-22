import React, {Component, Fragment} from 'react';
import API from '../utils/API';

class HomePage extends Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    async componentDidMount() {
        let users = await API.post(
            '/',
            {
                query: `
                query {
                    allUsers {
                      id
                      userName
                      email
                    }
                  }
                    `
            });

        console.log(users);
    }

    async fetchUsers() {
        try {
            let users = await API.post(
                '/',
                {
                    query: `
                    query  {
                        allUsers{
                          id
                          userName
                          email
                        }
                    }
                        `
                });

            console.log(users);
        } catch(e) {
            console.log(e);
        }
    }

    render() {
        return (
            <Fragment>
                <button
                    onClick={() => this.fetchUsers()}>
                    GET Users
                </button>
            </Fragment>
        )
    }
}

export default HomePage;