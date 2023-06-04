import React from "react";

// styles
import "./sidebar.css";

// images
import userImg from "../../images/image-25.png";

// icons
import notifBell from "../../images/icons/notif-bell.png";
import groupIconOutline from "../../images/icons/group-icon-outline.png";
import profileIconOutline from "../../images/icons/profile-icon-outline.png";

// utils
import { Link } from "react-router-dom";

const Sidebar = ({ setSidebarOpen }) => {
  return (
    <div className="sidebar-bg">
      <div className="sidebar">
        <Link to="/profile" onClick={() => setSidebarOpen((prev) => !prev)}>
          <div className="profile-link">
            <div className="profile-link-user-image">
              <img src={userImg} alt="" />
            </div>

            <div className="profile-link-display-name">
              <h3 className="h-100">Oludare Omolaja</h3>
              <small className="small-text">My Profile</small>
            </div>
          </div>
        </Link>

        <div className="sidebar-links">
          <Link to="/" onClick={() => setSidebarOpen((prev) => !prev)}>
            <div className="sidebar-link">
              <img src={profileIconOutline} alt="" />
              <p className="text-body"> Friends </p>
            </div>
          </Link>
          <Link to="/group" onClick={() => setSidebarOpen((prev) => !prev)}>
            <div className="sidebar-link">
              <img src={groupIconOutline} alt="" />
              <p className="text-body"> Groups </p>
            </div>
          </Link>
          <Link
            to="/notifications"
            onClick={() => setSidebarOpen((prev) => !prev)}
          >
            <div className="sidebar-link">
              <img src={notifBell} alt="" />
              <p className="text-body"> Notifications </p>
            </div>
          </Link>
        </div>

        <div
          className="logout-btn"
          onClick={() => setSidebarOpen((prev) => !prev)}
        >
          <Link to="/login">
            <button className="btn-secondary">Logout</button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
