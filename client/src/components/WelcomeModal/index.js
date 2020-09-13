import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { Modal, Typography, Button, Row, Col, Divider, List, Icon } from "antd";

import { useRouter } from "../../hooks/useRouter";
import { getJobCounts } from "../../utils/http_functions";
import { parseJSON } from "../../utils/misc";
import { countries } from "../../config";
import { fetchData } from "../../modules/data";

const { Paragraph, Text, Title } = Typography;

// console.log("countries lenght", Object.keys(countries).length);

const WelcomeModal = ({ fetchData: searchFetch }) => {
    const router = useRouter();
    const { pathname, location } = router;
    const shouldDisplay = pathname === "/" && !location.search;
    const [jobCounts, setJobCounts] = useState([]);
    const [isFetching, setIsFetching] = useState(false);

    const [modalOpen, setModalOpen] = useState(shouldDisplay);
    useEffect(() => {
        if (shouldDisplay) {
            setIsFetching(true);
            getJobCounts()
                .then(parseJSON)
                .then(response => {
                    setJobCounts(response.data);
                    setIsFetching(false);
                })
                .catch(error => {
                    console.error("error getting job counts: ", error);
                    setIsFetching(false);
                });
        }
    }, []);

    const handleCountrySelect = val => {
        setModalOpen(false);
        searchFetch({ country: val });
        router.push({
            pathname: "/",
            search: `?country=${val}`
        });
    };
    return (
        <div>
            <Modal
                visible={modalOpen}
                footer={null}
                onCancel={() => setModalOpen(false)}
            >
                <Title level={3}>Welcome to The GIS Jobs Map</Title>
                <Paragraph>
                    <Text>Explore Geospatial jobs around the world! </Text>
                    <Text strong>Choose an option below to get started.</Text>
                </Paragraph>

                <div style={{ padding: "12px" }}>
                    <Button
                        type="primary"
                        block
                        onClick={() => setModalOpen(false)}
                    >
                        Browse All Countries
                    </Button>
                </div>
                <Divider>Or</Divider>
                <Paragraph style={{ textAlign: "center" }}>
                    <Text>Browse by most active countries</Text>
                </Paragraph>

                <List
                    loading={isFetching}
                    grid={{ sm: 2, xs: 1 }}
                    dataSource={jobCounts}
                    renderItem={count => (
                        <List.Item style={{ margin: "12px" }}>
                            <Button
                                block
                                key={count[0]}
                                onClick={() => handleCountrySelect(count[0])}
                            >
                                <span
                                    style={{ marginRight: "5px" }}
                                    className={`near-flag flag-icon flag-icon-${count[0].toLowerCase()}`}
                                />{" "}
                                <Text>
                                    {countries[count[0]]} ({count[1]})
                                </Text>
                            </Button>
                        </List.Item>
                    )}
                />
                <Row>
                    <Col style={{ textAlign: "center" }}>
                        <Text strong>
                            Over 50 more countries available using the{" "}
                            <span
                                style={{
                                    textAlign: "center",
                                    border: "1px solid rgb(217, 217, 217)",
                                    height: "25px",
                                    width: "25px",
                                    padding: "2px",
                                    display: "inline-block",
                                    borderRadius: "50%",
                                    MozBorderRadius: "50%",
                                    WebkitBorderRadius: "50%"
                                }}
                            >
                                <Icon type="search-o" />
                            </span>{" "}
                            button.
                        </Text>
                    </Col>
                </Row>
            </Modal>
        </div>
    );
};

const mapStateToProps = ({ data }) => ({
    data
});

const mapDispatchToProps = dispatch =>
    bindActionCreators(
        {
            fetchData
        },
        dispatch
    );

export default connect(mapStateToProps, mapDispatchToProps)(WelcomeModal);
