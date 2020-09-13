import { format } from "timeago.js";

import { countries } from "../config";

export function parseJSON(response) {
    return response.data;
}

export const getRelativeTime = timestamp => {
    const t = format(`${timestamp[0]} ${timestamp[1]}`);
    if (t.includes("hour") || t.includes("minute") || t.includes("second")) {
        return "Today";
    }
    return t;
};

export const strShort = (str, length) => {
    // let length = large ?  42 : 25;
    if (str === str.toUpperCase()) {
        return length - 3;
    }
    if (str.length > length) {
        return str.substr(0, length).trim() + "...";
    }
    return str;
};

export function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

export const removeEmpty = obj => {
    const o = JSON.parse(JSON.stringify(obj)); // Clone source oect.

    Object.keys(o).forEach(key => {
        if (o[key] && typeof o[key] === "object") o[key] = removeEmpty(o[key]);
        // Recurse.
        else if (typeof o[key] === "boolean") o[key] === false && delete o[key];
        else if (o[key] === undefined || o[key] === null || !o[key].length)
            delete o[key];
        // Delete undefined and null.

        // else o[key] = o[key]; // Copy value.
    });

    return o; // Return new object.
};


// detemrines if there are any searches aside from iso2
export const checkIfSearchEmpty = inSearches => {
    const searchObj = { ...inSearches };
    delete searchObj.iso2;
    if (
        searchObj === null ||
        searchObj === undefined ||
        Array.isArray(searchObj) ||
        typeof searchObj !== "object"
    ) {
        return true;
    }
    return Object.getOwnPropertyNames(searchObj).length === 0;
};

export const countryNameFromIso2 = iso2 => {
    if (iso2) {
        Object.entries(countries).forEach(([key, value]) => {
            if (key.toLowerCase() === iso2.toLowerCase()) {
                return value;
            }
            return null;
        });
    }
    return null;
};

// used to retrieve title case and validate layer name
export const layerNameTitleCase = layer => {
    const layers = {
        jobs: "Jobs",
        organizations: "Organizations",
        schools: "Schools",
        rfps: "RFPs",
        resumes: "Resumes"
    };

    return layers[layer];
};
