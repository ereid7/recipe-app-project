import React from "react";
import { Link } from "react-router-dom";
import { Container, Navbar } from "react-bootstrap";

const Header = () => {
  return (
    <Navbar bg="light" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">Recipe App</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <div className="navbar-nav">
            <Link className="nav-link" to="/">Recipes</Link>
            <Link className="nav-link" to="/scrape-recipe">Scrape Recipe</Link>
          </div>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;
