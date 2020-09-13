import { doGeocode } from "../utils/http_functions";
import { parseJSON } from "../utils/misc";

export const FETCH_GEOCODE_REQUEST = "geocode/FETCH_GEOCODE_REQUEST";
export const RECEIVE_GEOCODE = "geocode/RECEIVE_GEOCODE";
export const RECEIVE_GEOCODE_ERROR = "geocode/RECEIVE_GEOCODE_ERROR";
export const SET_SELECTED_GEOCODE = "geocode/SET_SELECTED_GEOCODE";

const initialState = {
    isFetching: false,
    dataId: null,
    searchTerm: "",
    selected: {
        coords: [],
        id: 0
    },
    results: [],
    status: "success",
    message: {}
};

// reducer
export default (state = initialState, action) => {
    switch (action.type) {
        case FETCH_GEOCODE_REQUEST:
            return {
                ...state,
                isFetching: true,
                dataId: action.payload.dataId,
                searchTerm: action.payload.searchTerm
            };

        case RECEIVE_GEOCODE:
            if (state.dataId === action.payload.dataId) {
                return {
                    ...state,
                    isFetching: false,
                    results: action.payload.response.data,
                    status: action.payload.response.status
                };
            }
            return state;

        case RECEIVE_GEOCODE_ERROR:
            return {
                ...state,
                isFetching: false,
                status: "fail",
                message: action.payload
            };

        case SET_SELECTED_GEOCODE:
            return {
                ...state,
                selected: {
                    id: action.payload.id,
                    coords: action.payload.coords
                }
            };

        default:
            return state;
    }
};

// action
export const fetchGeocodeResults = searchTerm => {
    return dispatch => {
        const dataId = Math.random();

        dispatch({
            type: FETCH_GEOCODE_REQUEST,
            payload: { searchTerm, dataId }
        });

        doGeocode(searchTerm)
            .then(parseJSON)
            .then(response => {
                dispatch({
                    type: RECEIVE_GEOCODE,
                    payload: { response, dataId }
                });
            })
            .catch(error => {
                dispatch({
                    type: RECEIVE_GEOCODE_ERROR,
                    payload: error
                });
            });
    };
};

// action
export const setGeocodeResults = selected => {
    const id = Math.random();

    const coords = JSON.parse(selected);

    return dispatch => {
        dispatch({
            type: SET_SELECTED_GEOCODE,
            payload: { coords, id }
        });
    };
};
