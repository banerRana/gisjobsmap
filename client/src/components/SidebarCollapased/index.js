import React from "react";
import {
    Row,
    Col,
    Layout,
    Button,
    Badge,
    Popover,
    Typography,
    Icon,
    Tooltip
} from "antd";

import { useRouter } from "../../hooks/useRouter";
import { WrappedJobSearchForm } from "../JobSearch";
import { getQueryCount } from "../../utils/routing";
import "./Mobile.css";

const { Text } = Typography;

export const SidebarCollapased = ({ country, isFetching, data, fetchData }) => {
    const router = useRouter();

    return (
        <Layout className="mobile-layout">
            {/* {props.children} */}
            <div>
                <Row
                    gutter={0}
                    style={{
                        padding: "15px 0"
                    }}
                >
                    <Col style={{ textAlign: "center" }}>
                        <Text strong style={{ fontSize: "small" }}>
                            Displaying
                        </Text>
                        <div
                            style={{
                                fontWeight: "600",
                                fontSize: "2em",
                                whiteSpace: "pre-wrap"
                            }}
                        >
                            {isFetching ? " " : data.length}
                        </div>
                        <Text strong style={{ fontSize: "small" }}>
                            jobs
                        </Text>
                    </Col>
                </Row>

                <Row style={{ textAlign: "center" }}>
                    <Badge
                        count={getQueryCount(router.query)}
                        style={{ background: "#1890ff" }}
                    >
                        <Popover
                            placement="right"
                            // title={<span>Search</span>}
                            content={
                                <WrappedJobSearchForm
                                    isFetching={isFetching}
                                    fetchData={(layer, obj) =>
                                        fetchData(layer, obj)
                                    }
                                />
                            }
                            trigger="click"
                        >
                            <Button
                                loading={isFetching}
                                type="ghost"
                                icon="search"
                                shape="circle"
                            />
                        </Popover>
                    </Badge>
                </Row>
                <Row
                    style={{
                        textAlign: "center",
                        marginTop: "20px"
                    }}
                >
                    <Col>
                        {country && country.iso2 ? (
                            <Tooltip
                                placement="right"
                                title={`Filtered by ${country.name}`}
                            >
                                <span
                                    style={{ height: "20px", width: "20px" }}
                                    className={`near-flag flag-icon flag-icon-${country.iso2.toLowerCase()}`}
                                />
                            </Tooltip>
                        ) : null}
                    </Col>
                </Row>
                <Row>
                    <Col
                        style={{
                            textAlign: "center",
                            marginTop: "25px"
                        }}
                    >
                        {!isFetching && data && data.length === 100 ? (
                            <Tooltip
                                placement="right"
                                title="Max 100 results. Narrow your search criteria or zoom in on the map."
                            >
                                <Icon
                                    type="info-circle"
                                    style={{
                                        fontSize: "18px"
                                    }}
                                />
                            </Tooltip>
                        ) : null}
                    </Col>
                </Row>
            </div>
        </Layout>
    );
};
