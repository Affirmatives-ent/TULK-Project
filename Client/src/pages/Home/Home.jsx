import React from "react";

// styles
import "./home.css";

// utils
import { useState } from "react";

// images
import profilePhoto from "../../images/image-25.png";

// components
import NewPeople from "../../components/newPeople/NewPeople";
import Friends from "../../components/Friends/Friends";
import Groups from "../../components/groups/Groups";
import MessageContacts from "../../components/MessageContacts/MessageContacts";
import Stories from "../../components/Stories/Stories";
import CreatePost from "../../components/CreatePost/CreatePost";
import Newsreel from "../../components/Newsreel/Newsreel";
import Post from "../../components/Post/Post";
import ChatPopup from "../../components/ChatPopup/ChatPopup";
import Chat from "../../components/Chat/Chat";

// data
import { posts } from "../../data/data";

// Show only 20 posts
let minPosts = posts.slice(1, 20);

export default function Home() {
  // variable to store state of chat Modal whether active or not
  const [showChatModal, setShowChatModal] = useState(false);

  // function to switch feed
  // variable to hold feeds state
  const [feedsSwitched, setFeedsSwitched] = useState(true);
  const switchFeed = () => {
    document.getElementById("toggleFeed").classList.toggle("active");
    setFeedsSwitched(!feedsSwitched);
  };

  return (
    <div className="home-container">
      <div className="home-left">
        <div className="home-left-profile-link">
          <img src={profilePhoto} alt="" />
          <h3 className="h-100">Oludare Omolaja</h3>
        </div>
        <NewPeople />
        <Friends />
        <Groups />
        <MessageContacts />
        <ChatPopup />
      </div>
      <div className={feedsSwitched ? "home-center" : "home-right"}>
        {showChatModal && <Chat setShowChatModal={setShowChatModal} />}
        {/* <Stories /> */}
        <CreatePost />
        {minPosts.map((post) => {
          return <Post post={post} key={post.id} />;
        })}
      </div>
      <div className="home-right-toggle-feed">
        <div className="toggle-feed" id="toggleFeed" onClick={switchFeed}>
          <p className="body-text">Switch Feed</p>
          <div className="feed-toggler-container">
            <div className="feed-toggler-thumb"></div>
          </div>
        </div>
      </div>
      <div className={feedsSwitched ? "home-right" : "home-center"}>
        <Newsreel feedsSwitched={feedsSwitched} />
      </div>
    </div>
  );
}
