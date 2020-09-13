import React, { useContext } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";

import { Layout, Icon } from "antd";

import { useWindowSize } from "../../hooks/useWindowSize";

import { SidebarCollapased } from "../SidebarCollapased";

import { SidebarOpened } from "../SidebarOpened";

import { toggleHighlightMarker } from "../../modules/highlightMarker";

import { SideBarContext } from "../../contexts/SidebarContext";

import { fetchData } from "../../modules/data";

import "./style.css";

const { Sider, Content, Footer } = Layout;

const SidebarContainer = ({
    children,
    fetchData: searchFetch,
    data,
    toggleHighlightMarker: toggleMarker
}) => {
    const windowSize = useWindowSize();
    const { isSidebarOpen, setSidebarOpen, isMobile } = useContext(
        SideBarContext
    );

    const getTriggerNode = () => {
        let nodeType = null;
        let nodeText = "";

        if (isSidebarOpen) {
            nodeType = "left";
            if (isMobile) {
                nodeText = " Show Map";
            } else {
                nodeText = " More Map";
            }
        } else {
            nodeType = "right";
        }
        return (
            <span>
                <Icon type={nodeType} />
                {nodeText}
            </span>
        );
    };

    return (
        <Sider
            collapsible
            collapsed={!isSidebarOpen}
            // onCollapse={() => setSidebarOpen(!isSidebarOpen)}
            width={windowSize < 700 ? windowSize.innerWidth : 375}
            style={{
                // position: windowSize.innerWidth < 700 ? "fixed" : "inherit",
                zIndex: "500",
                marginTop: "49px",
                minHeight: "calc(100% - 49px)",
                left: 0,
                // height: windowSize.innerHeight - 49,
                marginLeft: 0,
                //height: "calc(100vh - 49px)",
                boxShadow: "2px 1px 5px 0 rgba(0,0,0,.4)",
                overflow: "hidden"
            }}
            theme="light"
            breakpoint="lg"
            collapsedWidth="80"
            trigger={null}
        >
            <Layout style={{ height: "100%" }}>
                <Content
                    style={{
                        background: "#fff",
                        padding: 0,
                        margin: 0,
                        height: "100%"
                    }}
                >
                    {children}
                    {isSidebarOpen ? (
                        <SidebarOpened
                            // visibleCount={sidebar.visibleJobs.length}
                            data={data.features || []}
                            country={data.country}
                            near={data.near || {}}
                            fetchData={searchFetch}
                            isFetching={data.isFetching}
                            toggleHighlightMarker={toggleMarker}
                            // handleClick={(g)=>handleClick(g)}
                            // extent={() => goToExtent()}
                        />
                    ) : (
                        <SidebarCollapased
                            fetchData={searchFetch}
                            data={data.features || []}
                            country={data.country}
                            near={data.near || {}}
                            isFetching={data.isFetching}
                            // extent={() => goToExtent()}
                        />
                    )}
                </Content>
                <Footer
                    style={{
                        padding: "10px",
                        textAlign: "center",
                        borderTop: "1px solid #acacac",
                        cursor: "pointer",
                        background: "whitesmoke"
                    }}
                    onClick={() => setSidebarOpen(!isSidebarOpen)}
                >
                    {getTriggerNode()}
                </Footer>
            </Layout>
        </Sider>
    );
};

const mapStateToProps = ({ data }) => ({
    data
});

const mapDispatchToProps = dispatch =>
    bindActionCreators(
        {
            toggleHighlightMarker,
            fetchData
        },
        dispatch
    );

export default connect(mapStateToProps, mapDispatchToProps)(SidebarContainer);
