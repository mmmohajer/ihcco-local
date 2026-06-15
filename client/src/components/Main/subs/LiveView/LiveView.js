import { Camera } from "lucide-react";

import styles from "./LiveView.module.css";

const LiveView = () => {
  return (
    <section className={styles.card}>
      <div className={styles.header}>
        <div>
          <p>Live Camera</p>
          <h2>Entrance Monitoring</h2>
        </div>

        <div className={styles.badge}>
          <Camera size={16} />
          Live
        </div>
      </div>

      <div className={styles.videoWrap}>
        <img
          src="/api/people-counter/live-view"
          alt="Live camera view"
          className={styles.video}
        />
      </div>
    </section>
  );
};

export default LiveView;
