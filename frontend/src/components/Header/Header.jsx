import { useState } from "react";
import { NavLink } from "react-router-dom";
import styles from "./Header.module.css";

const navLinks = [
  { to: "/", label: "Home", end: true },
  { to: "/styles-pricing", label: "Styles & Pricing" },
  { to: "/gallery", label: "Gallery" },
  { to: "/about", label: "About" },
  { to: "/reviews", label: "Reviews" },
];

function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  function toggleMenu() {
    setIsMenuOpen((previousState) => !previousState);
  }

  function closeMenu() {
    setIsMenuOpen(false);
  }

  return (
    <header className={styles.header}>
      <div className={styles.brand}>Braids by Miah</div>

      <button
        type="button"
        className={styles.menuToggle}
        aria-expanded={isMenuOpen}
        aria-controls="primary-navigation"
        aria-label={
          isMenuOpen ? "Close navigation menu" : "Open navigation menu"
        }
        onClick={toggleMenu}
      >
        <span className={styles.menuIconBar}></span>
        <span className={styles.menuIconBar}></span>
        <span className={styles.menuIconBar}></span>
      </button>

      <nav
        id="primary-navigation"
        className={`${styles.nav} ${isMenuOpen ? styles.navOpen : ""}`}
        aria-label="Main navigation"
      >
        <ul className={styles.navList}>
          {navLinks.map((link) => (
            <li key={link.to}>
              <NavLink
                to={link.to}
                end={link.end}
                className={({ isActive }) =>
                  isActive
                    ? `${styles.navLink} ${styles.navLinkActive}`
                    : styles.navLink
                }
                onClick={closeMenu}
              >
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <NavLink to="/book-now" className={styles.ctaButton}>
        Book Now
      </NavLink>
    </header>
  );
}

export default Header;
