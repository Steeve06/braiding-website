import {
  formatCategoryLabel,
  formatDuration,
  formatPrice,
} from "../../utils/format.js";
import styles from "./StyleCard.module.css";

function StyleCard({ style }) {
  return (
    <article className={styles.card}>
      {style.hero_image && (
        <img src={style.hero_image} alt={style.name} className={styles.image} />
      )}
      <div className={styles.body}>
        <span className={styles.category}>
          {formatCategoryLabel(style.category)}
        </span>
        <h3 className={styles.name}>{style.name}</h3>
        <p className={styles.description}>{style.description}</p>

        <dl className={styles.specs}>
          <div className={styles.specRow}>
            <dt>Prep required</dt>
            <dd>{style.prep_required}</dd>
          </div>
          <div className={styles.specRow}>
            <dt>Duration</dt>
            <dd>{formatDuration(style.estimated_duration_minutes)}</dd>
          </div>
          <div className={styles.specRow}>
            <dt>Maintenance</dt>
            <dd>{style.maintenance_guidelines}</dd>
          </div>
        </dl>

        <p className={styles.price}>
          Starting at {formatPrice(style.starting_price)}
        </p>
      </div>
    </article>
  );
}

export default StyleCard;
