import L from "leaflet";
import { withLeaflet, MapLayer } from "react-leaflet";

require("leaflet.markercluster");

require("leaflet.markercluster/dist/MarkerCluster.Default.css");

class MarkerClusterGroup extends MapLayer {
    createLeafletElement(props) {
        const el = new L.markerClusterGroup(props); // eslint-disable-line
        this.contextValue = {
            ...props.leaflet,
            layerContainer: el
        };
        return el;
    }
}

export default withLeaflet(MarkerClusterGroup);
