export const HIGHLIGHT_MARKER_REQUEST =
    "highlightMarker/HIGHLIGHT_MARKER_REQUEST";
export const CLEAR_MARKER_REQUEST = "highlightMarker/CLEAR_MARKER_REQUEST";

const initialState = {
    geometry: {},
    title: ""
};

// reducer
export default (state = initialState, action) => {
    switch (action.type) {
        case HIGHLIGHT_MARKER_REQUEST:
            return {
                ...state,
                geometry: action.payload.geometry,
                title: action.payload.title
            };

        case CLEAR_MARKER_REQUEST:
            return {
                ...state,
                geometry: {},
                title: ""
            };
        default:
            return state;
    }
};

// action
export const toggleHighlightMarker = (geometry, title) => {
    return dispatch => {
        if (geometry) {
            dispatch({
                type: HIGHLIGHT_MARKER_REQUEST,
                payload: { geometry, title }
            });
        } else {
            dispatch({
                type: CLEAR_MARKER_REQUEST
            });
        }
    };
};
