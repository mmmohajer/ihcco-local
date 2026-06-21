import { Camera } from "lucide-react";

import styles from "./LiveView.module.css";

const LiveView = () => {
  const apiProtocol =
    typeof window !== "undefined" && window.location.protocol === "https:"
      ? "https"
      : "http";

  const liveViewUrl =
    typeof window !== "undefined"
      ? `${apiProtocol}://${window.location.hostname}:8000/api/people-counter/live-view`
      : "";

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
        {liveViewUrl && (
          <img
            src={liveViewUrl}
            alt="Live camera view"
            className={styles.video}
          />
        )}
      </div>
    </section>
  );
};

export default LiveView;
