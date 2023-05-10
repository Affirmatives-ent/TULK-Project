// Utils
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Pages
import Navbar from "./components/Navbar/Navbar";
import Home from "./pages/Home/Home";
import Profile from "./pages/Profile/Profile";
import Group from "./pages/Group/Group";
import SearchResult from "./pages/SearchResult/SearchResult";

function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Routes>
          <Route index element={<Home />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/group" element={<Group />} />
          <Route path="/searchResult" element={<SearchResult />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
