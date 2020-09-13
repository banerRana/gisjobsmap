import { getTags } from "../utils/http_functions";

import { parseJSON } from "../utils/misc";

export const FETCH_TAGS_REQUEST = "tags/FETCH_TAGS_REQUEST";
export const RECEIVE_TAGS = "tags/RECEIVE_TAGS";
export const RECEIVE_TAGS_ERROR = "tags/RECEIVE_TAGS_ERROR";

const initialState = {
    isFetching: false,
    status: "",
    data: []
};

// reducer
export default (state = initialState, action) => {
    switch (action.type) {
        case FETCH_TAGS_REQUEST:
            return {
                ...state,
                isFetching: true
            };

        case RECEIVE_TAGS:
            return {
                ...state,
                isFetching: false,
                data: action.response.data,
                status: action.respsonse.status
            };

        case RECEIVE_TAGS_ERROR:
            return {
                ...state,
                isFetching: false,
                data: action.response.data,
                status: action.respsonse.status
            };

        default:
            return state;
    }
};

// action
export const fetchTags = searches => {
    return dispatch => {
        dispatch({
            type: FETCH_TAGS_REQUEST
        });

        getTags()
            .then(parseJSON)
            .then(response => {
                dispatch({
                    type: RECEIVE_TAGS,
                    payload: response
                });
            })
            .catch(error => {
                dispatch({
                    type: RECEIVE_TAGS_ERROR,
                    payload: error
                });
            });
    };
};
