import axios from "axios";
import queryString from "query-string";

// get user location and initialize map. Pass in argument to get user Location or not.
export function getJobs(params) {
    return axios.get("/api/jobs/all", {
        params,
        paramsSerializer: function(params) {
            return queryString.stringify(params, { arrayFormat: "comma" });
        }
    });
}

export function getJobCounts() {
    return axios.get("/api/jobs/counts");
}

export function postJob(params) {
    return axios.post("/api/jobs/add-no-auth", params);
}

export function getOrganizations(params) {
    return axios.get("/api/organizations/all", { params });
}

export function getSchools(params) {
    return axios.get("/api/schools/all", { params });
}

export function getRFPs(params) {
    return axios.get("/api/rfps/all", { params });
}

export function getResumes(params) {
    return axios.get("/api/resumes/all", { params });
}

// get user location and initialize map
export function getJobDetail(params) {
    return axios.get("/api/jobs/detail", { params });
}

export function getOrganizationDetail(params) {
    return axios.get("/api/organizations/detail", { params });
}

// geocoder - also pass in current country.
export function doGeocode(params) {
    return axios.get("/api/geonames/geocode", { params });
}

export function getTitles() {
    return axios.get("/api/titles/all");
}

export function getTags(params) {
    return axios.get("/api/tags/all", { params });
}

export function getCategories(params) {
    return axios.get("/api/categories/all", { params });
}

export function getOrganizationSuggestions(params) {
    return axios.get("/api/organizations/all", { params });
}

export function getReverseGeocode(params) {
    return axios.get("/api/geonames/reverse-geocode", { params });
}

export function getGeocode(params) {
    return axios.get("/api/geonames/geocode", { params });
}

// get user location
// export function getLocation(params){
//     return axios.get('/api/getLocation');
// }
