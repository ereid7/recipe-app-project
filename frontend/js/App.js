import * as Sentry from "@sentry/react";
import React from "react";
import { Provider } from "react-redux";
// import { BrowserRouter as Router, Routes, Route } from 'react-router';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import Home from "./pages/Home";
import configureStore from "./store";
import RecipeList from './components/RecipeList';
import ScrapeRecipe from "./components/ScrapeRecipe";
// import RecipeDetail from './components/RecipeDetail';
// import RecipeForm from './components/RecipeForm';
// import ScrapeRecipe from './components/ScrapeRecipe';

const store = configureStore({});

const router = createBrowserRouter([
  {
    path: "/",
    element: <RecipeList />,
  },
  {
    path: "/scrape-recipe",
    element: <ScrapeRecipe />,
  },
]);

const App = () => (
  
  <Sentry.ErrorBoundary fallback={<p>An error has occurred</p>}>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </Sentry.ErrorBoundary>
);

export default App;
