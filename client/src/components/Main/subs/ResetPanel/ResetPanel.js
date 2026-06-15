import { RotateCcw } from "lucide-react";

import styles from "./ResetPanel.module.css";
import { handleReset } from "../../utils";

const ResetPanel = ({ state, setState }) => {
  return (
    <section className={styles.card}>
      <div className={styles.header}>
        <div>
          <p>Manual Control</p>
          <h3>Adjust Count</h3>
        </div>

        <RotateCcw size={20} />
      </div>

      <div className={styles.form}>
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

        <button onClick={() => handleReset(state, setState)}>
          Reset Count
        </button>
      </div>
    </section>
  );
};

export default ResetPanel;
