export const addFridge = name => {
    fetch('http://localhost:4000/new-fridge', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(name),
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.error('Fridge has not been created', error);
      });
}

export const fetchFridges = async () => {
  try {
    const response = await fetch('http://localhost:4000/list-fridges', {
      method: 'GET',
    });
    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error('Fridge has not been created', error);
  }
};