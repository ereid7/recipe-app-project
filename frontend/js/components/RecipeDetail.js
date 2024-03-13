import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Container, Row, Col, Button, Spinner, ListGroup } from 'react-bootstrap';

const RecipeDetail = () => {
  const [recipe, setRecipe] = useState(null);
  const { recipeId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRecipeDetails = async () => {
      try {
        const response = await axios.get(`/api/recipes/${recipeId}/`);
        setRecipe(response.data);
      } catch (error) {
        console.error('Error fetching recipe details:', error);
      }
    };
    fetchRecipeDetails();
  }, [recipeId]);

  return (
    <Container style={{ paddingTop: "20px" }}>
      <Row className="justify-content-md-center" style={{ marginBottom: "20px" }}>
        <Col md={8}>
          <Button onClick={() => navigate(-1)} style={{ marginBottom: "20px" }}>Back to Recipes</Button>
          {recipe ? (
            <Card style={{ padding: "20px" }}>
              <Card.Body>
                <Card.Title>{recipe.title}</Card.Title>
                <Card.Text>{recipe.description}</Card.Text>
                <Card.Text><strong>URL:</strong> <a href={recipe.url} target="_blank" rel="noopener noreferrer">{recipe.url}</a></Card.Text>
                <Card.Text><strong>Ingredients:</strong> {recipe.ingredient_list.join(", ")}</Card.Text>
                <Card.Text><strong>Instructions:</strong> {recipe.instructions}</Card.Text>
                <ListGroup variant="flush">
                  <strong>Restaurants:</strong>
                  {recipe.restaurant_names.map((name, index) => (
                    <ListGroup.Item key={index}>{name}</ListGroup.Item>
                  ))}
                </ListGroup>
              </Card.Body>
            </Card>
          ) : (
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default RecipeDetail;
