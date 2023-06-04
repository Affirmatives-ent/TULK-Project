// utils
import { NavLink, Link, useLocation, useNavigate } from "react-router-dom";
import React, { useState } from "react";

// style
import "./navbar.css";

// images
import logo from "../../images/logo.png";
import profilePhoto from "../../images/image-25.png";

// icons
import homeIconSolid from "../../images/icons/home-icon-solid.png";
import homeIconOutline from "../../images/icons/home-icon-outline.png";
import groupIconSolid from "../../images/icons/group-icon-solid.png";
import groupIconOutline from "../../images/icons/group-icon-outline.png";
import chatIconSolid from "../../images/icons/chat-icon-solid.png";
import chatIconOutline from "../../images/icons/chat-icon-outline.png";
import profileIconSolid from "../../images/icons/profile-icon-solid.png";
import profileIconOutline from "../../images/icons/profile-icon-outline.png";

import { BsSearch, BsBell } from "react-icons/bs";
import { FaBars } from "react-icons/fa";

export default function Navbar({ setSidebarOpen, setNotificationOpen }) {
  // store the search input in a variable
  const [searchInput, setSearchInput] = useState("");

  // react hook to be used to redirect user to search result page
  const navigate = useNavigate();

  // function to redirect user to search result page on search
  const showSearchResult = (e) => {
    e.preventDefault();

    // navigate user to search result page if search entry is not blank
    if (searchInput.trim() !== "") {
      navigate("/searchResult");
    }
  };

  // function to hide user icon from navbar in login page
  const location = useLocation();

  return (
    <div className="navbar">
      <div className="navbar-lg-screen">
        <div className="navbar-left">
          <div className="navbar-logo">
            <NavLink to="/">
              <img src={logo} alt="logo" />
            </NavLink>
          </div>
        </div>
        <div className="navbar-center">
          <NavLink to="/">
            <img src={homeIconSolid} alt="" />
          </NavLink>

          <NavLink to="/profile">
            <img src={profileIconSolid} alt="" />
          </NavLink>

          <NavLink to="/group">
            <img src={groupIconSolid} alt="" />
          </NavLink>

          <NavLink to="/messenger">
            <img src={chatIconSolid} alt="" />
          </NavLink>
        </div>
        <div className="navbar-empty-space"></div>
        <div className="navbar-right">
          <div className="navbar-search">
            <BsSearch />
            <form onSubmit={showSearchResult}>
              <input
                type="text"
                placeholder="Search Tulk"
                onChange={(e) => setSearchInput(e.target.value)}
              />
            </form>
          </div>
          <div className="navbar-notification">
            <BsBell onClick={() => setNotificationOpen((prev) => !prev)} />
          </div>
          <div className="navbar-profile-link">
            <Link to="/profile">
              <img src={profilePhoto} alt="profile link" />
            </Link>
          </div>
        </div>
        <div className="navbar-mobile-links">
          <div className="navbar-mobile-search-input">
            <BsSearch />
            <form onSubmit={showSearchResult}>
              <input
                type="text"
                placeholder="Search Tulk"
                onChange={(e) => setSearchInput(e.target.value)}
              />
            </form>
          </div>
          {location.pathname !== "/login" && (
            <div className="navbar-mobile-burger">
              <FaBars
                className="burger-icon"
                onClick={() => setSidebarOpen((prev) => !prev)}
              />
            </div>
          )}
        </div>
      </div>

      {location.pathname !== "/login" && (
        <div className="navbar-sm-screen">
          <NavLink to="/newsPage">News</NavLink>
          <NavLink to="/">Social</NavLink>
          <NavLink to="/messenger">Chat</NavLink>
        </div>
      )}
    </div>
  );
}
