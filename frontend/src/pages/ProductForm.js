import { useState } from "react";
import {
  FormControl,
  FormLabel,
  Input,
  Button,
  Checkbox,
  CheckboxGroup,
  NumberInput,
  NumberInputField,
  Select
} from "@chakra-ui/react";
import ProductPhotoBox from "./ProductPhotoBox";

function ProductForm({ product, onFormButtonClick }) {
  //it is a React built-in hook that allows you to add state
  //to functional components. The hook returns an array with two
  //values: the current state value, and a function to update that value.
  console.log(product)

  const [barcode, setBarcode] = useState(product.barcode || '');
  const [name, setName] = useState(product.name || '');
  const [brand, setBrand] = useState(product.brand || '');
  const [labels, setLabels] = useState(product.labels || []);
  const [ecoScore, setEcoScore] = useState(product.eco_score || '');
  const [novaScore, setNovaScore] = useState(product.nova_score || '');
  const [bigImageUrl, setBigImageUrl] = useState(product.big_image_url || '');
  const [miniImageUrl, setMiniImageUrl] = useState(product.mini_image_url || '');
  const [meal, setMeal] = useState(product.meal || []);
  const [allergens, setAllergens] = useState(product.allergens || []);
  const [quantity, setQuantity] = useState(product.quantity || '');

  const handleSubmit = event => {
    event.preventDefault();
    const product = {
      name,
      brand,
      labels,
      eco_score: ecoScore,
      nova_score: novaScore,
      big_image_url: bigImageUrl,
      mini_image_url: miniImageUrl,
      meal,
      allergens,
      quantity,
    };
    sendData(product);
  };

  const sendData = async product => {
    try {
      const response = await fetch(`http://localhost:4000/product/${product.barcode}`);
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }
      this.setState({ mode: 'video' });
    } catch (error) {
      console.error(error);
      this.setState({ error: 'Failed to retrieve product information.' });
    }
  };



  return (
    <div>
      <ProductPhotoBox />
      <form onSubmit={handleSubmit}>
        <FormControl>
          <FormLabel>Barcode</FormLabel>
          <Input
            type="text"
            value={barcode}
            onChange={e => setBarcode(e.target.value)}
          />
        </FormControl>

        <FormControl mt={4}>
          <FormLabel>Name</FormLabel>
          <Input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
          />
        </FormControl>

        <FormControl mt={4}>
          <FormLabel>Brand</FormLabel>
          <Input
            type="text"
            value={brand}
            onChange={e => setBrand(e.target.value)}
          />
        </FormControl>

        <FormControl mt={4}>
          <FormLabel>Labels</FormLabel>
          <CheckboxGroup value={labels} onChange={setLabels}>
            <Checkbox value="gluten-free">Gluten Free</Checkbox>
            <Checkbox value="vegan">Vegan</Checkbox>
            {/* add more labels here */}
          </CheckboxGroup>
        </FormControl>

        <FormControl mt={4}>
          <FormLabel>Eco Score</FormLabel>
          <Select value={ecoScore} onChange={e => setEcoScore(e.target.value)}>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
          </Select>
        </FormControl>

        <FormControl mt={4}>
          <FormLabel>Nova Score</FormLabel>
          <Select
            value={novaScore}
            onChange={e => setNovaScore(e.target.value)}
          >
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
          </Select>
        </FormControl>
        <FormControl mt={4}>
          <FormLabel>Big Image URL</FormLabel>
          <Input
            type="text"
            value={bigImageUrl}
            onChange={e => setBigImageUrl(e.target.value)}
          />
        </FormControl>

        <FormControl mt={4}>
          <FormLabel>Mini Image URL</FormLabel>
          <Input
            type="text"
            value={miniImageUrl}
            onChange={e => setMiniImageUrl(e.target.value)}
          />
        </FormControl>

        <FormControl mt={4}>
          <FormLabel>Meal</FormLabel>
          <CheckboxGroup value={meal} onChange={setMeal}>
            <Checkbox value="breakfast">Breakfast</Checkbox>
            <Checkbox value="lunch">Lunch</Checkbox>
            <Checkbox value="snack">Snack</Checkbox>
            <Checkbox value="dinner">Dinner</Checkbox>
          </CheckboxGroup>
        </FormControl>

        <FormControl mt={4}>
          <FormLabel>Allergens</FormLabel>
          <CheckboxGroup value={allergens} onChange={setAllergens}>
            <Checkbox value="peanuts">Peanuts</Checkbox>
            <Checkbox value="tree-nuts">Tree Nuts</Checkbox>
            <Checkbox value="wheat">Wheat</Checkbox>
            {/* add more allergens here */}
          </CheckboxGroup>
        </FormControl>

        <FormControl mt={4}>
          <FormLabel>Quantity</FormLabel>
          <NumberInput value={quantity} onChange={value => setQuantity(value)}>
            <NumberInputField />
          </NumberInput>
        </FormControl>

        <Button type="submit" mt={4}>
          Submit
        </Button>
      </form>
    </div>
  );
}

export default ProductForm;
      