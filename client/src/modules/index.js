import { combineReducers } from "redux";
import { connectRouter } from "connected-react-router";

import data from "./data";
import detail from "./detail";
import geocode from "./geocode";
import highlightMarker from "./highlightMarker";
import tags from "./tags";
import categories from "./categories";

export default history =>
    combineReducers({
        router: connectRouter(history),
        data,
        detail,
        geocode,
        highlightMarker,
        tags,
        categories,
    });
