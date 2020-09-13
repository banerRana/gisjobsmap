import React, { createContext, useState } from "react";

export const SideBarContext = createContext();

function SidebarContextProvider({ children }) {
    const getSize = () => {
        return window.innerWidth > 700;
    };

    const checkDevice = () => {
        const windowWidth =
            window.screen.width < window.outerWidth
                ? window.screen.width
                : window.outerWidth;
        const mobile = windowWidth < 500;
        return mobile;
    };

    const [isSidebarOpen, setSidebarOpen] = useState(getSize());

    const isMobile = checkDevice();

    return (
        <SideBarContext.Provider
            value={{
                isSidebarOpen,
                setSidebarOpen,
                isMobile
            }}
        >
            {children}
        </SideBarContext.Provider>
    );
}
export default SidebarContextProvider;
