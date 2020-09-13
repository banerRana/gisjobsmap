import {
    getJobs
    // getOrganizations,
    // getSchools,
    // getRFPs,
    // getResumes
} from "../utils/http_functions";
import { parseJSON } from "../utils/misc";

export const FETCH_DATA_REQUEST = "data/FETCH_DATA_REQUEST";
export const RECEIVE_DATA = "data/RECEIVE_DATA";
export const RECEIVE_DATA_ERROR = "data/RECEIVE_DATA_ERROR";

const initialState = {
    isFetching: false,
    dataId: null,
    error: { status: false, response: null },
    features: [],
    near: { properties: {} },
    country: { iso2: "", name: "", geom: {} }
};

// reducer
export default (state = initialState, action) => {
    switch (action.type) {
        case FETCH_DATA_REQUEST:
            return {
                ...state,
                isFetching: true,
                dataId: action.payload.dataId,
                searches: action.payload.searches,
                features: initialState.features,
                near: initialState.near,
                country: initialState.country,
                error: { status: false, response: null }
            };

        case RECEIVE_DATA:
            if (state.dataId === action.payload.dataId) {
                return {
                    ...state,
                    isFetching: false,
                    features: action.payload.response.data,
                    near: action.payload.response.near,
                    country: action.payload.response.country
                };
            }
            return state;

        case RECEIVE_DATA_ERROR:
            return {
                ...state,
                isFetching: false,
                error: action.payload.response
            };

        default:
            return state;
    }
};

// action
export const fetchData = searches => {
    return dispatch => {
        const dataId = Math.random();

        dispatch({
            type: FETCH_DATA_REQUEST,
            payload: { searches, dataId }
        });

        getJobs(searches)
            .then(parseJSON)
            .then(response => {
                dispatch({
                    type: RECEIVE_DATA,
                    payload: { response, dataId }
                });
            })
            .catch(error => {
                dispatch({
                    type: RECEIVE_DATA_ERROR,
                    payload: error
                });
            });

        // if (layer.toLowerCase() === 'jobs') {
        //     getJobs(searches)
        //         .then(parseJSON)
        //         .then(response => {
        //             dispatch({
        //                 type: RECEIVE_DATA,
        //                 payload: { response, dataId }
        //             })
        //         })
        //         .catch(error => {
        //             dispatch({
        //                 type: RECEIVE_DATA_ERROR,
        //                 payload: error
        //             })
        //         });
        // }

        // else if (layer.toLowerCase() === 'organizations') {
        //     getOrganizations(searches)
        //         .then(parseJSON)
        //         .then(response => {
        //             dispatch({
        //                 type: RECEIVE_DATA,
        //                 payload: { response, dataId }
        //             })
        //         })
        //         .catch(error => {
        //             dispatch({
        //                 type: RECEIVE_DATA_ERROR,
        //                 payload: error
        //             })
        //         });
        // }

        // else if (layer.toLowerCase() === 'schools') {
        //     getSchools(searches)
        //         .then(parseJSON)
        //         .then(response => {
        //             dispatch({
        //                 type: RECEIVE_DATA,
        //                 payload: { response, dataId }
        //             })
        //         })
        //         .catch(error => {
        //             dispatch({
        //                 type: RECEIVE_DATA_ERROR,
        //                 payload: error
        //             })
        //         });
        // }

        // else if (layer.toLowerCase() === 'rfps') {
        //     getRFPs(searches)
        //         .then(parseJSON)
        //         .then(response => {
        //             dispatch({
        //                 type: RECEIVE_DATA,
        //                 payload: { response, dataId }
        //             })
        //         })
        //         .catch(error => {
        //             dispatch({
        //                 type: RECEIVE_DATA_ERROR,
        //                 payload: error
        //             })
        //         });
        // }

        // else if (layer.toLowerCase() === 'resumes') {
        //     getResumes(searches)
        //         .then(parseJSON)
        //         .then(response => {
        //             dispatch({
        //                 type: RECEIVE_DATA,
        //                 payload: { response, dataId }
        //             })
        //         })
        //         .catch(error => {
        //             dispatch({
        //                 type: RECEIVE_DATA_ERROR,
        //                 payload: error
        //             })
        //         });
        // }

        // else if (layer.toLowerCase() === 'events') {
        //     getResumes(searches)
        //         .then(parseJSON)
        //         .then(response => {
        //             dispatch({
        //                 type: RECEIVE_DATA,
        //                 payload: { response, dataId }
        //             })
        //         })
        //         .catch(error => {
        //             dispatch({
        //                 type: RECEIVE_DATA_ERROR,
        //                 payload: error
        //             })
        //         });
        // }
    };
};
