import * as Sentry from "@sentry/react";
import React from "react";
import { Provider } from "react-redux";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import configureStore from "./store";
import RecipeList from './components/RecipeList';
import ScrapeRecipe from "./components/ScrapeRecipe";
import RecipeDetail from './components/RecipeDetail'; // Import the RecipeDetail component
import Layout from "./components/Layout";

const store = configureStore({});

const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <Layout>
        <RecipeList />
      </Layout>
    ),
  },
  {
    path: "/scrape-recipe",
    element: (
      <Layout>
        <ScrapeRecipe />
      </Layout>
    ),
  },
  {
    path: "/recipe/:recipeId", // Add a route for recipe details
    element: (
      <Layout>
        <RecipeDetail />
      </Layout>
    ),
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
