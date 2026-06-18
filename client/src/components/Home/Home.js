"use client";

import { useEffect, useState } from "react";

import { wsHandler, handleReset } from "./utils";

const Home = () => {
  const [state, setState] = useState({
    count: 0,
    status: "Disconnected",
    resetValue: "",
  });

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/people-counter");
    return wsHandler(ws, setState);
  }, []);

  return (
    <div>
      <h1>People Counter</h1>

      <p>Status: {state.status}</p>
      <p>Count: {state.count}</p>

      <input
        type="number"
        value={state.resetValue}
        onChange={(event) =>
          setState((prevState) => ({
            ...prevState,
            resetValue: event.target.value,
          }))
        }
        placeholder="Set count"
      />

      <button onClick={() => handleReset(state, setState)}>Reset Count</button>
    </div>
  );
};

export default Home;
