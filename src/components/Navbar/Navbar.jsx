// utils
import { NavLink, BrowserRouter as Router } from "react-router-dom";

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

        <GrGroup className="navbar-icon" />
        <BsChatLeftDots className="navbar-icon" />
      </div>
      <div className="navbar-right-space"></div>
      <div className="navbar-right">
        <div className="navbar-search">
          <BsSearch />
          <input type="text" placeholder="Search Tulk" />
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
