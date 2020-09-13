import React from "react";
import { countries } from "../../../config";
import { getRelativeTime } from "../../../utils/misc";

import { Icon, Row, Col, Typography, Tag } from "antd";

const { Text } = Typography;

export const Header = props => {
    const {
        isRemote,
        countryCode,
        formattedLocation,
        tags,
        invalidGeom
    } = props;

    let relTime = getRelativeTime(props.publishDate).toLowerCase();
    if (props.title) {
        return (
            <div style={{ margin: "5px" }}>
                <Row>
                    <Col span={24}>
                        <h1>{props.title}</h1>
                    </Col>
                </Row>
                <Row>
                    <Col span={24}>
                        <h2>{props.company}</h2>
                    </Col>
                </Row>
                <Row gutter={[16, 16]}>
                    <Col span={24} style={{ fontSize: "small" }}>
                        {formattedLocation && !invalidGeom ? (
                            <Text>
                                <Icon type="environment-o" />{" "}
                                {formattedLocation}
                            </Text>
                        ) : null}
                        {formattedLocation && !invalidGeom && isRemote && " - "}
                        {isRemote ? (
                            <Text>
                                <Icon type="home" /> Remote
                            </Text>
                        ) : null}{" "}
                        - {countries[countryCode.toLowerCase()]}
                    </Col>
                </Row>
                <Row gutter={[16, 16]}>
                    <Col span={24} style={{ fontSize: "small" }}>
                        <Text>
                            <Icon type="clock-circle" /> Posted {relTime}
                        </Text>
                    </Col>
                </Row>
                {}
                {tags.length ? (
                    <Row gutter={[16, 16]}>
                        <Col span={24}>
                            <div style={{ lineHeight: "2em" }}>
                                {/* {categories.length
                                    ? props.categories.map(item => {
                                          return (
                                              <Tag key={item.id}>
                                                  {item.name}
                                              </Tag>
                                          );
                                      })
                                    : null} */}
                                {props.tags.map(item => {
                                    return (
                                        <Tag key={item.id} color="geekblue">
                                            {item.name}
                                        </Tag>
                                    );
                                })}
                            </div>
                        </Col>
                    </Row>
                ) : null}
                {/* {props.url && (
                    <Row gutter={[16, 16]}>
                        <Col span={24}>
                            <a
                                href={props.url}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                <Button type="link" size="small">
                                    <Icon type="link-o" />
                                    {source === "indeed"
                                        ? " View on Indeed"
                                        : " More Information"}
                                </Button>
                            </a>
                        </Col>
                    </Row>
                )} */}
            </div>
        );
    }
};
