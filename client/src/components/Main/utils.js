export const wsHandler = (ws, setState) => {
  ws.onopen = () =>
    setState((prevState) => ({
      ...prevState,
      status: "Connected",
    }));

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    setState((prevState) => ({
      ...prevState,
      count: data.people_count,
      maxCount: data.max_people_count,
      totalEntries: data.total_entries_today,
    }));
  };

  ws.onerror = () =>
    setState((prevState) => ({
      ...prevState,
      status: "Error",
    }));

  ws.onclose = () =>
    setState((prevState) => ({
      ...prevState,
      status: "Disconnected",
    }));

  return () => ws.close();
};

export const handleReset = async (state, setState) => {
  const value = Number(state.resetValue);

  if (Number.isNaN(value) || value < 0) {
    alert("Please enter a valid number");
    return;
  }

  // --------------------------------------------------
  // --------------------------------------------------
  const apiProtocol = window.location.protocol === "https:" ? "https" : "http";
  const apiUrl = `${apiProtocol}://${window.location.hostname}:8000/api/people-counter/count/reset/`;
  // --------------------------------------------------
  // --------------------------------------------------
  // const apiUrl = "http://localhost:8000/api/people-counter/count/reset/"
  try {
    await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        people_count: value,
      }),
    });
  } catch (err) {
    console.log(err);
  }

  setState((prevState) => ({
    ...prevState,
    resetValue: "",
  }));
};
