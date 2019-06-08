import React from 'react';
import {Query} from "react-apollo";
import {gql} from "apollo-boost";

const AllUsers = () => (
    <Query
        query={gql`
            {
                allUsers {
                    id
                    userName
                    email
                    firstName
                    lastName
                }
            }
        `}
    >
        {({loading, error, data}) => {
            if (loading) return <p>Loading...</p>;
            if (error) return <p>Error :(</p>;

            console.log(data);
            return (
                <ul>
                    {data.allUsers.map( (user) => {
                        return (
                            <li key={user.id}>
                                {user.email}
                            </li>
                        )
                    })}
                </ul>
            )
        }}
    </Query>
);

export default AllUsers;