import React, { Component } from 'react';
import { Box, Flex, Text, Avatar, Button } from '@chakra-ui/react';
import { Link } from 'react-router-dom';
import './Sidebar.css';
import AppContext from '../context';

class Sidebar extends Component {
  constructor(props) {
    super(props);
    const pathParts = window.location.pathname.split('/');
    this.state = {
      activeButton: pathParts[1],
    };
  }

  handleButtonClick = buttonName => {
    this.setState({ activeButton: buttonName });
  };

  render() {
    const { activeButton } = this.state;

    return (
      <AppContext.Consumer>
        {({ sidebarOpened, toggleSidebar }) => (
          <Flex className={`sidebar_wrapper${sidebarOpened ? ' open' : ''}`}>
            <Box className="sidebar">
              <Box display="flex" alignItems="center">
                <Avatar size="md" src={'https://i.redd.it/nhre2ney3z211.jpg'} />
                <Box ml="3">
                  <Text fontWeight="bold" fontSize="md">
                    Yo
                  </Text>
                  <Text fontSize="sm" color="yellow.500">
                    Online
                  </Text>
                </Box>
              </Box>

              <Box display="flex" alignItems="center">
                <Avatar size="md" src={'https://i.redd.it/nhre2ney3z211.jpg'} />
                <Box ml="3" position="relative">
                  <Text fontWeight="bold" fontSize="md" zIndex="1">
                    {'yo'}
                  </Text>
                  <Box
                    position="absolute"
                    top="50%"
                    left="50%"
                    transform="translate(-50%, -50%)"
                    bg="white"
                    borderRadius="sm"
                    padding="1"
                    zIndex="0"
                  />
                </Box>
              </Box>

              <Box display="flex" flexDirection="column">
                <Link to="/home">
                  <Button
                    variant="ghost"
                    isActive={activeButton === 'home'}
                    onClick={() => this.handleButtonClick('home')}
                  >
                    Home
                  </Button>
                </Link>
                <Link to="/scan">
                  <Button
                    variant="ghost"
                    isActive={activeButton === 'scan'}
                    onClick={() => this.handleButtonClick('scan')}
                  >
                    Scan
                  </Button>
                </Link>
                <Link to="/discovery">
                  <Button
                    variant="ghost"
                    isActive={activeButton === 'discovery'}
                    onClick={() => this.handleButtonClick('discovery')}
                  >
                    Discovery
                  </Button>
                </Link>
              </Box>
            </Box>
          </Flex>
        )}
      </AppContext.Consumer>
    );
  }
}

export default Sidebar;
