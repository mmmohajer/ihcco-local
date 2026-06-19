import { Activity, Camera, Users, TrendingUp, DoorOpen } from "lucide-react";

import styles from "./TopStats.module.css";

const TopStats = ({ count, maxCount, totalEntries, status }) => {
  const statusStats = [
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

  const countStats = [
    {
      label: "Current Count",
      value: count,
      helper: "People inside",
      icon: Users,
    },
    {
      label: "Peak Today",
      value: maxCount,
      helper: "Maximum occupancy",
      icon: TrendingUp,
    },
    {
      label: "Entries Today",
      value: totalEntries,
      helper: "Total entrances",
      icon: DoorOpen,
    },
  ];

  const renderCard = (item) => {
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
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.statusStats}>{statusStats.map(renderCard)}</div>

      <div className={styles.countStats}>{countStats.map(renderCard)}</div>
    </div>
  );
};

export default TopStats;
