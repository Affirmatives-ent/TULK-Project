import React from "react";

// styles
import "./messenger.css";

// components
import MessengerItem from "../../components/MessengerItem/MessengerItem";

export default function Messenger() {
  return (
    <div className="messenger">
      <MessengerItem />
      <MessengerItem />
      <MessengerItem />
      <MessengerItem />
      <MessengerItem />
      <MessengerItem />
      <MessengerItem />
      <MessengerItem />
      <MessengerItem />
      <MessengerItem />
    </div>
  );
}
