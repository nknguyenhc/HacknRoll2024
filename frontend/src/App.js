import "./App.css";
import Main from "./components/Main";
import Library from "./components/Library";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { SnackbarProvider } from "notistack";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import { PageContextProvider } from "./context";

const theme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#2272FF",
    },
    secondary: {
      main: "#FFFFFF",
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <SnackbarProvider maxSnack={3}>
        <Router>
          <PageContextProvider>
            <Navbar />
            <Routes>
              <Route path="/" element={<Main />} />
              <Route path="/library" element={<Library />} />
            </Routes>
          </PageContextProvider>
        </Router>
      </SnackbarProvider>
    </ThemeProvider>
  );
}

export default App;
