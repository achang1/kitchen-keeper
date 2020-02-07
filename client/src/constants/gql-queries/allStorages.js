import {gql} from "apollo-boost";

export const ALLSTORAGES_QUERY = gql`
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
`