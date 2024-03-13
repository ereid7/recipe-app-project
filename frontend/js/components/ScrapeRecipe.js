import React, { useState, useEffect } from "react";
import axios from "axios";
import { Button, Form, Container, Row, Col, Alert } from "react-bootstrap";
import MultiSelect from "./MultiSelect";

const ScrapeRecipe = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [selectedRestaurants, setSelectedRestaurants] = useState([]);
  const [url, setUrl] = useState("");
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch restaurants
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

  const handleRestaurantChange = (event) => {
    setSelectedRestaurants(
      [...event.target.selectedOptions].map((option) => option.value),
    );
  };

  const handleUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const validateRecipeSchema = async () => {
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
  };

  const addRecipe = async () => {
    try {
      await axios.post("/api/recipes/", {
        ...recipe,
        restaurants: selectedRestaurants,
      });
      setUrl("");
      setRecipe(null);
      setSelectedRestaurants([]);
      setError(null);
      alert("Recipe added successfully!");
    } catch (error) {
      setError("Error adding recipe.");
      console.error("Error adding recipe:", error);
    }
  };

  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col md={8}>
          <h1 className="text-center mb-4">Scrape Recipe</h1>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Select Restaurants</Form.Label>
              <MultiSelect
                options={restaurants}
                selectedOptions={selectedRestaurants}
                onChange={handleRestaurantChange}
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
                <p>
                  <strong>Title:</strong> {recipe.title}
                </p>
                <p>
                  <strong>Description:</strong> {recipe.description}
                </p>
                <p>
                  <strong>Ingredients:</strong> {recipe.ingredients.join(", ")}
                </p>
                <Button variant="success" onClick={addRecipe}>
                  Add Recipe
                </Button>
              </div>
            )}
            {error && (
              <Alert variant="danger" className="mt-3">
                {error}
              </Alert>
            )}
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default ScrapeRecipe;
