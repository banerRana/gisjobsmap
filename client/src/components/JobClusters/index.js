import React from "react";
import { Marker, Tooltip } from "react-leaflet";

import MarkerClusterGroup from "../MarkerClusterGroup";

export const JobClusters = ({ mapFeatures, markerClick }) => {
    return (
        <MarkerClusterGroup chunkedLoading chunkInterval={100}>
            {mapFeatures &&
                mapFeatures.map(item => {
                    if (item.geometry && !item.properties.invalidGeom) {
                        return (
                            <Marker
                                onClick={e => markerClick(e)}
                                key={item.properties.slug}
                                title={item.properties.title}
                                publishDate={item.properties.publishDate}
                                company={item.properties.company}
                                formattedLocation={
                                    item.properties.formattedLocation
                                }
                                slug={item.properties.slug}
                                country={item.properties.country}
                                position={[
                                    item.geometry.coordinates[1],
                                    item.geometry.coordinates[0]
                                ]}
                            >
                                <Tooltip
                                    label={item.properties.title}
                                    direction="top"
                                >
                                    <span>{item.properties.title}</span>
                                </Tooltip>
                            </Marker>
                        );
                    }
                    return null;
                })}
        </MarkerClusterGroup>
    );
};
