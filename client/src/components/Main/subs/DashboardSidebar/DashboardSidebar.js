import {
  Activity,
  BarChart3,
  Camera,
  Home,
  Settings,
  ShieldCheck,
} from "lucide-react";

import styles from "./DashboardSidebar.module.css";

const items = [
  { icon: Home, label: "Dashboard", active: true },
  { icon: Camera, label: "Live View" },
  { icon: Activity, label: "Occupancy" },
  { icon: BarChart3, label: "Reports" },
  { icon: Settings, label: "Settings" },
];

const DashboardSidebar = () => {
  return (
    <aside className={styles.sidebar}>
      <div className={styles.brand}>
        <img src="/ihcco-logo.jpeg" alt="IHCCO Logo" />
        <div>
          <h2>IHCCO</h2>
          <p>Cultural Centre</p>
        </div>
      </div>

      <nav className={styles.nav}>
        {items.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              className={`${styles.navItem} ${
                item.active ? styles.active : ""
              }`}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className={styles.footerCard}>
        <ShieldCheck size={24} />
        <h3>Secure Monitoring</h3>
        <p>Live occupancy insights for safer space management.</p>
      </div>
    </aside>
  );
};

export default DashboardSidebar;
