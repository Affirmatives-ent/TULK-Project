// Utils
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";

// Pages
import Navbar from "./components/Navbar/Navbar";
import Home from "./pages/Home/Home";
import Profile from "./pages/Profile/Profile";
import Group from "./pages/Group/Group";
import SearchResult from "./pages/SearchResult/SearchResult";
import Login from "./pages/Login/Login";
import NewsPage from "./pages/NewsPage/NewsPage";
import Messenger from "./pages/Messenger/Messenger";

function App() {
  const [sidebarActive, setSidebarActive] = useState(false);
  return (
    <>
      <Router>
        <Navbar
          sidebarActive={sidebarActive}
          setSidebarActive={setSidebarActive}
        />
        <div className="margin-top-container">
          <Routes>
            <Route index element={<Home />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/group" element={<Group />} />
            <Route path="/searchResult" element={<SearchResult />} />
            <Route path="/login" element={<Login />} />
            <Route path="/newsPage" element={<NewsPage />} />
            <Route path="/messenger" element={<Messenger />} />
          </Routes>
        </div>
      </Router>
    </>
  );
}

export default App;
