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

  try {
  await fetch("http://localhost:8000/api/people-counter/count/reset/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      people_count: value,
    }),
  })} catch(err) {
    console.log(err)
  }

  setState((prevState) => ({
    ...prevState,
    resetValue: "",
  }));
};
