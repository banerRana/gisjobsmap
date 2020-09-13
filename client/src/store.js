import { createStore, applyMiddleware, compose } from "redux";
import { routerMiddleware } from "connected-react-router";
import thunk from "redux-thunk";
import { persistStore, persistReducer } from "redux-persist";
// import hardSet from "redux-persist/lib/stateReconciler/hardSet";
import storage from "redux-persist/lib/storage";
import { createLogger } from "redux-logger";

import createRootReducer from "./modules";

const createHistory = require("history").createBrowserHistory;

export const history = createHistory();

// not currently utilized
const persistConfig = {
    key: "root",
    storage,
    // stateReconciler: hardSet,
    whitelist: []
    // whitelist: []
    // blacklist: ["router", "data", "detail"]
};

const persistedReducer = persistReducer(
    persistConfig,
    createRootReducer(history)
);

const enhancers = []; // TODO: not setup properly
const middleware = [thunk, routerMiddleware(history)];

if (process.env.NODE_ENV === "development") {
    const devToolsExtension = window.__REDUX_DEVTOOLS_EXTENSION__;
    if (typeof devToolsExtension === "function") {
        enhancers.push(devToolsExtension());
    }
    const logger = createLogger({
        collapsed: true
    });
    middleware.push(logger);
}

export default function configureStore(preloadedState) {
    const store = createStore(
        persistedReducer, // root reducer with router state
        preloadedState,
        compose(
            applyMiddleware(
                routerMiddleware(history), // for dispatching history actions
                ...middleware
                // ... other middlewares ...
            )
        )
    );
    const persistor = persistStore(store);

    return { persistor, store };
}
