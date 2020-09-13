import React, { useState, useEffect, useRef } from "react";
import InfiniteScroll from "react-infinite-scroller";
import {
    Layout,
    Row,
    Button,
    Col,
    Typography,
    Tooltip,
    List,
    Spin,
    Icon,
    Badge,
    Popover
} from "antd";

import { WrappedJobSearchForm } from "../JobSearch";
import { NearestCity } from "../NearestCity";
import { getQueryCount } from "../../utils/routing";

import { useRouter } from "../../hooks/useRouter";

import "./style.css";

import ListJobs from "../ListJobs";

const { Text } = Typography;

export const SidebarOpened = ({
    data,
    country,
    near,
    fetchData,
    isFetching,
    toggleHighlightMarker,
    handleClick
}) => {
    const router = useRouter();

    const infiniteParentRef = useRef(null);

    const scrollAmount = 20;

    const [listData, setListData] = useState([]);

    const [listIdx, setListIdx] = useState(scrollAmount);

    const handleInfiniteOnLoad = () => {
        if (listData.length >= data.length) {
            return;
        }
        if (data.length) {
            setListData(
                listData.concat(data.slice(listIdx + 1, listIdx + scrollAmount))
            );
            setListIdx(listIdx + scrollAmount);
        }
    };

    useEffect(() => {
        if (!isFetching) {
            if (infiniteParentRef && infiniteParentRef.current) {
                infiniteParentRef.current.scrollTop = 0;
            }
            setListIdx(scrollAmount);
            setListData(data.slice(0, scrollAmount + 1));
        }
    }, [isFetching]);

    return (
        <Layout style={{ height: "100%", minHeight: "100%" }}>
            <Row
                gutter={0}
                style={{
                    padding: "8px 0",
                    // marginTop: '3px',
                    backgroundColor: "whitesmoke",
                    boxShadow: "rgb(172, 172, 172) 0px 1px 4px 1px",
                    zIndex: "1",
                    minHeight: "75px"
                }}
            >
                <Row style={{ padding: "5px" }}>
                    <Col span={19} style={{ textAlign: "center" }}>
                        <Row gutter={0}>
                            <Col span={24}>
                                {!isFetching && data && data.length === 100 ? (
                                    <Tooltip
                                        placement="bottom"
                                        title="Max 100 results. Narrow your search criteria or zoom in on the map."
                                    >
                                        <Icon
                                            type="info-circle"
                                            style={{
                                                // color: "orange",
                                                margin: "0 10px",
                                                fontSize: "18px",
                                                verticalAlign: "text-bottom"
                                            }}
                                        />
                                    </Tooltip>
                                ) : null}

                                {!isFetching && (
                                    <Text
                                        style={{
                                            fontSize: "medium",
                                            fontWeight: 500
                                        }}
                                    >
                                        Displaying{" "}
                                        {data && data.length ? data.length : 0}{" "}
                                        jobs
                                    </Text>
                                )}
                            </Col>
                            <Col span={24} style={{ marginTop: "5px" }}>
                                <NearestCity
                                    country={country}
                                    near={near}
                                    isFetching={isFetching}
                                />
                            </Col>
                        </Row>
                    </Col>
                    <Col
                        span={5}
                        style={{
                            textAlign: "center",
                            marginTop: "10px"
                        }}
                    >
                        <Badge
                            count={getQueryCount(router.query)}
                            style={{ background: "#1890ff" }}
                        >
                            <Popover
                                placement="right"
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
                                    icon="search"
                                    shape="circle"
                                />
                            </Popover>
                        </Badge>
                    </Col>
                </Row>
            </Row>
            <div
                style={{
                    overflowY: "scroll",
                    height: "100%"
                    // background: "white"
                }}
                ref={infiniteParentRef}
            >
                {isFetching && (
                    <div className="list-loading-container">
                        <Spin />
                    </div>
                )}
                <InfiniteScroll
                    initialLoad={false}
                    pageStart={0}
                    loadMore={handleInfiniteOnLoad}
                    hasMore={listData.length < data.length}
                    useWindow={false}
                >
                    <List
                        dataSource={listData}
                        locale={{
                            emptyText: (
                                <span>
                                    {isFetching
                                        ? "Please wait..."
                                        : "No results found here."}
                                </span>
                            )
                        }}
                        renderItem={item => (
                            <ListJobs
                                item={item}
                                handleClick={handleClick}
                                handleMapHighlight={toggleHighlightMarker}
                            />
                        )}
                    />
                </InfiniteScroll>
            </div>
        </Layout>
    );
};
