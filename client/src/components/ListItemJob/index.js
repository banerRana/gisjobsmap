import React, { Fragment } from "react";

import { Row, Col, List, Icon, Typography, Tooltip, Tag, Card } from "antd";
import "./style.css";

import { getRelativeTime } from "../../utils/misc";

const { Text } = Typography;

const CategoriesRow = ({ cat }) => {
    if (cat) {
        return (
            <div>
                {cat.map(c => {
                    return (
                        <Tag key={c.id} color="#40a9ff">
                            {c.name}
                        </Tag>
                    );
                })}
            </div>
        );
    } else {
        return null;
    }
};

export const ListItemJob = props => {
    const { properties, geometry } = props.item;
    const { dataSource, categories } = properties;
    const relTime = properties.publishDate
        ? getRelativeTime(properties.publishDate)
        : null;

    return (
        // <div style={{ background: "#ECECEC", padding: "30px" }}>
        <Row style={{ width: "100%", marginBottom: "10px" }}>
            <Col span={24}>
                <Card
                    style={{ background: "transparent" }}
                    bodyStyle={{ paddingBottom: "0" }}
                    size="small" //{dataSource === "gjm" ? "default" : "small"}
                    title={properties.title}
                    bordered={false}
                    extra={
                        <span
                            style={{
                                color:
                                    relTime.toLowerCase() === "today"
                                        ? "#0066ff"
                                        : "inherit"
                            }}
                        >
                            {relTime}
                        </span>
                    }
                    headStyle={{ border: "none" }}
                >
                    <Row>
                        <Col span={14}>
                            <Text
                                ellipsis
                                style={{
                                    maxWidth: "130px"
                                }}
                            >
                                {" "}
                                {properties.company}
                            </Text>
                        </Col>
                        <Col
                            span={10}
                            style={{
                                textAlign: "right"
                            }}
                        >
                            <Text
                                ellipsis
                                style={{
                                    maxWidth: "120px"
                                }}
                            >
                                {properties.isRemote ? (
                                    <span>
                                        <Tooltip title="Remote">
                                            <Icon type="home-o" /> Remote
                                        </Tooltip>
                                    </span>
                                ) : null}
                                {geometry && !properties.invalidGeom ? (
                                    <span>
                                        <Icon type="environment-o" />{" "}
                                        {properties.formattedLocation}
                                    </span>
                                ) : null}
                            </Text>
                        </Col>
                    </Row>

                    {dataSource === "gjm" ? (
                        <Fragment>
                            <Row style={{ paddingTop: "12px" }}>
                                <Col>
                                    <CategoriesRow cat={categories} />
                                </Col>
                            </Row>
                            <Row
                                style={{
                                    lineHeight: "1em",
                                    paddingTop: "12px"
                                }}
                            >
                                <Col
                                    span={24}
                                    style={{
                                        textAlign: "center",
                                        fontSize: "x-small",
                                        lineHeight: "1em"
                                        // color: "black"
                                    }}
                                >
                                    sponsored listing
                                </Col>
                            </Row>
                        </Fragment>
                    ) : null}
                </Card>
            </Col>
        </Row>
        // </div>
    );
};
