// utils
import { useState } from "react";

// styles
import "./profile.css";

// images
import profileCoverPhoto from "../../images/flowers-276014__340 1.png";
import profileUserAvatar from "../../images/image-25.png";

// icons
import { FaEllipsisH } from "react-icons/fa";

// components
import UserPhotos from "../../components/UserPhotos/UserPhotos";
import UserFriends from "../../components/UserFriends/UserFriends";
import UserGroups from "../../components/UserGroups/UserGroups";
import CreatePost from "../../components/CreatePost/CreatePost";
import Post from "../../components/Post/Post";

// data
import { users, posts } from "../../data/data";

// buttons from DOM
const showFriendsBtn = document.getElementById("showFriendsBtn");
const showPhotosBtn = document.getElementById("showPhotosBtn");
const showGroupsBtn = document.getElementById("showGroupsBtn");

export default function Profile() {
  // variable to store current user
  const currentUser = users[8];

  const currentUserPosts = posts.filter((post) => {
    return post.userId === currentUser.id;
  });

  console.log(currentUserPosts);
  // functions
  const [showPhotos, setShowPhotos] = useState(true);
  const [showFriends, setShowFriends] = useState(false);
  const [showGroups, setShowGroups] = useState(false);

  // function to display user photos and media
  const showPhotosFunction = () => {
    // display only necessary component
    if (!showPhotos) {
      setShowPhotos(true);
    }
    setShowFriends(false);
    setShowGroups(false);

    // adds style to button
    if (!showPhotosBtn.classList.contains("active")) {
      showPhotosBtn.classList.add("active");
    }

    if (showFriendsBtn.classList.contains("active")) {
      showFriendsBtn.classList.remove("active");
    }

    if (showGroupsBtn.classList.contains("active")) {
      showGroupsBtn.classList.remove("active");
    }
  };

  // function to display user friends
  const showFriendsFunction = () => {
    // display only necessary component
    if (!showFriends) {
      setShowFriends(true);
    }
    setShowPhotos(false);
    setShowGroups(false);

    // adds style to button
    if (!showFriendsBtn.classList.contains("active")) {
      showFriendsBtn.classList.add("active");
    }

    if (showPhotosBtn.classList.contains("active")) {
      showPhotosBtn.classList.remove("active");
    }

    if (showGroupsBtn.classList.contains("active")) {
      showGroupsBtn.classList.remove("active");
    }
  };

  // function to display user groups
  const showGroupsFunction = () => {
    // display only necessary component
    if (!showGroups) {
      setShowGroups(true);
    }
    setShowPhotos(false);
    setShowFriends(false);

    // adds style to button
    if (!showGroupsBtn.classList.contains("active")) {
      showGroupsBtn.classList.add("active");
    }

    if (showFriendsBtn.classList.contains("active")) {
      showFriendsBtn.classList.remove("active");
    }

    if (showPhotosBtn.classList.contains("active")) {
      showPhotosBtn.classList.remove("active");
    }
  };

  return (
    <div className="profile">
      <div className="profile-user-data">
        <div className="profile-cover-photo">
          <img src={profileCoverPhoto} alt="" />
        </div>
        <div className="profile-user-image-name">
          <div className="profile-user-avatar">
            <img src={profileUserAvatar} alt="" />
          </div>
          <div className="profile-user-name-slogan">
            <h2 className="h-200">{currentUser.name}</h2>
            <div className="profile-user-slogan mt-xsm">
              <p>{currentUser.company.catchPhrase}</p>
            </div>
          </div>

          <div className="profile-user-edit-button">
            <button className="btn-secondary">
              <FaEllipsisH />
            </button>
          </div>
        </div>
      </div>

      <div className="profile-user-info">
        <h3 className="h-100">
          Works at: <b>{currentUser.company.name} </b>
        </h3>
        <h3 className="h-100">
          Studied at: <b>{currentUser.address.city}</b>
        </h3>
        <h3 className="h-100">
          Marital Status: <b>Single</b>
        </h3>
        <h3 className="h-100">
          Birthday: <b>30 December </b>
        </h3>
        <h3 className="h-100">
          Contact: <b>{currentUser.phone} </b>
        </h3>
        <h3 className="h-100">
          Email: <b>{currentUser.email}</b>
        </h3>
        <h3 className="h-100">
          Web: <b>{currentUser.website}</b>
        </h3>
      </div>

      <div className="profile-bottom-page">
        <div className="profile-bottom-page-left">
          <div className="profile-action-buttons">
            <p
              className="active"
              id="showPhotosBtn"
              onClick={showPhotosFunction}
            >
              Photos & Media
            </p>
            <p className="" id="showFriendsBtn" onClick={showFriendsFunction}>
              Friends
            </p>
            <p className="" id="showGroupsBtn" onClick={showGroupsFunction}>
              My Groups
            </p>
          </div>
          {showPhotos && <UserPhotos />}
          {showFriends && <UserFriends />}
          {showGroups && <UserGroups />}
          {/* {showFriends && <UserGroups />} */}
        </div>
        <div className="profile-bottom-page-right">
          <CreatePost />
          {currentUserPosts.map((currentUserPost) => {
            return <Post key={currentUserPost.id} post={currentUserPost} />;
          })}
        </div>
      </div>
    </div>
  );
}
