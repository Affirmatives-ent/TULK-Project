// Utils
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import React, { lazy, Suspense, useState } from "react";

// Pages
import Loader from "./components/Loader/Loader";
import Navbar from "./components/Navbar/Navbar";
import Login from "./pages/Login/Login";
import Sidebar from "./components/Sidebar/Sidebar";
import NotificationPopup from "./components/Notifications/NotificationPopup";

// lazy load pages
const Home = lazy(() => import("./pages/Home/Home"));
const Profile = lazy(() => import("./pages/Profile/Profile"));
const NewsPage = lazy(() => import("./pages/NewsPage/NewsPage"));
const Group = lazy(() => import("./pages/Group/Group"));
const Messenger = lazy(() => import("./pages/Messenger/Messenger"));
const SearchResult = lazy(() => import("./pages/SearchResult/SearchResult"));
const Notifications = lazy(() =>
  import("./components/Notifications/Notifications")
);
const CreateGroup = lazy(() => import("./components/CreateGroup/CreateGroup"));

function App() {
  // toggle sidebar
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // toggle notification
  const [notificationOpen, setNotificationOpen] = useState(false);

  return (
    <>
      <Router>
        <Navbar
          setSidebarOpen={setSidebarOpen}
          setNotificationOpen={setNotificationOpen}
        />
        <div className="margin-top-container">
          <Routes>
            <Route
              index
              element={
                <Suspense fallback={<Loader />}>
                  <Home />
                </Suspense>
              }
            />
            <Route
              path="/searchResult"
              element={
                <Suspense fallback={<Loader />}>
                  <SearchResult />
                </Suspense>
              }
            />
            <Route
              path="/profile"
              element={
                <Suspense fallback={<Loader />}>
                  <Profile />
                </Suspense>
              }
            />
            <Route
              path="/group"
              element={
                <Suspense fallback={<Loader />}>
                  <Group />
                </Suspense>
              }
            />
            <Route
              path="/create-group"
              element={
                <Suspense fallback={<Loader />}>
                  <CreateGroup />
                </Suspense>
              }
            />

            <Route path="/login" element={<Login />} />
            <Route
              path="/newsPage"
              element={
                <Suspense fallback={<Loader />}>
                  <NewsPage />
                </Suspense>
              }
            />
            <Route
              path="/messenger"
              element={
                <Suspense fallback={<Loader />}>
                  <Messenger />
                </Suspense>
              }
            />

            <Route
              path="/notifications"
              element={
                <Suspense fallback={<Loader />}>
                  <Notifications />
                </Suspense>
              }
            />
          </Routes>
          {sidebarOpen && <Sidebar setSidebarOpen={setSidebarOpen} />}
          {notificationOpen && (
            <NotificationPopup setNotificationOpen={setNotificationOpen} />
          )}
        </div>
      </Router>
    </>
  );
}

export default App;
