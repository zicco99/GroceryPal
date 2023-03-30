import {
  Box,
  Flex,
  Text,
  Button,
  Stack,
  Input,
  HStack,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
} from '@chakra-ui/react';
import './Controlbar.css';
import { addFridge, fetchFridges } from './fridgeControls';
import AppContext from '../context';
import React from 'react';

class Controlbar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      curr_fridge: '',
      isSelecting: true,
      initFridgeList: ['Aggiungi un frigo'],
      deltaFridgeList: [],
    };
  }
  handleToggle = () => {
    const { toggleSidebar } = this.context;
    toggleSidebar();
  };

  handleAddFridge = () => {
    addFridge(this.state.curr_fridge);
    this.setState({ isSelecting: !this.state.isSelecting });
  };

  handleInputChange = e => {
    this.setState({ curr_fridge: e.target.value });
  };

  handleOptionSelect = option => {
    console.log(option);

    if (option === undefined) {
      this.setState({ isSelecting: !this.state.isSelecting });
    } else {
      console.log(option)
      this.setState({ curr_fridge: option });
    }
  };

  async componentDidMount() {
    console.log(this.state.deltaFridgeList);
    const fridges = await fetchFridges();
    if (fridges) {
      this.setState({ deltaFridgeList: fridges });
    }
  }

  render() {
    var content;
    const path = window.location.pathname;
    switch (path) {
      case '/fridge': {
        content = (
          <div>
            {this.state.isSelecting === false ? (
              <Box>
                <Menu>
                  <MenuButton as={Button}>{this.state.curr_fridge}</MenuButton>
                  <MenuList>
                    {console.log(this.state.deltaFridgeList)}
                    {[
                      ...this.state.initFridgeList,
                      ...this.state.deltaFridgeList,
                    ].map((item, index) => (
                      <MenuItem
                        bg="blue.500"
                        item={item}
                        key={index}
                        onClick={this.handleOptionSelect}
                      >
                        {item}
                      </MenuItem>
                    ))}
                  </MenuList>
                </Menu>
              </Box>
            ) : (
              <HStack spacing={4}>
                <Box
                  bg="blue.500"
                  borderRadius="lg"
                  px={2}
                  py={1}
                  width="300px"
                >
                  <Input
                    variant="unstyled"
                    value={this.state.curr_fridge}
                    onChange={this.handleInputChange}
                    placeholder="Enter some text"
                    color="white"
                  />
                </Box>
                <Button
                  colorScheme="teal"
                  variant="solid"
                  onClick={this.handleAddFridge}
                >
                  Add Fridge
                </Button>
              </HStack>
            )}
          </div>
        );
      }
      case '/scan':
        break;
      default:
        content = null;
        break;
    }

    return (
      <AppContext.Consumer>
        {({ sidebarOpened }) => (
          <Flex
            className={`controlbar ${sidebarOpened ? ' open' : ''}`}
            as="header"
            align="center"
            justify="space-between"
            wrap="wrap"
            padding="1.5rem"
            bg="gray.500"
            color="white"
          >
            <Stack direction="row" spacing={4} align="center">
              <div>{content}</div>
            </Stack>
            <Box>
              {/* Add your controls here */}
              <Button colorScheme="blue" mr="4" onClick={this.handleToggle}>
                {sidebarOpened ? 'Close Sidebar' : 'Open Sidebar'}
              </Button>
            </Box>
          </Flex>
        )}
      </AppContext.Consumer>
    );
  }
}

Controlbar.contextType = AppContext;
export default Controlbar;
