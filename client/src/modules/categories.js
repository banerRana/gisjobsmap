import { getTitles } from "../utils/http_functions";

import { parseJSON } from "../utils/misc";

export const FETCH_CATEGORIES_REQUEST = "categories/FETCH_CATEGORIES_REQUEST";
export const RECEIVE_CATEGORIES = "categories/RECEIVE_CATEGORIES";
export const RECEIVE_CATEGORIES_ERROR = "categories/RECEIVE_CATEGORIES_ERROR";

const initialState = {
    isFetching: false,
    status: "",
    data: []
};

// reducer
export default (state = initialState, action) => {
    switch (action.type) {
        case FETCH_CATEGORIES_REQUEST:
            return {
                ...state,
                isFetching: true
            };

        case RECEIVE_CATEGORIES:
            return {
                ...state,
                isFetching: false,
                data: action.response.data,
                status: action.respsonse.status
            };

        case RECEIVE_CATEGORIES_ERROR:
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
export const fetchCategories = searches => {
    return dispatch => {
        dispatch({
            type: FETCH_CATEGORIES_REQUEST
        });

        getTitles()
            .then(parseJSON)
            .then(response => {
                dispatch({
                    type: RECEIVE_CATEGORIES,
                    payload: response
                });
            })
            .catch(error => {
                dispatch({
                    type: RECEIVE_CATEGORIES_ERROR,
                    payload: error
                });
            });
    };
};
