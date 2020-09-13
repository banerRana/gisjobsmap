import React, { createContext, useState } from "react";
import PropTypes from "prop-types";

export const JobDetailContext = createContext();

function JobDetailContextProvider({ children }) {
    const [isJobDetailOpen, setJobDetailOpen] = useState(false);

    return (
        <JobDetailContext.Provider
            value={{
                isJobDetailOpen,
                setJobDetailOpen
            }}
        >
            {children}
        </JobDetailContext.Provider>
    );
}

JobDetailContextProvider.propTypes = {
    children: PropTypes.any
};

export default JobDetailContextProvider;
