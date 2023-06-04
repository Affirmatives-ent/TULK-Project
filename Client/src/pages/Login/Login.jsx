import React from "react";

// styles
import "./login.css";

// utils
import { Link } from "react-router-dom";

// images
import welcomeImg from "../../images/TULK-hot-1.png";
import Newsreel from "../../components/Newsreel/Newsreel";
import { useState } from "react";
import Signup from "../../components/Signup/Signup";

export default function Login() {
  // variable to store sign up active state
  const [signupModalVisible, setSignupModalVisible] = useState(false);
  // function to open signup page modal when signup button is clicked

  const showSignUpModal = () => {
    setSignupModalVisible(true);
  };
  return (
    <div className="login">
      <div className="login-left">
        <div className="welcome-img">
          <img src={welcomeImg} alt="" />
        </div>
        <div className="login-form">
          <form className="login" onSubmit={(e) => e.preventDefault()}>
            <input type="text" placeholder="Email or phone ..." required />
            <input type="password" placeholder="Password" required />
            <Link to="/">
              <button type="submit" className="btn-solid">
                Login
              </button>
            </Link>
          </form>
          <div className="forgotten-password-link mt-xsm">
            <a href="#">Forgotten Password?</a>
          </div>
          <h2 className="h-100">OR</h2>
          <div className="signup-btn-modal-popup">
            <button className="btn-secondary" onClick={showSignUpModal}>
              Create Account
            </button>
          </div>
        </div>
      </div>
      {signupModalVisible && (
        <Signup setSignupModalVisible={setSignupModalVisible} />
      )}
      <div className="login-right">
        <div className="news-nav">
          <ul>
            <li className="active">All News</li>
            <li>Sport</li>
            <li>Politics</li>
            <li>Metro</li>
            <li>Entertainment & More</li>
          </ul>
        </div>
        <Newsreel loginPage />
      </div>
    </div>
  );
}
