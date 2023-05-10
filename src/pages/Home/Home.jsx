import "./home.css";
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

export default function Home() {
  return (
    <div className="home">
      <div className="home-left">
        <div className="home-left-profile-link">
          <img src={profilePhoto} alt="profile photo" />
          <h3 className="h-100">Oludare Omolaja</h3>
        </div>
        <NewPeople />
        <Friends />
        <Groups />
        <MessageContacts />
      </div>
      <div className="home-center">
        <Stories />
        <CreatePost />
        <Post />
        <Post />
        <Post />
        <Post />
        <Post />
      </div>
      <div className="home-right-toggle-feed"></div>
      <div className="home-right">
        <News />
      </div>
    </div>
  );
}
