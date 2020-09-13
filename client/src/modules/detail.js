import { getJobDetail } from "../utils/http_functions";
import { parseJSON } from "../utils/misc";

export const FETCH_DETAIL_REQUEST = "detail/FETCH_DETAIL_REQUEST";
export const RECEIVE_DETAIL = "detail/RECEIVE_DETAIL";
export const RECEIVE_DETAIL_ERROR = "detail/RECEIVE_DETAIL_ERROR";
export const CLOSE_DETAIL = "detail/CLOSE_DETAIL";

const initialState = {
    isFetching: false,
    dataId: null,
    slug: null,
    data: { geometry: {}, properties: {} },
    error: { status: false, response: null }
};

// reducer
export default (state = initialState, action) => {
    switch (action.type) {
        case FETCH_DETAIL_REQUEST:
            return {
                ...initialState,
                isFetching: true,
                dataId: action.payload.dataId,
                slug: action.payload.slug,
                error: { status: false, response: null }
            };

        case RECEIVE_DETAIL:
            if (state.dataId === action.payload.dataId) {
                return {
                    ...state,
                    isFetching: false,
                    data: action.payload.data
                };
            }
            return state;

        case RECEIVE_DETAIL_ERROR:
            return {
                ...state,
                isFetching: false,
                error: { status: true, response: action.payload }
            };

        case CLOSE_DETAIL:
            return {
                ...state,
                isFetching: false,
                dataId: null,
                slug: null
            };
        default:
            return state;
    }
};

// action
export const fetchDetail = slug => {
    // const jobId = jobData.id;
    // const { slug } = jobData;
    return dispatch => {
        const dataId = Math.random();

        dispatch({
            type: FETCH_DETAIL_REQUEST,
            payload: { dataId, slug }
        });
        // if (layer === "jobs") {
        getJobDetail({ slug })
            .then(parseJSON)
            .then(response => {
                const { data } = response;
                dispatch({
                    type: RECEIVE_DETAIL,
                    payload: { data, dataId }
                });
            })
            .catch(error => {
                dispatch({
                    type: RECEIVE_DETAIL_ERROR,
                    payload: error
                });
            });
        // }
        // else if (layer === "organizations") {
        //   getOrganizationDetail({ slug })
        //     .then(parseJSON)
        //     .then(response => {
        //       const { results } = response;
        //       dispatch({
        //         type: RECEIVE_DETAIL,
        //         payload: { results, dataId }
        //       });
        //     })
        //     .catch(error => {
        //       dispatch({
        //         type: RECEIVE_DETAIL_ERROR,
        //         payload: error
        //       });
        //     });
        // }
    };
};

// action
export const closeDetail = () => {
    return dispatch => {
        dispatch({
            type: CLOSE_DETAIL
        });
    };
};
