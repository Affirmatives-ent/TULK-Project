// utils

// styles
import "./profile.css";

// images
import profileCoverPhoto from "../../images/flowers-276014__340 1.png";
import profileUserAvatar from "../../images/image-25.png";

// components
import UserPhotos from "../../components/UserPhotos/UserPhotos";
import UserFriends from "../../components/UserFriends/UserFriends";

// functions

export default function Profile() {
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
            <h2 className="h-200">Oludare Adebayo</h2>
            <div className="profile-user-slogan mt-xsm">
              <p>The man with the style</p>
            </div>
          </div>

          <div className="profile-user-edit-button">
            <button className="btn-secondary">Edit Profile</button>
          </div>
        </div>
      </div>

      <div className="profile-user-info">
        <h3 className="h-100">Works at: Affirmatives Entertainment </h3>
        <h3 className="h-100">Studied at: University of Lagos</h3>
        <h3 className="h-100">Marital Status: Single</h3>
        <h3 className="h-100">Birthday: 30 December </h3>
        <h3 className="h-100">Contact: 08072940649 </h3>
        <h3 className="h-100">Email: affirmatives.ent@gmail.com</h3>
        <h3 className="h-100">Web: tulkonline.com</h3>
      </div>

      <div className="profile-action-buttons">
        <p className="active">Photos & Media</p>
        <p>Friends</p>
        <p>My Groups</p>
        <p>My Posts</p>
      </div>

      <UserFriends />
    </div>
  );
}
