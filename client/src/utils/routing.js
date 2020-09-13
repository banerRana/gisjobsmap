import queryString from "query-string";

import { countries } from "../config";

const validSearches = [
    //must be alllowercase

    "box",
    "q",
    // "name",
    "tags",
    // "layer",
    // "slug",
    "date",
    "categories",
    "type",
    "date",
    // "distributed",
    "maponly",
    "country"
    // "source"
];

export const hasCountryPath = location => {
    const { layer } = location.params;
    if (layer) {
        const isCountryParam = countries[layer.toLowerCase()];
        if (isCountryParam) {
            return layer.toLowerCase();
        }
    }
    return undefined;
};

export const boxQueryToArray = box => {
    if (box) {
        const s = box.split(",");
        if (s.length === 4) {
            return [
                [parseFloat(s[1]), parseFloat(s[0])],
                [parseFloat(s[3]), parseFloat(s[2])]
            ];
        }
    }
    return undefined;
};

export const shortenBoxUrlParam = boxArray => {
    if (boxArray) {
        const s = boxArray.split(",");
        return [
            parseFloat(s[0]).toFixed(2),
            parseFloat(s[1]).toFixed(2),
            parseFloat(s[2]).toFixed(2),
            parseFloat(s[3]).toFixed(2)
        ].join(",");
    }
    return "";
};

export const shortenBBoxStringToArray = box => {
    if (box) {
        const spl = box.split(",");
        if (spl.length === 4) {
            return spl.map(item => Math.round(Number(item) * 1e4) / 1e4);
        }
    }
    return [];
};

export const areBoundsEqual = (mapBounds, queryBounds) => {
    if (mapBounds.length && queryBounds.length) {
        return JSON.stringify(mapBounds) === JSON.stringify(queryBounds);
    }
    return false;
};

export const validateCountryIso2 = input => {
    return countries[input];
};

export const updateCountryParam = (iso2, layer) => {
    // returns updated pathname based on selected iso2 country code
    return `/${iso2}/${layer}`;
};

export const changeLayerRoute = (layer, queryObject) => {
    // returns updated pathname based on selected layer
    const result = { ...queryObject };
    delete result["layer"];
    delete result["slug"];
    const st = queryString.stringify(result);
    return `/${layer}?${st}`;
};

export const stringifyQueryParams = queries => {
    const result = { ...queries };
    delete result["layer"];
    delete result["slug"];
    return queryString.stringify(result, { arrayFormat: "none" });
};

export const getQueryCount = queryObject => {
    const result = { ...queryObject };
    delete result["layer"];
    delete result["slug"];
    delete result["box"];
    return Object.keys(result).length;
};

export const resetQueryParams = queryObject => {
    const { box } = queryObject;
    return queryString.stringify({ box });
};

export const validateSearches = queryObject => {
    const result = { ...queryObject };
    Object.keys(result).forEach(key => {
        if (!validSearches.includes(key.toLowerCase())) {
            delete result[key];
        }
    });
    return result;
};

export const parseQueryString = st => {
    return queryString.parse(st, {
        parseBooleans: true,
        parseNumbers: true
    });
};

export const removeEmptyProperties = obj => {
    Object.keys(obj).forEach(
        k => !obj[k] && obj[k] !== undefined && delete obj[k]
    );
    return obj;
};

export const removeEmptySearches = obj => {
    if (obj.categories && !obj.categories.length) {
        delete obj.categories;
    }
    if (obj.country && obj.country === "any") {
        delete obj.country;
    }
    if (obj.date && obj.date === "0") {
        delete obj.date;
    }
    if (obj.maponly === false) {
        delete obj.maponly;
    }
    if (obj.q === "") {
        delete obj.q;
    }
    if (obj.tags && !obj.tags.length) {
        delete obj.tags;
    }
    return obj;
};
