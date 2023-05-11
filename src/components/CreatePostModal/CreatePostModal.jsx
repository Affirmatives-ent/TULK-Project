// styles
import "./createPostModal.css";

// images
import userImg from "../../images/image-25.png";

// icons
import { IoIosClose } from "react-icons/io";
import { MdOutlinePermMedia } from "react-icons/md";

export default function CreatePostModal({ setCreatePostModal }) {
  // function to hide create post modal when hide button is clicked
  const hideCreatePostModal = () => {
    setCreatePostModal(false);
  };
  return (
    <div className="create-post-modal">
      <div className="create-post-modal-container">
        <div className="create-post-modal-container-header mt-sm">
          <h3 className="h-100">Create Post</h3>
          <div className="close-post-modal-btn" onClick={hideCreatePostModal}>
            <IoIosClose />
          </div>
        </div>

        <div className="create-post-modal-container-user-image-add-file mt-xsm">
          <div className="create-post-modal-container-user-image">
            <img src={userImg} alt="" />
          </div>
          <div className="create-post-modal-container-add-file">
            <label htmlFor="createPostFileInput">
              <p className="text-body">Add File</p>
              <MdOutlinePermMedia />
            </label>
            <input
              type="file"
              id="createPostFileInput"
              multiple="multiple"
              hidden
            />
          </div>
        </div>

        <div className="create-post-modal-container-textarea mt-xsm">
          <textarea
            id="createPostInputText"
            placeholder="Create Post..."
          ></textarea>
        </div>

        <div className="create-post-modal-container-cta mt-xsm">
          <button className="btn-solid">Create Post</button>
        </div>
      </div>
    </div>
  );
}
