import React from 'react';

const AppContext = React.createContext({
  sidebarOpened: false,
  toggleSidebar: () => {},
});

export default AppContext;