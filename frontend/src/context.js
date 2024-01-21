import { createContext, useContext, useState } from "react"

const usePageState = () => {
  const [url, setUrl] = useState('');
  const [isUrlSubmitted, setIsUrlSubmitted] = useState(false);
  
  return {
    url,
    setUrl,
    isUrlSubmitted,
    setIsUrlSubmitted,
  };
}

const PageContext = createContext(null);

export const PageContextProvider = ({ children }) => (
  <PageContext.Provider value={usePageState()}>{children}</PageContext.Provider>
);

export const usePageContext = () => useContext(PageContext);
