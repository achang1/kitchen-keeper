import {gql} from "apollo-boost";

export const ALLUSERS_QUERY = gql`
    {
        allUsers {
            id
            userName
            email
            firstName
            lastName
        }
    }
`