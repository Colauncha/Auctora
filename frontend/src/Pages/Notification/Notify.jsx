import React from "react";
import { FaTimes } from "react-icons/fa";
import { useState } from "react";
import { camera, Nikon } from "../../Constants";

const Notify = () => {
  const [activeTab, setActiveTab] = useState("auction");
  const notifications = {
    auction: [
      {
        id: 1,
        image: Nikon,
        name: "Camera",
        price: "Rs.120",
        bids: 3,
        seller: "Seller name",
        timeLeft: "4d 20h",
      },
      {
        id: 2,
        image: camera,
        name: "Painting",
        price: "Rs.120",
        bids: 3,
        seller: "Seller name",
        timeLeft: "4d 20h",
      },
    ],
    inbox: [],
  };
  const handleNotificationClose = () => {
    console.log("closing notification");
  };
  return (
    <div className="bg-[#FFEEF499] rounded-xl shadow-lg">
      <div className="flex justify-between items-center border-b-[1px] p-4">
        <h1 className="text-[16px] lg:text-[28px] font-[700]">Notifications</h1>
        <FaTimes
          className="cursor-pointer font-[100]"
          onClick={handleNotificationClose}
        />
      </div>
      {/* Tabs */}
      <div className="flex mt-3 border-b">
        <button
          className={`flex-1 py-2 font-semibold ${
            activeTab === "auction"
              ? "border-b-2 border-[#9f3248] text-[#9f3248]"
              : "text-gray-500"
          }`}
          onClick={() => setActiveTab("auction")}
        >
          Auction{" "}
          <span className="bg-[#9f3248] text-white px-2 rounded-full text-sm">
            {notifications.auction.length}
          </span>
        </button>
        <button
          className={`flex-1 py-2 font-semibold ${
            activeTab === "inbox"
              ? "border-b-2 border-gray-500 text-gray-500"
              : "text-gray-500"
          }`}
          onClick={() => setActiveTab("inbox")}
        >
          Inbox{" "}
          <span className="bg-gray-500 text-white px-2 rounded-full text-sm">
            {notifications.inbox.length}
          </span>
        </button>
      </div>

      {/* Notification List */}
      <div className="mt-3">
        {notifications[activeTab].length === 0 ? (
          <p className="text-center text-gray-500">No notifications</p>
        ) : (
          notifications[activeTab].map((item) => (
            <div
              key={item.id}
              className="flex items-center p-3 bg-white rounded-lg shadow-sm mb-2"
            >
              <img
                src={item.image}
                alt={item.name}
                className="w-12 h-12 rounded-md"
              />
              <div className="ml-3 flex-1">
                <p className="font-semibold">{item.name}</p>
                <p className="text-red-500">
                  {item.price}{" "}
                  <span className="text-gray-500">{item.bids} bids</span>
                </p>
                <p className="text-xs text-gray-400">(Seller: {item.seller})</p>
                <span className="text-xs bg-red-200 text-red-700 px-2 py-1 rounded mt-1 inline-block">
                  Time left {item.timeLeft}
                </span>
              </div>
              <button className="text-gray-600">▼</button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Notify;
