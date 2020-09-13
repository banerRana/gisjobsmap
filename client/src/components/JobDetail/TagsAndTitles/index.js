import React from "react";
import { Tag } from "antd";

export const Tags = props => (
    <div style={{ marginBottom: "10px" }}>
        {props.data.map(item => {
            return (
                <Tag key={item.id} color="geekblue">
                    {item.name}
                </Tag>
            );
        })}
    </div>
);

export const Titles = props => (
    <div style={{ marginBottom: "15px" }}>
        <span style={{ marginRight: "5px" }}>Categorized as</span>
        {props.data.map(item => {
            return (
                <Tag key={item.id} color="orange">
                    {item.name}
                </Tag>
            );
        })}
    </div>
);
