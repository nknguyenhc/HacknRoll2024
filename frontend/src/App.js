import React from 'react';
import "./App.css";
import Main from "./components/Main";
import Navbar from './components/NavBar';
import Videos from './components/Videos';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#2272FF',
    },
    secondary: {
      main: '#FFFFFF',
    },
  },
});

function App() {
  // return (
  //   <div className="App">
  //     <header className="App-header">
  //       <img src={logo} className="App-logo" alt="logo" />
  //       <p>
  //         Edit <code>src/App.js</code> and save to reload.
  //       </p>
  //       <a
  //         className="App-link"
  //         href="https://reactjs.org"
  //         target="_blank"
  //         rel="noopener noreferrer"
  //       >
  //         Learn React
  //       </a>
  //     </header>
  //   </div>
  // );
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" exact component={Main} />
          <Route path="/videos" component={Videos} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
