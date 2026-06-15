import { Activity, Camera, Users } from "lucide-react";

import styles from "./TopStats.module.css";

const TopStats = ({ count, status }) => {
  const stats = [
    {
      label: "Current Count",
      value: count,
      helper: "People inside",
      icon: Users,
    },
    {
      label: "Camera Status",
      value: status,
      helper: "Live connection",
      icon: Camera,
    },
    {
      label: "System Mode",
      value: "Live",
      helper: "Real-time tracking",
      icon: Activity,
    },
  ];

  return (
    <div className={styles.stats}>
      {stats.map((item) => {
        const Icon = item.icon;

        return (
          <article key={item.label} className={styles.card}>
            <div className={styles.iconBox}>
              <Icon size={22} />
            </div>

            <div>
              <p>{item.label}</p>
              <h3>{item.value}</h3>
              <span>{item.helper}</span>
            </div>
          </article>
        );
      })}
    </div>
  );
};

export default TopStats;
