import React, { Fragment } from "react";

import { Row, Col, List, Icon, Typography, Tooltip, Tag } from "antd";

import { getRelativeTime } from "../../utils/misc";

const { Text } = Typography;

const CategoriesRow = ({ cat }) => {
    console.log("cat", cat);
    if (cat) {
        return (
            <div style={{ margin: "5px 0" }}>
                {cat.map(c => {
                    return (
                        <Tag key={c.id} color="geekblue">
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

export const ListItem = props => {
    const { properties, geometry } = props.item;
    const { dataSource } = properties;
    const relTime = properties.publishDate
        ? getRelativeTime(properties.publishDate)
        : null;

    // Indeed job source
    return (
        <Fragment>
            <List.Item.Meta
                // avatar={properties.logo ? <Avatar src={properties.logo} /> : null}

                title={
                    <Row>
                        <Col span={14}>
                            <Text
                                strong={dataSource === "gjm"}
                                ellipsis
                                style={{
                                    maxWidth: "200px",
                                    color:
                                        dataSource === "gjm"
                                            ? "black"
                                            : "inherit"
                                }}
                            >
                                {properties.title}
                            </Text>
                        </Col>
                        <Col
                            span={10}
                            style={{
                                fontSize: "12px",
                                textAlign: "right",
                                color:
                                    relTime.toLowerCase() === "today"
                                        ? "#0066ff"
                                        : "inherit"
                            }}
                        >
                            {relTime}
                        </Col>
                    </Row>
                }
                description={
                    <Fragment>
                        <Row>
                            <Col span={14}>
                                <Text
                                    ellipsis
                                    style={{
                                        maxWidth: "200px"
                                        // color:
                                        //     dataSource === "gjm"
                                        //         ? "black"
                                        //         : "initial"
                                    }}
                                >
                                    {properties.company}
                                </Text>
                            </Col>
                            <Col
                                span={10}
                                style={{ fontSize: "12px", textAlign: "right" }}
                            >
                                <Text
                                    ellipsis
                                    style={{
                                        maxWidth: "130px"
                                        // color: "initial"
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
                                <Row>
                                    <Col>{CategoriesRow(properties)}</Col>
                                </Row>
                                <Row style={{ lineHeight: "1em" }}>
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
                    </Fragment>
                }
            />
        </Fragment>
    );
};
