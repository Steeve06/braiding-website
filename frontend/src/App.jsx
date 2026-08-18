import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout/Layout.jsx";
import HomePage from "./pages/HomePage.jsx";
import StylesPricingPage from "./pages/StylesPricingPage.jsx";
import GalleryPage from "./pages/GalleryPage.jsx";
import AboutPage from "./pages/AboutPage.jsx";
import ReviewsPage from "./pages/ReviewsPage.jsx";
import BookNowPage from "./pages/BookNowPage.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="styles-pricing" element={<StylesPricingPage />} />
          <Route path="gallery" element={<GalleryPage />} />
          <Route path="about" element={<AboutPage />} />
          <Route path="reviews" element={<ReviewsPage />} />
          <Route path="book-now" element={<BookNowPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
