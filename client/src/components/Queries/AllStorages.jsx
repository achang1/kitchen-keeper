import React from 'react';
import {Query} from "react-apollo";
import {gql} from "apollo-boost";

const AllStorages = () => (
    <Query
        query={gql`
            {
                allStorages {
                    id
                    name
                    storageType
                    users {
                        userName
                        email
                    }
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
                    {data.allStorages.map( (storage) => {
                        return (
                            <li key={storage.id}>
                                {storage.storageType}
                            </li>
                        )
                    })}
                </ul>
            )
        }}
    </Query>
);

export default AllStorages;