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
  return (
    <header className={styles.header}>
      <div className={styles.brand}>Braids by Miah</div>
      <nav className={styles.nav} aria-label="Main navigation">
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
