import React, { Component } from 'react';
import { ChakraProvider, theme } from '@chakra-ui/react';
import Controlbar from './components/controlbar/Controlbar';
import AppContext from './components/context';
import Sidebar from './components/sidebar/Sidebar';
import { BrowserRouter } from 'react-router-dom';
import BarcodeScanner from './pages/BarcodeScanner';
import Discovery from './pages/Discovery';
import FridgePage from './pages/FridgePage';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sidebarOpened: false,
    };
    this.toggleSidebar = this.toggleSidebar.bind(this);
  }

  toggleSidebar() {
    this.setState(prevState => ({ sidebarOpened: !prevState.sidebarOpened }));
  }

  render() {
    const { sidebarOpened } = this.state;
    const path = window.location.pathname;

    var content;
    switch (path) {
      case '/discovery':
        content = <Discovery />;
        break;
      case '/scan':
        content = <BarcodeScanner />;
        break;
      case '/fridge':
        content = <FridgePage />;
        break;
      default:
        content = null;
        break;
    }

    // Here content is injected -> {content}
    return (
      <ChakraProvider theme={theme}>
        {/* Basically this part manages the scrollbar and sidabar */}
        <AppContext.Provider
          value={{
            sidebarOpened: sidebarOpened,
            toggleSidebar: this.toggleSidebar,
          }}
        >
          <BrowserRouter>
            <Controlbar value={sidebarOpened} />
            <div
              style={{ display: 'flex', flexDirection: 'row', height: '100%' }}
            >
              <Sidebar value={sidebarOpened} />
              <div style={{ flexGrow: 1, padding: '20px' }}>{content}</div> 
            </div>
          </BrowserRouter>
        </AppContext.Provider>
      </ChakraProvider>
    );
  }
}

export default App;
