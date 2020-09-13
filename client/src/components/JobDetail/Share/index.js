import React from "react";
import { Tag, Icon, Input, Col, Row, Typography } from "antd";

const { Text } = Typography;

export const Share = ({ slug, title, tags }) => {
    // const [copyIcon, setCopyIcon] = useState("link-o");

    // const doLinkCopy = link => {
    //     const { clipboard } = navigator;
    //     if (clipboard) {
    //         navigator.clipboard.writeText(link);
    //         setCopyIcon("check-o");
    //         setTimeout(() => {
    //             setCopyIcon("link-o");
    //         }, 1000);
    //     }
    // };

    const baseUrl = window.location.origin;
    const shareLink = `${baseUrl}/job/${slug}`;
    const hashTags = tags.length ? tags.map(item => item.name).join(",") : "";

    const twitterShareLink =
        `https://twitter.com/intent/tweet` +
        `?url=${encodeURIComponent(shareLink)}` +
        `&text=${encodeURIComponent(title)}` +
        `&hashTags=${encodeURIComponent(hashTags)}`;

    // const facebookShareLink =
    //     `https://www.facebook.com/sharer.php` +
    //     `?u=${encodeURIComponent(shareLink)}`;

    // const linkedInShareLink =
    //     `https://www.linkedin.com/shareArticle` +
    //     `?mini=true` +
    //     `&url=${encodeURIComponent(shareLink)}` +
    //     `&title=${encodeURIComponent(title)}` +
    //     `&summary=${encodeURIComponent(hashTags)}` +
    //     `&source=${encodeURIComponent("The GIS Jobs Map")}`;
    // const linkedInShareLink =
    //     `https://www.linkedin.com/sharing/share-offsite/` +
    //     `?url=${encodeURIComponent(shareLink)}`;

    return (
        <Row>
            <Col span={24} style={{ display: "inline-flex", height: "23px" }}>
                <span style={{ marginRight: "5px" }}>Share</span>
                <Tag color="#55acee">
                    <a
                        href={twitterShareLink}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <Icon type="twitter-o" color="white" />
                    </a>
                </Tag>
                {/* <Tag color="#3b5999">
                <a
                    href={facebookShareLink}
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <Icon type="facebook-o" color="white" />{" "}
                </a>
            </Tag> */}
                {/* <Tag color="#0077b5">
                <a
                    href={linkedInShareLink}
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <Icon type="linkedin-o" color="white" />
                </a>
            </Tag> */}
                <Tag>
                    <a
                        href={`mailto:?subject=${title}%20Job&body=Check out this job from the GIS Jobs Map: \r \n ${encodeURIComponent(
                            shareLink
                        )}`}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <Icon type="mail-o" color="white" />
                    </a>
                </Tag>
                <Text
                    copyable={{ text: shareLink }}
                    style={{
                        display: "inherit",
                        width: "100%"
                    }}
                >
                    <Input
                        size="small"
                        placeholder=""
                        value={shareLink}
                        style={{
                            width: "-webkit-fill-available",
                            maxWidth: "300px"
                        }}
                    />
                </Text>
                {/* <Input
                        size="small"
                        placeholder=""
                        value={shareLink}
                        style={{
                            width: "-webkit-fill-available",
                            maxWidth: "300px"
                        }}
                        prefix={
                            <Icon
                                type={copyIcon}
                                color={
                                    copyIcon === "check-o" ? "green" : "inherit"
                                }
                            />
                        }
                    /> */}
                {/* <Button size="small" onClick={() => doLinkCopy(shareLink)}>
                        Copy
                    </Button> */}
                {/* </div> */}
            </Col>
        </Row>
    );
};
