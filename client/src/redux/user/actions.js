import {SET_CURRENT_USER} from "./types";

export const setCurrentUser = (authorId) => {
    return {
        type: SET_CURRENT_USER,
        payload: authorId
    };
};