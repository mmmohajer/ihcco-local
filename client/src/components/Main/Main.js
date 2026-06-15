"use client";

import { useEffect, useState } from "react";

import styles from "./Main.module.css";
import { wsHandler } from "./utils";

import DashboardSidebar from "./subs/DashboardSidebar";
import TopStats from "./subs/TopStats";
import LiveView from "./subs/LiveView";
import CountPanel from "./subs/CountPanel";
import ResetPanel from "./subs/ResetPanel";
import RecentActivity from "./subs/RecentActivity";

const Main = () => {
  const [state, setState] = useState({
    count: 0,
    status: "Disconnected",
    resetValue: "",
  });

  useEffect(() => {
    const ws = new WebSocket("ws://localhost/ws/people-counter");
    return wsHandler(ws, setState);
  }, []);

  return (
    <main className={styles.page}>
      <DashboardSidebar />

      <section className={styles.content}>
        <div className={styles.header}>
          <div>
            <p className={styles.eyebrow}>IHCCO Smart System</p>
            <h1>People Counter Dashboard</h1>
            <p className={styles.subtitle}>
              Real-time occupancy monitoring for the cultural center.
            </p>
          </div>

          <div className={styles.statusPill}>
            <span
              className={`${styles.statusDot} ${
                state.status === "Connected" ? styles.connected : styles.error
              }`}
            />
            {state.status}
          </div>
        </div>

        <TopStats count={state.count} status={state.status} />

        <div className={styles.grid}>
          <div className={styles.leftColumn}>
            <LiveView />
          </div>

          <div className={styles.rightColumn}>
            <CountPanel count={state.count} />
            <ResetPanel state={state} setState={setState} />
            <RecentActivity count={state.count} status={state.status} />
          </div>
        </div>
      </section>
    </main>
  );
};

export default Main;
