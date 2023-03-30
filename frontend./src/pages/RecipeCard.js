import React, { Component } from 'react';
import {
  Box,
  Button,
  Card,
  CardBody,
  CardFooter,
  Flex,
  Text,
} from '@chakra-ui/react';

class RecipeCard extends Component {
  state = {
    xPosition: 0,
    yPosition: 0,
    rotation: 0,
    dragStartX: null,
    dragStartY: null,
  };

  handleDragStart = e => {
    this.setState({
      dragStartX: e.clientX || e.touches[0].clientX,
      dragStartY: e.clientY || e.touches[0].clientY,
    });
    e.preventDefault();
  };

  handleDragMove = e => {
    const { dragStartX, dragStartY } = this.state;
    if (dragStartX !== null && dragStartY !== null) {
      var xPosition = (e.clientX || e.touches[0].clientX) - dragStartX;
      var yPosition = (e.clientY || e.touches[0].clientY) - dragStartY;

      //TODO Limit the swipe (it should be adaptive)
      if (yPosition > 50) {
        yPosition = 50;
      } else if (yPosition < -50) {
        yPosition = -50;
      }

      if (xPosition > 400) {
        xPosition = 400;
      } else if (xPosition < -400) {
        xPosition = -400;
      }

      const rotation = xPosition * 0.05;
      this.setState({
        xPosition,
        yPosition,
        rotation,
      });
    }
    e.preventDefault();
  };

  handleDragEnd = () => {
    const { xPosition } = this.state;
    const { onDragEnd } = this.props;
    if (xPosition > 200) {
      onDragEnd('right');
    } else if (xPosition < -200) {
      onDragEnd('left');
    }
    this.setState(prevState => ({
      xPosition: 0,
      yPosition: 0,
      rotation: 0,
      dragStartX: null,
      dragStartY: null,
    }));
  };

  render() {
    const { xPosition, yPosition, rotation } = this.state;
    const { recipe } = this.props;

    return (
      <Flex
        justify="center"
        align="center"
        w="100vw"
        h="100vh"
        onMouseDown={this.handleDragStart}
        onTouchStart={this.handleDragStart}
        onMouseMove={this.handleDragMove}
        onTouchMove={this.handleDragMove}
        onMouseUp={() => this.handleDragEnd()}
        onTouchEnd={() => this.handleDragEnd()}
        onMouseLeave={() => this.handleDragEnd()}
        onTouchCancel={() => this.handleDragEnd()}
      >
        <Box
          transform={`translate(${xPosition}px, ${yPosition}px) rotate(${rotation}deg)`}
        >
          <Card w="400px" maxW="90vw">
            <CardBody>
              <Text fontSize="2xl">{recipe.title}</Text>
              <Text fontSize="md">{recipe.description}</Text>
            </CardBody>
            <CardFooter>
              <Button>Add to Favorites</Button>
            </CardFooter>
          </Card>
        </Box>
      </Flex>
    );
  }
}

export default RecipeCard;
