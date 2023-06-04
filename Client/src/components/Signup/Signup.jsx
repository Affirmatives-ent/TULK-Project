import React from "react";

// styles
import "./signup.css";

// icons
import { IoIosClose } from "react-icons/io";

export default function Signup({ setSignupModalVisible }) {
  return (
    <div className="signupPage">
      <div className="signup">
        <div className="signup-header">
          <div className="easy-signup">
            <h2 className="h-200">
              <span>Easy</span> <br />
              Sign Up
            </h2>
          </div>
          <div
            className="signup-close-btn"
            onClick={() => {
              setSignupModalVisible(false);
            }}
          >
            <IoIosClose />
          </div>
        </div>

        <div className="signup-body">
          <div className="signup-body-inputs">
            <span>
              <input type="text" placeholder="First Name ..." />
              <input type="text" placeholder="Surname Name ..." />
            </span>
            <input
              type="text"
              placeholder="Mobile Number or Email Address ..."
            />
            <input type="password" placeholder="New Password ..." />
            <input type="password" placeholder="Confirm Password ..." />

            <div className="signup-body-input-dob">
              <p>Date of Birth</p>
              <input type="date" className="mt-xsm" />
            </div>
            <div className="gender-input">
              <p>Gender</p>
              <select name="gender-input" id="gender-input" className="mt-xsm">
                <option value="male">Male</option>
                <option value="female">female</option>
                <option value="confidential">Confidential</option>
              </select>
            </div>
          </div>

          <div className="signup-body-terms mt-md">
            <p>
              By clicking Sign Up, you agree to our <a href="#">Terms</a>,{" "}
              <a href="#">Privacy Policy</a> and
              <a href="#">Cookies Policy</a>. You may receive SMS notifications
              from us and can opt out at any time.
            </p>
          </div>
          <div className="signup-btn">
            <button className="btn-solid">Sign Up</button>
          </div>
        </div>
      </div>
    </div>
  );
}
