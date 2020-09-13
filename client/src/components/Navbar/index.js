import React, { useState, useMemo, useContext } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { Layout, Menu, Icon, Button } from "antd";
import "flag-icon-css/css/flag-icon.css";

import { fetchGeocodeResults, setGeocodeResults } from "../../modules/geocode";
import { fetchData } from "../../modules/data";

import { FaqModal } from "../FaqModal";

import "./Navbar.css";

const Navbar = () => {
    const [FaqModalVisible, setFaqModalVisible] = useState(false);

    const handleMenuClick = (e) => {
        const { key } = e;
        if (key) {
            if (key.indexOf("faq") > -1) {
                setFaqModalVisible(true);
            } else if (key.indexOf("twitter") > -1) {
                window.open("https://twitter.com/gisjobsmap");
            } else if (key.indexOf("issue") > -1) {
                window.open(
                    "https://github.com/ishiland/gisjobsmap/issues/new"
                );
            } else if (key.indexOf("github") > -1) {
                window.open("https://github.com/ishiland/gisjobsmap");
            }
        }
    };

    // memoized to prevent unnecessary re-rendering
    const faqMemo = useMemo(() => {
        return (
            <FaqModal
                visible={FaqModalVisible}
                onClose={() => setFaqModalVisible(false)}
            />
        );
    }, [FaqModalVisible]);

    return (
        <Layout.Header
            className="header"
            style={{
                background: "white",
                padding: "0",
                position: "fixed",
                zIndex: 600,
                width: "100%",
                height: "51px"
            }}
        >
            <div className="logo" />
            <Menu
                theme="light"
                mode="horizontal"
                style={{
                    lineHeight: "64px",
                    height: "50px",
                    width: "65px",
                    float: "right"
                }}
                onClick={(e) => handleMenuClick(e)}
                selectedKeys={[]}
                key="nav"
            >
                {faqMemo}

                <Menu.SubMenu
                    key="submenu"
                    expandIcon={<Icon type="menu" />}
                    style={{
                        lineHeight: "54px",
                        float: "right",
                        height: "49px",
                        paddingLeft: "0px"
                    }}
                    title={
                        <span>
                            <Icon type="menu" style={{ marginRight: "5px" }} />
                        </span>
                    }
                >
                    <Menu.Item
                        key="twitter"
                        className="navMenuItem"
                        style={{ padding: "0 10px !important" }}
                    >
                        <span>
                            <Icon type="twitter-o" style={{ color: "black" }} />
                            Follow
                        </span>
                    </Menu.Item>
                    <Menu.Item
                        key="faq"
                        className="navMenuItem"
                        style={{ padding: "0 10px !important" }}
                    >
                        <span>
                            <Icon
                                type="question-circle"
                                style={{ color: "black" }}
                            />
                            FAQ
                        </span>
                    </Menu.Item>
                    <Menu.Item
                        key="issue"
                        className="navMenuItem"
                        style={{ padding: "0 10px !important" }}
                    >
                        <span>
                            <Icon type="edit" style={{ color: "black" }} />
                            Report Issue
                        </span>
                    </Menu.Item>
                    <Menu.Item
                        key="github"
                        className="navMenuItem"
                        style={{ padding: "0 10px !important" }}
                    >
                        <span>
                            <Icon type="github-o" style={{ color: "black" }} />
                            Contribute
                        </span>
                    </Menu.Item>
                </Menu.SubMenu>
            </Menu>
            <div
                style={{
                    float: "right",
                    lineHeight: "53px",
                    marginRight: "10px"
                }}
            ></div>
        </Layout.Header>
    );
};

const mapStateToProps = ({ highlightLayer, data }) => ({
    highlightLayer,
    data
});

const mapDispatchToProps = (dispatch) =>
    bindActionCreators(
        {
            fetchGeocodeResults,
            setGeocodeResults,
            fetchData
        },
        dispatch
    );

export default connect(mapStateToProps, mapDispatchToProps)(Navbar);
