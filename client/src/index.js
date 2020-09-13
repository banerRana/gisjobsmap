import React from "react";
import { render } from "react-dom";
import { Provider } from "react-redux";
import { Route, Switch } from "react-router";
import { ConnectedRouter } from "connected-react-router";
import { PersistGate } from "redux-persist/integration/react";
import ReactGA from "react-ga";

import "./polyfills";
import configureStore, { history } from "./store";
import App from "./components/App";

import "./index.css";

const { persistor, store } = configureStore(/* provide initial state if any */);

const target = document.querySelector("#root");

// Google Analytics
if (process.env.NODE_ENV !== "development") {
    ReactGA.initialize("UA-71564480-1");
    ReactGA.pageview(window.location.pathname + window.location.search);
    history.listen((location, action) => {
        ReactGA.set({ page: location.pathname, action });
        ReactGA.pageview(location.pathname);
    });
} else {
    console.log("Google Analytics disabled"); // eslint-disable-line no-console
}

render(
    <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
            <ConnectedRouter history={history}>
                <Switch>
                    <Route path="/:layer?/:slug?" component={App} />
                    {/* <Route path="/job/:slug?" component={App} /> */}
                    {/* <Redirect from="*" to="/map" component={App} /> */}
                </Switch>
            </ConnectedRouter>
        </PersistGate>
    </Provider>,
    target
);
