import "./createPost.css";

// icons
import { VscSmiley } from "react-icons/vsc";
import { MdPermMedia } from "react-icons/md";

// images
import postUserImg from "../../images/image-25.png";

export default function CreatePost() {
  return (
    <div className="createPostDiv">
      <div className="createPost">
        <div className="create-post-user-img">
          <img src={postUserImg} alt="" />
        </div>
        <div className="create-post-textarea">
          <textarea rows="2" placeholder="Create Post..."></textarea>
          <VscSmiley className="createPostIcon" />
        </div>
      </div>

      <div className="create-post-insert-media">
        <MdPermMedia className="create-post-insert-media-icon" />
        <p className="text-body">Upload Photo / Video</p>
      </div>
    </div>
  );
}
