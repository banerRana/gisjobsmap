import React from "react";
import { Modal, Button, Icon } from "antd";

export const FaqModal = ({ visible, onClose }) => {
    return (
        <Modal
            title="Frequently Asked Questions"
            visible={visible}
            onClose={onClose}
            onCancel={onClose}
            footer={
                <Button key="close" onClick={onClose}>
                    OK
                </Button>
            }
        >
            <h3>How can I filter jobs by country?</h3>
            <p>
                To filter by country, use the country select within the{" "}
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
                feature. To remove this filter, use the &quot;Reset&quot; button
                located within this feature.
            </p>
            <p>
                This filter is automatically applied if only one country is
                visible on the map.
            </p>

            <p>
                A light blue highlight overlays the country indicating a filter
                is applied. This overlay is a simplified version of the country
                geometry.
            </p>

            <h3>Why aren&apos;t all jobs in the list visible on the map?</h3>
            <p>
                By default all jobs which allow remote work are listed in the
                sidebar for all countries in the map window. You can optionally
                exclude 100% remote jobs by choosing the &apos;Map Only&apos;
                option in the search menu.
            </p>

            <p>
                Some remote jobs are not mappable and therefore will only
                display in the list.
            </p>

            <h3>Why is there a maximum of 100 jobs listed at once?</h3>
            <p>
                A query limit is applied to maximize application performance.
                You can filter results by panning/zooming the map and applying
                search terms.
            </p>

            <h3>How are jobs ordered in the list?</h3>
            <p>All jobs are ordered by date posted, with most recent first.</p>

            <h3>Where is job data sourced from?</h3>
            <p>
                External job data is regularly updated from{" "}
                <a href="https://www.indeed.com">Indeed.com</a>.
            </p>

            <h3>How can I post a Job?</h3>
            <p>
                <a href="mailto:ishiland@gmail.com?subject=GIS%20Jobs%20Map%20posting">
                    Send a message
                </a>{" "}
                with job details. A suggested donation of $1/day is appreciated.
            </p>
            <h3>How can I donate?</h3>
            <p>
                Keep this site going! All donations go towards hosting and
                maintaining this site. Even the smallest amount is greatly
                appreciated!
            </p>
            <div
                style={{
                    textAlign: "center",
                    marginTop: ".3em",
                    marginBottom: "1em"
                }}
            >
                <form
                    action="https://www.paypal.com/cgi-bin/webscr"
                    method="post"
                    target="_blank"
                >
                    <input type="hidden" name="cmd" value="_s-xclick" />
                    <input
                        type="hidden"
                        name="hosted_button_id"
                        value="MAZV5KVWM7M6J"
                    />
                    <input
                        type="image"
                        src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif"
                        border="0"
                        name="submit"
                        title="PayPal - The safer, easier way to pay online!"
                        alt="Donate with PayPal button"
                    />
                    <img
                        alt=""
                        border="0"
                        src="https://www.paypal.com/en_US/i/scr/pixel.gif"
                        width="1"
                        height="1"
                    />
                </form>
            </div>
        </Modal>
    );
};
