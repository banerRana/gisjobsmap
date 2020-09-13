import React from "react";
import { Select } from "antd";

import "flag-icon-css/css/flag-icon.css";
import { countries } from "../../config";

export const CountrySelect = () => {
    return (
        <Select>
            {Object.keys(countries).map(key => {
                return (
                    <Select.Option key={key} value={key}>
                        <span className={`flag-icon flag-icon-${key}`} />{" "}
                        {countries[key]}
                    </Select.Option>
                );
            })}
            <Select.Option key="other" value="other">
                Other
            </Select.Option>
        </Select>
    );
};
