import {INIT_HOMEPAGE} from "../constants/action-types";
import {client} from "../utils/API";
import {allUsersQuery} from "../constants/gql-queries/index";
import {allStoragesQuery} from "../constants/gql-queries/index";

export async function initializeHomePage(dispatch) {
    const allUsersData = await client.query({
        query: allUsersQuery
    })

    const allStoragesData = await client.query({
        query: allStoragesQuery
    })

    dispatch({
        type: INIT_HOMEPAGE,
        payload: {
            allUsersData,
            allStoragesData
        }
    });
};