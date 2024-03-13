import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { Button, Form, Container, Row, Col, Alert } from "react-bootstrap";
import Select from 'react-select';

const ScrapeRecipe = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [selectedRestaurants, setSelectedRestaurants] = useState([]);
  const [url, setUrl] = useState("");
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRestaurants = async () => {
      try {
        const response = await axios.get("/api/restaurants/");
        setRestaurants(
          response.data.map((restaurant) => ({
            value: restaurant.id,
            label: restaurant.name,
          })),
        );
      } catch (error) {
        console.error("Error fetching restaurants:", error);
      }
    };
    fetchRestaurants();
  }, []);

  const handleRestaurantChange = useCallback((selectedOptions) => {
    setSelectedRestaurants(selectedOptions.map(option => option.value));
  }, []);

  const handleUrlChange = useCallback((event) => {
    setUrl(event.target.value);
  }, []);

  const validateRecipeSchema = useCallback(async () => {
    try {
      const response = await axios.get("/api/scrape-recipe/", {
        params: {
          url: url,
        },
      });
      setRecipe(response.data.recipe);
      setError(null);
    } catch (error) {
      setError("Invalid recipe schema or URL.");
      setRecipe(null);
      console.error("Error validating recipe schema:", error);
    }
  }, [url]);

  const addRecipe = useCallback(async () => {
    try {
      const postData = {
        title: recipe.title,
        description: recipe.description,
        instructions: recipe.instructions,
        url: url,
        ingredients: recipe.ingredients,
        restaurants: selectedRestaurants,
      };
  
      await axios.post("/api/recipes/", postData);
      setUrl("");
      setRecipe(null);
      setSelectedRestaurants([]);
      setError(null);
      alert("Recipe added successfully!");
    } catch (error) {
      if (error.response && error.response.status === 409) {
        setError("A recipe with this URL already exists.");
      } else {
        setError("Error adding recipe.");
      }
      console.error("Error adding recipe:", error);
    }
  }, [recipe, url, selectedRestaurants]);

  // Disable the Add Recipe button if no valid recipe was scraped or no restaurants are selected
  const isAddRecipeDisabled = !recipe || selectedRestaurants.length === 0;

  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col md={8}>
          <h1 className="text-center mb-4">Scrape Recipe</h1>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Select Restaurants</Form.Label>
              <Select
                isMulti
                name="restaurants"
                options={restaurants}
                className="basic-multi-select"
                classNamePrefix="select"
                onChange={handleRestaurantChange}
                value={restaurants.filter(restaurant => selectedRestaurants.includes(restaurant.value))}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Recipe URL</Form.Label>
              <Form.Control
                type="url"
                placeholder="Enter recipe URL"
                value={url}
                onChange={handleUrlChange}
              />
            </Form.Group>
            <Button variant="primary" onClick={validateRecipeSchema}>
              Validate Recipe Schema
            </Button>
            {recipe && (
              <div className="mt-3">
                <h3>Recipe Details</h3>
                <p><strong>Title:</strong> {recipe.title}</p>
                <p><strong>Description:</strong> {recipe.description}</p>
                <p><strong>Ingredients:</strong> {recipe.ingredients.join(", ")}</p>
                <p><strong>Instructions:</strong> {recipe.instructions}</p>
                <Button variant="success" onClick={addRecipe} disabled={isAddRecipeDisabled}>
                  Add Recipe
                </Button>
              </div>
            )}
            {error && (
              <Alert variant="danger" className="mt-3">{error}</Alert>
            )}
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default ScrapeRecipe;
