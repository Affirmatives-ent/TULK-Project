import React from "react";
// styles
import "./createGroup.css";

export default function CreateGroup() {
  return (
    <div className="create-group">
      <div className="create-group-bg-image">
        <input
          type="file"
          className="create-group-bg-image-input"
          id="createGroupBgImageInput"
        />
        <label
          htmlFor="createGroupBgImageInput"
          className="create-group-bg-image-label"
        >
          Add background Photo
        </label>
      </div>

      <div className="create-group-avatar">
        <input
          type="file"
          className="create-group-avatar-input"
          id="createGroupBgImageInput"
        />
        <label
          htmlFor="createGroupBgImageInput"
          className="create-group-avatar-label"
        >
          Add <br />
          Photo
        </label>
      </div>

      <div className="create-group-input-fields">
        <input type="text" placeholder="Group Name" />

        <div className="create-group-input-fields-flex">
          <select>
            <option value="Classification">Classification</option>
            <option value="Classification">Classification</option>
            <option value="Classification">Classification</option>
            <option value="Classification">Classification</option>
          </select>
          <input type="text" placeholder="Location" />
        </div>

        <input type="text" placeholder="Slogan" />
        <textarea rows="5" placeholder="About"></textarea>
        <div className="create-group-input-fields-flex">
          <input type="text" placeholder="Phone Contact" />
          <input type="email" placeholder="Email Address" />
        </div>
        <input type="text" placeholder="Website/Link" />
        <input type="text" placeholder="Invite Friends" />
        <button className="btn-solid">Create Group</button>
      </div>
    </div>
  );
}
