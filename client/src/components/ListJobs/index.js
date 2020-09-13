import React from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";

import { List } from "antd";

import { getRelativeTime } from "../../utils/misc";
import { fetchDetail } from "../../modules/detail";
import { ListItem } from "../ListItem";
import { ListItemJob } from "../ListItemJob";

const ListJobs = props => {
    const handleClick = slug => {
        props.fetchDetail(slug);
    };
    const { item } = props;
    const { properties, geometry } = item;
    const { dataSource } = properties;
    const relTime = properties.publishDate
        ? getRelativeTime(properties.publishDate)
        : null;

    const { title } = properties;

    if (relTime) {
        return (
            <List.Item
                className="data-list-item"
                key={properties.slug}
                onMouseEnter={() => props.handleMapHighlight(geometry, title)}
                onMouseLeave={() => props.handleMapHighlight()}
                onClick={() => handleClick(properties.slug)}
            >
                <ListItemJob item={item} />
            </List.Item>
        );
    }

    return <div />;
};

const mapStateToProps = ({ detail }) => ({
    detail
});

const mapDispatchToProps = dispatch =>
    bindActionCreators(
        {
            fetchDetail
        },
        dispatch
    );

export default connect(mapStateToProps, mapDispatchToProps)(ListJobs);
