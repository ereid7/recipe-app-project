import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Container, Table, Button, Row, Col } from 'react-bootstrap';

const RecipeList = () => {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const response = await axios.get('/api/recipes/');
        setRecipes(response.data);
      } catch (error) {
        console.error('Error fetching recipes:', error);
      }
    };
    fetchRecipes();
  }, []);

  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col md={8}>
          <h1 className="text-center mb-4">Recipes</h1>
          {recipes.length > 0 ? (
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Description</th>
                  <th>Ingredients Count</th>
                  {/* <th>Restaurant Count</th> */}
                </tr>
              </thead>
              <tbody>
                {recipes.map((recipe) => (
                  <tr key={recipe.id}>
                    <td><Link to={`/recipe/${recipe.id}`}>{recipe?.title}</Link></td>
                    <td>{recipe?.description}</td>
                    <td>{recipe.ingredients_count}</td>
                    {/* <td>{recipe.restaurants.length}</td> */}
                  </tr>
                ))}
              </tbody>
            </Table>
          ) : (
            <p>No recipes found.</p>
          )}
          <div className="mt-4 d-flex justify-content-between">
            <Link to="/scrape-recipe">
              <Button variant="success">Scrape Recipe</Button>
            </Link>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default RecipeList;
