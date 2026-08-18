import { useMemo, useState } from "react";
import useFetch from "../hooks/useFetch.js";
import StyleCard from "../components/StyleCard/StyleCard.jsx";
import { formatCategoryLabel } from "../utils/format.js";
import styles from "./StylesPricingPage.module.css";

function StylesPricingPage() {
  const { data: allStyles, isLoading, error } = useFetch("/styles/");
  const [activeCategory, setActiveCategory] = useState("all");

  const categories = useMemo(() => {
    if (!allStyles) return [];
    return Array.from(new Set(allStyles.map((style) => style.category)));
  }, [allStyles]);

  const filteredStyles = useMemo(() => {
    if (!allStyles) return [];
    if (activeCategory === "all") return allStyles;
    return allStyles.filter((style) => style.category === activeCategory);
  }, [allStyles, activeCategory]);

  if (isLoading) {
    return (
      <section className={styles.page}>
        <p>Loading styles...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className={styles.page}>
        <p>Something went wrong loading styles: {error}</p>
      </section>
    );
  }

  return (
    <section className={styles.page}>
      <h1>Styles & Pricing</h1>

      <div
        className={styles.filters}
        role="group"
        aria-label="Filter styles by category"
      >
        <button
          type="button"
          className={
            activeCategory === "all"
              ? `${styles.filterButton} ${styles.filterButtonActive}`
              : styles.filterButton
          }
          onClick={() => setActiveCategory("all")}
        >
          All
        </button>
        {categories.map((category) => (
          <button
            key={category}
            type="button"
            className={
              activeCategory === category
                ? `${styles.filterButton} ${styles.filterButtonActive}`
                : styles.filterButton
            }
            onClick={() => setActiveCategory(category)}
          >
            {formatCategoryLabel(category)}
          </button>
        ))}
      </div>

      {filteredStyles.length === 0 ? (
        <p>No styles found in this category yet.</p>
      ) : (
        <div className={styles.grid}>
          {filteredStyles.map((style) => (
            <StyleCard key={style.id} style={style} />
          ))}
        </div>
      )}
    </section>
  );
}

export default StylesPricingPage;
