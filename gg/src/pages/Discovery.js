import React, { Component } from 'react';
import RecipeCard from './RecipeCard';

class Discovery extends Component {
  state = {
    recipes: [],
    currentRecipeIndex: 0,
  };

  handleDragEnd = direction => {
    const { recipes, currentRecipeIndex } = this.state;
    const currentRecipe = recipes[currentRecipeIndex];

    fetch('http://localhost:4000/add-recipe', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        is_chosen: direction === 'right',
        recipe_id: currentRecipe.id,
      }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('HTTP error, status = ' + response.status);
        }
        return response.json();
      })
      .then(() => {
        // Remove the recipe from the list
        this.setState(() => ({
          recipes: recipes.filter(recipe => recipe !== currentRecipe),
        }));

        // If recipe list is empty -> request some more
        if (!recipes || recipes.length === []) this.fetchRecipes();
      })
      .catch(error => {
        if (error.message === 'HTTP error, status = 404') {
          console.error('Recipe not found:', currentRecipe.id);
        } else {
          console.error(
            'Error making http://localhost:4000/add-recipe POST request:',
            error
          );
        }
      });
  };

  componentDidMount() {
    const storedRecipes = localStorage.getItem('recipes');
    if (storedRecipes && storedRecipes.length !== 0) {
      this.setState({
        recipes: JSON.parse(storedRecipes),
      });
    } else {
      this.fetchRecipes();
    }
  }

  render() {
    const { recipes, currentRecipeIndex } = this.state;
    return (
      <div>
        {recipes.length === 0 ? (
          <div>Loading...</div>
        ) : (
          <RecipeCard
            recipe={recipes[currentRecipeIndex]}
            onDragEnd={this.handleDragEnd}
          />
        )}
      </div>
    );
  }

  //AUXILIARY FUNCTIONS

  fetchRecipes() {
    fetch('http://localhost:4000/recipes', { method: 'GET' })
      .then(response => response.json())
      .then(data => {
        this.setState({ recipes: data }, () => {
          localStorage.setItem('recipes', JSON.stringify(this.state.recipes));
        });
      })
      .catch(error => {
        console.error('Error in recipes retrieving', error);
      });
  }
}

export default Discovery;
