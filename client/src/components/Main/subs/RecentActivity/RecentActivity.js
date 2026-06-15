import { CheckCircle2, Clock, Radio } from "lucide-react";

import styles from "./RecentActivity.module.css";

const RecentActivity = ({ count, status }) => {
  const items = [
    {
      icon: Radio,
      title: "Live count update",
      detail: `${count} people detected inside`,
    },
    {
      icon: CheckCircle2,
      title: "System status",
      detail: status,
    },
    {
      icon: Clock,
      title: "Last sync",
      detail: "Updating every second",
    },
  ];

  return (
    <section className={styles.card}>
      <h3>Recent Activity</h3>

      <div className={styles.list}>
        {items.map((item) => {
          const Icon = item.icon;

          return (
            <div key={item.title} className={styles.item}>
              <div className={styles.iconBox}>
                <Icon size={17} />
              </div>

              <div>
                <p>{item.title}</p>
                <span>{item.detail}</span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default RecentActivity;
