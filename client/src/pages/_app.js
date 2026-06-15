import { useEffect } from "react";
import { useRouter } from "next/router";
import { Provider } from "react-redux";
import Script from "next/script";

import "@fontsource/inter/400.css";
import "@fontsource/inter/500.css";
import "@fontsource/inter/600.css";
import "@fontsource/inter/700.css";

import { store } from "@/root/src/store";

import "@/styles/globals.css";

const App = ({ Component, pageProps }) => {
  const router = useRouter();

  return (
    <>
      {/* -------------------------------- */}
      {/* Main App with Redux Provider */}
      {/* -------------------------------- */}
      <Provider store={store}>
        <Component {...pageProps} />
      </Provider>
    </>
  );
};

export default App;
