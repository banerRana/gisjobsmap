import React, { useEffect, useState, useRef, useMemo, useContext } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
// import bbox from "@turf/bbox";
// import { multiPoint, lineString } from "@turf/helpers";
import {
    Map,
    TileLayer,
    ZoomControl,
    FeatureGroup,
    CircleMarker,
    GeoJSON,
    AttributionControl
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./map.css";

import {
    boxQueryToArray,
    shortenBoxUrlParam,
    stringifyQueryParams,
    validateSearches,
    hasCountryPath
} from "../../utils/routing";
import { basemapProvider } from "../../config";
import { fetchData } from "../../modules/data";
import { fetchDetail } from "../../modules/detail";

import { toggleHighlightMarker } from "../../modules/highlightMarker";

import { useRouter } from "../../hooks/useRouter";
import { SideBarContext } from "../../contexts/SidebarContext";
import { JobClusters } from "../JobClusters";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
    iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"), // eslint-disable-line global-require
    iconUrl: require("leaflet/dist/images/marker-icon.png"), // eslint-disable-line global-require
    shadowUrl: require("leaflet/dist/images/marker-shadow.png") // eslint-disable-line global-require
});

const initialBounds = "-138.52,-59.71,179.65,74.40";

// let firstStart = true;
// let countrySwitch = false;
// let hasJobDetailOnload = false;

const LeafletMap = ({
    detail,
    data,
    fetchData,
    fetchDetail,
    highlightMarker
}) => {
    const router = useRouter();
    const { match, query } = router;
    const box = query.box ? query.box : initialBounds;

    const { isSidebarOpen, isMobile } = useContext(SideBarContext);
    // eslint-disable-next-line no-unused-vars
    const mapBounds = boxQueryToArray(box);
    console.log("mapBounds", mapBounds);
    // const [mapBounds, setMapBounds] = useState(boxQueryToArray(box));
    const [hasJobDetailOnload, setHasJobDetailOnLoad] = useState(false);
    const [countrySwitch, setCountrySwitch] = useState(false);
    const [firstStart, setFirstStart] = useState(true);

    // eslint-disable-next-line no-unused-vars
    const [crosshairVisible, setCrosshairVisible] = useState([]);

    const mapRef = useRef(null);
    const jobFeatureGroupRef = useRef(null);

    const { features } = data;

    const onMarkerClick = e => {
        const { slug } = e.target.options;
        fetchDetail(slug);
    };

    const updatedMapQueries = () => {
        if (mapRef.current && mapRef.current.leafletElement) {
            const bounds = mapRef.current.leafletElement.getBounds();
            const boundsString = bounds.toBBoxString();
            const urlBoxParam = shortenBoxUrlParam(boundsString);
            const { query } = router;
            const newQueries = {
                ...validateSearches(query),
                ...{ box: urlBoxParam }
            };
            const search = stringifyQueryParams(newQueries);
            router.push({
                pathname: "/",
                search
            });

            return newQueries;
        }
        return null;
    };

    const onMoveEnd = () => {
        // const map = e.target;
        // const map =  mapRef.current.leafletElement
        if (!countrySwitch && !firstStart && !hasJobDetailOnload) {
            // const queries = updatedMapQueries();
            // console.log("\n", "movend", queries, "\n");
            // fetchData(queries);
        }
    };

    // const fitBoundsToCountry = country => {
    //     console.log("country", country);
    //     const coords = bbox(country);
    //     const corner1 = L.latLng(coords[1], coords[0]);
    //     const corner2 = L.latLng(coords[3], coords[2]);
    //     const bounds = L.latLngBounds(corner1, corner2);
    //     console.log("countryBounds", bounds);
    //     if (bounds.isValid()) {
    //         mapRef.current.leafletElement.fitBounds(bounds, {
    //             padding: [10, 10]
    //         });
    //     }
    // };

    useEffect(() => {
        if (!firstStart) {
            console.log("\nfirst start changed!!\n");
            // onMoveEnd();
        }
    }, [firstStart]);

    useEffect(() => {
        if (!countrySwitch) {
            console.log("\ncountry switch change!\n");
            // onMoveEnd();
        }
    }, [countrySwitch]);

    const fitMapBounds = b => {
        if (mapRef.current && b) {
            const bnds = L.latLngBounds(b);
            if (bnds.isValid()) {
                console.log("\nfitMapBounds", bnds);

                mapRef.current.leafletElement.fitBounds(bnds, {
                    animate: false,
                    noMoveStart: true
                });
                if (firstStart) {
                    setFirstStart(false);
                    console.log("\nset first start false!!\n");
                }
            }
        }
    };

    const setFullExtent = () => {
        if (mapRef.current && features.length) {
            const bounds = L.latLngBounds(
                features.map(c => {
                    return [
                        c.geometry && c.geometry.coordinates[1],
                        c.geometry && c.geometry.coordinates[0]
                    ];
                })
            );

            const isBoundsValid = bounds.isValid();
            if (isBoundsValid) {
                mapRef.current.leafletElement.fitBounds(bounds, {
                    animate: false
                });
                console.log("\nsetFullExtent\n");

                if (firstStart) {
                    setFirstStart(false);
                    console.log("\nset first start false!!\n");
                }
                // onMoveEnd
                // setTimeout(() => {
                //     // firstStart = false;
                //     if (countrySwitch) {
                //         setCountrySwitch(false);
                //     }
                // }, 1000);
            }
        }
    };

    // toggle map window size with sidebar change
    useEffect(() => {
        if (mapRef && mapRef.current) {
            setTimeout(() => {
                mapRef.current.leafletElement.invalidateSize();
            }, 200);
        }
    }, [isSidebarOpen]);

    // highlight marker on sidebar hover
    useEffect(() => {
        if (mapRef.current) {
            if (highlightMarker.geometry.coordinates) {
                L.popup({
                    closeButton: false,
                    autoPan: false,
                    offset: [0, -15]
                })
                    .setLatLng([
                        highlightMarker.geometry.coordinates[1],
                        highlightMarker.geometry.coordinates[0]
                    ])
                    .setContent(highlightMarker.title)
                    .openOn(mapRef.current.leafletElement);
            } else {
                mapRef.current.leafletElement.closePopup();
            }
        }
    }, [highlightMarker]);

    // useEffect(() => {
    //     if (
    //         data.features.length &&
    //         !data.isFetching &&
    //         firstStart &&
    //         !query.box
    //     ) {
    //         setFullExtent();
    //     }
    // }, [data, firstStart, query]);

    useEffect(() => {
        fitMapBounds(mapBounds);
        // if (match.params.layer === "job" && match.params.slug) {
        //     setHasJobDetailOnLoad(true);
        // } else {
        //     const countryPath = hasCountryPath(router.match);
        //     if (countryPath) {
        //         fetchData(validateSearches({ country: countryPath }));
        //     } else {
        //         const searches = validateSearches({ box, ...router.query });
        //         if (box) {
        //             console.log("fitbounds", box);
        //             fitMapBounds(mapBounds);
        //         }
        //         fetchData(searches);
        //     }
        // }
        // console.log("\nloaded\n");
    }, []);

    // useEffect(() => {
    //     if (hasJobDetailOnload && !detail.isFetching) {
    //         setHasJobDetailOnLoad(false);
    //         const { properties, geometry } = detail.data;
    //         if (geometry && properties && !properties.invalidGeom) {
    //             const { coordinates } = geometry;
    //             console.log("set view");
    //             mapRef.current.leafletElement.setView(
    //                 [coordinates[1], coordinates[0]],
    //                 10
    //             );
    //         } else if (properties.countryCode) {
    //             console.log("detail has country code!");
    //             fetchData(
    //                 validateSearches({ country: properties.countryCode })
    //             );
    //         }
    //     }
    // }, [hasJobDetailOnload, detail]);

    // memoized to prevent unecessary rerendering
    const jobClustersMemo = useMemo(() => {
        return (
            <JobClusters markerClick={onMarkerClick} mapFeatures={features} />
        );
    }, [features]);

    const mapStyle = {
        position: isMobile ? "fixed" : "relative",
        width: isMobile ? "calc(100% - 80px)" : "100%",
        left: isMobile ? "80px" : "0",
        height: "calc(100% - 50px)",
        marginTop: "50px",
        zIndex: "1"
    };

    return (
        <div style={mapStyle}>
            <Map
                className="leaflet-map"
                zoomControl={false}
                onMoveEnd={onMoveEnd}
                maxZoom={12}
                //zoom={1}
                // center={{ lat: 51, lng: 0 }}
                attributionControl={false}
                bounds={mapBounds}
                // boundsOptions={{ padding: [50, 50] }}
                ref={mapRef}
                worldCopyJump
            >
                <AttributionControl
                    position="bottomright"
                    prefix="Built by <a href='http://ian.shi.land' target='_blank'>ian.shi.land</a>"
                />

                <TileLayer
                    attribution='<a href="https://leafletjs.com/">Leaflet</a> | &amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a>'
                    url={basemapProvider}
                />

                <ZoomControl position="bottomright" />

                <FeatureGroup ref={jobFeatureGroupRef}>
                    {jobClustersMemo}
                </FeatureGroup>

                {data.country &&
                data.country.geom.coordinates &&
                data.country.geom.coordinates.length ? (
                    <GeoJSON
                        data={{
                            type: "Feature",
                            properties: {},
                            geometry: data.country.geom
                        }}
                        className="country-layer"
                        style={() => ({
                            stroke: false,
                            weight: 1,
                            fillOpacity: 0.1
                        })}
                    />
                ) : null}

                {highlightMarker.geometry.coordinates ? (
                    <CircleMarker
                        key={`highlight-layer-${highlightMarker.title}`}
                        center={[
                            highlightMarker.geometry.coordinates[1],
                            highlightMarker.geometry.coordinates[0]
                        ]}
                        stroke
                        strokeColor="#00FFFF"
                        strokeOpacity={0.7}
                        radius={20}
                    />
                ) : null}
            </Map>
        </div>
    );
};

const mapStateToProps = ({ data, highlightMarker, detail }) => ({
    data,
    highlightMarker,
    detail
});

const mapDispatchToProps = dispatch =>
    bindActionCreators(
        {
            fetchData,
            fetchDetail,
            toggleHighlightMarker
        },
        dispatch
    );

export default connect(mapStateToProps, mapDispatchToProps)(LeafletMap);
