import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { Modal, Icon, Typography, Divider, Button } from "antd";

import { useRouter } from "../../hooks/useRouter";
import { fetchDetail, closeDetail } from "../../modules/detail";
import { Header } from "../JobDetail/Header";
import { Share } from "./Share";
import "./style.css";

const { Paragraph, Text } = Typography;

const JobDetail = ({ detail, closeDetail, fetchDetail }) => {
    const router = useRouter();

    const [pageTitle, setPageTitle] = useState("The GIS Jobs Map");

    const { match } = router;
    const { isFetching, data, slug } = detail;

    const {
        url,
        description,
        formattedLocation,
        dataSource,
        company,
        publishDate,
        tags,
        categories,
        title,
        isRemote,
        isActive,
        countryCode,
        invalidGeom
    } = data.properties;

    useEffect(() => {
        if (!slug && match.params.layer === "job" && match.params.slug) {
            fetchDetail(match.params.slug);
        }
    }, []);

    useEffect(() => {
        if (slug && title) {
            router.push({
                pathname: `/job/${slug}`,
                search: router.location.search
            });
            setPageTitle(title);
        }
    }, [slug, title]);

    const closeModal = () => {
        router.push({ pathname: `/`, search: router.location.search });
        setPageTitle("The GIS Jobs Map");
        closeDetail();
    };

    return (
        <Modal
            title={null}
            visible={slug ? true : false}
            onCancel={() => closeModal()}
            // bodyStyle={{ paddingTop: "50px" }}
            footer={null}
            style={{
                minWidth: "50vw"
                //maxWidth: "800px"
            }}
        // width="calc(100vw - 40rem)"
        >
            {isFetching ? (
                <div className="loading-div">
                    <Icon type="loading" /> Loading
                </div>
            ) : (
                    <>
                        <Header
                            title={title}
                            company={company}
                            publishDate={publishDate}
                            countryCode={countryCode}
                            formattedLocation={formattedLocation}
                            source={dataSource}
                            url={url}
                            tags={tags}
                            categories={categories}
                            isRemote={isRemote}
                            invalidGeom={invalidGeom}
                        />
                        <Divider />

                        <Share slug={slug} title={title} tags={tags} />

                        <Paragraph className="job-description">
                            {!isActive && (
                                <div
                                    style={{
                                        color: "red",
                                        textAlign: "center",
                                        fontSize: "large"
                                    }}
                                >
                                    This job posting is no longer active
                                </div>
                            )}
                            {description}
                        </Paragraph>
                        <div>
                            {url && (
                                <div
                                    style={{ textAlign: "center", margin: "10px" }}
                                >
                                    <a
                                        href={url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        <Button block type="link" size="large">
                                            <Icon type="link-o" />
                                            {dataSource === "indeed"
                                                ? " View on Indeed"
                                                : " More Information"}
                                        </Button>
                                    </a>
                                </div>
                            )}
                        </div>
                    </>
                )}
        </Modal>
    );
};

const mapStateToProps = ({ detail }) => ({
    detail
});

const mapDispatchToProps = dispatch =>
    bindActionCreators(
        {
            fetchDetail,
            closeDetail
        },
        dispatch
    );

export default connect(mapStateToProps, mapDispatchToProps)(JobDetail);
