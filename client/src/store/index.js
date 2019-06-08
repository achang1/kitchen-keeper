import {createStore} from "redux";
import {initialState} from "../store/states/initialState";
import rootReducer from "../reducers";

const store = createStore(rootReducer, initialState);

export default store;