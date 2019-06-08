import {INIT_HOMEPAGE} from "../constants/action-types";

function rootReducer(state, action) {
    if (action.type === INIT_HOMEPAGE) {
        return {
            ...state,
            allUsers: action.payload.allUsersData.data.allUsers,
            allStorages: action.payload.allStoragesData.data.allStorages
          }
    }
    return state;
}

export default rootReducer;