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
import News from "../../components/News/News";
import Post from "../../components/Post/Post";
import ChatPopup from "../../components/ChatPopup/ChatPopup";
import Chat from "../../components/Chat/Chat";

// data
import { posts } from "../../data/data";

export default function Home() {
  // variable to store state of chat Modal whether active or not
  const [showChatModal, setShowChatModal] = useState(false);

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
      <div className="home-center">
        {showChatModal && <Chat setShowChatModal={setShowChatModal} />}
        {/* <Stories /> */}
        <CreatePost />
        {posts.map((post) => {
          return <Post post={post} key={post.id} />;
        })}
      </div>
      {/* <div className="home-right-toggle-feed"></div> */}
      <div className="home-right">
        <News />
      </div>
    </div>
  );
}
