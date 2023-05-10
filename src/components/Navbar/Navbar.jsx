// utils
import { NavLink, useNavigate } from "react-router-dom";
import { useState } from "react";

// style
import "./navbar.css";

// images
import logo from "../../images/logo.png";
import profilePhoto from "../../images/image-25.png";

// icons
import { GrHomeRounded } from "react-icons/gr";
import { SlPeople } from "react-icons/sl";
import { GrGroup } from "react-icons/gr";
import { BsChatLeftDots, BsBell, BsSearch } from "react-icons/bs";

export default function Navbar() {
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
  return (
    <div className="navbar">
      <div className="navbar-left">
        <div className="navbar-logo">
          <img src={logo} alt="logo" />
        </div>
      </div>
      <div className="navbar-center">
        <NavLink to="/">
          <GrHomeRounded className="navbar-icon" />
        </NavLink>

        <NavLink to="/profile">
          <SlPeople className="navbar-icon" />
        </NavLink>

        <NavLink to="/group">
          <GrGroup className="navbar-icon" />
        </NavLink>

        <BsChatLeftDots className="navbar-icon" />
      </div>
      <div className="navbar-right-space"></div>
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
          <BsBell />
        </div>
        <div className="navbar-profile-link">
          <img src={profilePhoto} alt="profile link" />
        </div>
      </div>
    </div>
  );
}
