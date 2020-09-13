import React, { Fragment } from "react";
import "flag-icon-css/css/flag-icon.css";
import { Tooltip, Typography } from "antd";
import { countries } from "../../config";

const { Text } = Typography;

export const NearestCity = ({ country, near, isFetching }) => {
    const { properties } = near;
    if (!properties && !isFetching && !country.name) {
        return (
            <Fragment>
                <Text type="secondary" style={{ fontSize: "small" }}>
                    Searching all countries in map window
                </Text>
            </Fragment>
        );
    } else if (properties && properties.name && !isFetching) {
        return (
            <Fragment>
                <Text
                    type="secondary"
                    style={{ fontSize: "small", maxWidth: "260px" }}
                    ellipsis
                >
                    Near {`${properties.name}, ${properties.admin1}`}
                </Text>
                <Tooltip
                    placement="bottom"
                    title={`Filtered by ${
                        countries[properties.iso2.toLowerCase()]
                    }`}
                >
                    {" "}
                    <span
                        style={{ verticalAlign: "text-top" }}
                        className={`near-flag flag-icon flag-icon-${properties.iso2.toLowerCase()}`}
                    />
                </Tooltip>
            </Fragment>
        );
    } else if (!properties && country.name && !isFetching) {
        return (
            <Fragment>
                <Text type="secondary" style={{ fontSize: "small" }}>
                    Filtered by {"  "}
                    {country.name}{" "}
                    <span
                        className={`near-flag flag-icon flag-icon-${country.iso2.toLowerCase()}`}
                    />
                </Text>
            </Fragment>
        );
    } else {
        return null;
    }
};
