import { Users } from "lucide-react";

import styles from "./CountPanel.module.css";

const CountPanel = ({ count }) => {
  return (
    <section className={styles.card}>
      <div className={styles.iconBox}>
        <Users size={28} />
      </div>

      <p>Current Occupancy</p>
      <h2>{count}</h2>
      <span>People currently inside</span>

      <div className={styles.progress}>
        <div
          className={styles.progressFill}
          style={{ width: `${Math.min(count * 5, 100)}%` }}
        />
      </div>
    </section>
  );
};

export default CountPanel;
