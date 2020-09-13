import React from "react";
import { Layout } from "antd";

import SidebarContainer from "../SidebarContainer";
import JobDetail from "../JobDetail";

import LeafletMap from "../LeafletMap";
import Navbar from "../Navbar";
import WelcomeModal from "../WelcomeModal";

import SidebarContextProvider from "../../contexts/SidebarContext";
import JobDetailContextProvider from "../../contexts/JobDetailContext";

import "./App.css";

const App = () => (
    <Layout className="App">
        <WelcomeModal />
        <Navbar />
        <Layout style={{ height: "100%" }}>
            <JobDetailContextProvider>
                <SidebarContextProvider>
                    <SidebarContainer />
                    <LeafletMap />
                </SidebarContextProvider>
            </JobDetailContextProvider>
            <JobDetail />
        </Layout>
    </Layout>
);
export default App;
