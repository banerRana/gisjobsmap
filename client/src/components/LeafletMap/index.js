import React, { useEffect, useState, useRef, useMemo, useContext } from "react";
import { Icon } from "antd"
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
let setBoundsFired = false;
let firstStart = true;
let countrySwitch = false;
let hasJobDetailOnload = false;

const LeafletMap = ({
    detail,
    data,
    fetchData,
    fetchDetail,
    highlightMarker
}) => {
    const router = useRouter();
    const { match } = router;

    const box = router.query.box ? router.query.box : initialBounds;

    const { isSidebarOpen, isMobile } = useContext(SideBarContext);
    // eslint-disable-next-line no-unused-vars
    const [mapBounds, setMapBounds] = useState(boxQueryToArray(box));

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

    const onMoveEnd = e => {
        const map = e.target;
        if (map && !setBoundsFired) {
            if (!firstStart && !hasJobDetailOnload) {
                const queries = updatedMapQueries();
                fetchData(queries);
            }
        } else if (setBoundsFired) {
            setBoundsFired = false;
        }
    };


    const setFullExtent = () => {
        if (mapRef.current && features.length) {
            const bounds = L.latLngBounds(
                features
                    .filter(f => !f.properties.invalidGeom && f.geometry)
                    .map(c => {
                        return [
                            c.geometry.coordinates[1],
                            c.geometry.coordinates[0]
                        ];
                    })
            );

            const isBoundsValid = bounds.isValid();
            if (isBoundsValid) {
                setBoundsFired = true;
                mapRef.current.leafletElement.fitBounds(bounds);
                setTimeout(() => {
                    setBoundsFired = false;
                }, 1000);
            }
        }
        firstStart = false;
        countrySwitch = false;
    };

    useEffect(() => {
        if (mapRef.current && data.features.length && firstStart) {
            setFullExtent();
        }
    }, [data, mapRef]);

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

    useEffect(() => {
        if (
            data.features.length &&
            !data.isFetching &&
            (firstStart || countrySwitch)
        ) {
            setFullExtent();
        }
    }, [data]);

    useEffect(() => {
        if (router.query.country && !firstStart) {
            countrySwitch = true;
        }
    }, [router.query.country]);

    // memoized to prevent unecessary rerendering
    const jobClustersMemo = useMemo(() => {
        return (
            <JobClusters markerClick={onMarkerClick} mapFeatures={features} />
        );
    }, [features]);

    useEffect(() => {
        if (match.params.layer === "job" && match.params.slug) {
            hasJobDetailOnload = true;
        } else if (mapRef && mapRef.current) {
            const countryPath = hasCountryPath(router.match);
            if (countryPath) {
                router.push({
                    pathname: "/",
                    search: `?country=${countryPath}`
                });
                countrySwitch = true;
                fetchData(validateSearches({ country: countryPath }));
            } else {
                fetchData(validateSearches({ box, ...router.query }));
            }
        }
        // firstStart = false;
    }, []);

    useEffect(() => {
        if (!detail.isFetching && detail.dataId && hasJobDetailOnload) {
            hasJobDetailOnload = false;
            const { geometry, properties } = detail.data;
            if (geometry && geometry.coordinates && !properties.invalidGeom) {
                firstStart = false;
                const { coordinates } = geometry;
                mapRef.current.leafletElement.setView(
                    [coordinates[1], coordinates[0]],
                    10
                );
            } else if (properties) {
                // for remote jobs w/ no geometry
                const { countryCode } = properties;
                fetchData(
                    validateSearches({
                        country: countryCode
                    })
                );
            }
        }
    }, [detail.isFetching]);

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
                attributionControl={false}
                bounds={mapBounds}
                ref={mapRef}
                worldCopyJump
            >
                <AttributionControl
                    position="bottomright"
                    prefix="<a href='https://github.com/ishiland/gisjobsmap' target='_blank'>Contribute on Github</a>"
                />

                <TileLayer
                    attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a>'
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
