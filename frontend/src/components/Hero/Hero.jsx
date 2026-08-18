import { NavLink } from "react-router-dom";
import styles from "./Hero.module.css";

function Hero() {
  return (
    <section className={styles.hero} aria-label="Braids by Miah hero banner">
      <div className={styles.heroContent}>
        <p className={styles.heroEyebrow}>Braids by Miah</p>
        <h1 className={styles.heroHeading}>Artistry in Every Braid</h1>
        <p className={styles.heroLocation}>Serving Atlanta, GA</p>
        <div className={styles.availabilityBadge}>
          <span className={styles.badgeDot} aria-hidden="true"></span>
          Now booking — limited slots this month
        </div>
        <div>
          <NavLink to="/book-now" className={styles.heroCta}>
            Book Your Appointment
          </NavLink>
        </div>
      </div>
    </section>
  );
}

export default Hero;
