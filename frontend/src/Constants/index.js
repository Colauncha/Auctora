import search_glass from "../assets/icons/search_glass.png";
import likee from "../assets/icons/likee.png";
import user from "../assets/icons/user.png";
import ps_5 from "../assets/uploads/ps_5.png";
import Nikon from "../assets/uploads/Nikon.png";
import logo from "../assets/icons/Auctora_logo.png";
import Fride from "../assets/uploads/Fridge.png";
import AC from "../assets/uploads/Air_conditioner.png";
import Macbook from "../assets/uploads/Macbook20.png";
import email from "../assets/icons/email_icon.png";
import twitter from "../assets/icons/1.png";
import facebook from "../assets/icons/2.png";
import instaggram from "../assets/icons/3.png";
import github from "../assets/icons/4.png";
import fb_auth from "../assets/icons/fb_auth.png";
import insta_auth from "../assets/icons/insta.png";
import google_auth from "../assets/icons/google_auth.png";
import filter_icom from "../assets/icons/filter_icon.png";
import upload from "../assets/icons/upload.png";

import headphone from "../assets/svg/headphone.svg";
import cellphone from "../assets/svg/phones.svg";
import computer from "../assets/svg/computers.svg";
import camera from "../assets/svg/Camera.svg";
import gamepad from "../assets/svg/gaming.svg";
import smartwatch from "../assets/svg/SmartWatch.svg";

// desktops
import dheadphone from "../assets/svg/dheadphone.svg";
import dphone from "../assets/svg/dphone.svg";
import dcamera from "../assets/svg/dcamera.svg";
import dgaming from "../assets/svg/dgaming.svg";
import dsmartwatch from "../assets/svg/dsmartwatch.svg";
import dcomputer from "../assets/svg/dcomputer.svg";
//shipping services
import shipping from "../assets/svg/shipping.svg";
import delivery from "../assets/svg/delivery.svg";
import category from "../Pages/Home/Category";

// Icons
import WalletHistory from "../assets/svg/WalletHistory.svg";
import FundWallet from "../assets/svg/FundWallet.svg";
import Withdraw from "../assets/svg/Withdraw.svg";
import Logout from "../assets/svg/Logout.svg";
import SettingsIcon from "../assets/svg/SettingsIcon.svg";
import AddIcon from "../assets/svg/AddIcon.svg";
import ActivityIcon from "../assets/svg/ActivityIcon.svg";
import Avatar from "../assets/svg/ProfileIcon.svg";
import Edit from "../assets/svg/Edit.svg";
import Money from "../assets/svg/Money.svg";

export {
  logo,
  search_glass,
  email,
  likee,
  user,
  ps_5,
  Nikon,
  Fride,
  AC,
  Macbook,
  facebook,
  instaggram,
  github,
  twitter,
  fb_auth,
  google_auth,
  insta_auth,
  filter_icom,
  headphone,
  cellphone,
  computer,
  camera,
  gamepad,
  smartwatch,
  dcamera,
  dcomputer,
  dgaming,
  dheadphone,
  dphone,
  dsmartwatch,
  shipping,
  delivery,
  upload,
  category,
  AddIcon,
  ActivityIcon,
  Withdraw,
  WalletHistory,
  FundWallet,
  Logout,
  SettingsIcon,
  Avatar,
  Edit,
  Money,
};

// const buildArr = {

//     imgUrl: String;
//     itemName: String;
//     sellerName: String;
//     bid:Number;
//     bidTimes:Number;
//     price:Number;
//     countDown:Number;
// }

export const productListArr = [
  {
    _id: 1,
    slug: "play-station-5",
    imgUrl: ps_5,
    itemName: "Play Station 5",
    sellerName: "Blessed",
    bid: 4,
    bidTimes: 6,
    price: "5000",
    countDown: "4D: 4H : 23M : 2S",
    description: {
      title: "Play Station 5",
      detail:
        "The PlayStation 5 (PS5) is a home video game console developed by Sony Interactive Entertainment. It was announced as the successor to the PlayStation 4 in April 2019, was launched on November 12, 2020, in Australia, Japan, New Zealand, North America, and South Korea, and was released worldwide a week later. The PS5 is part of the ninth generation of video game consoles, along with Microsoft's Xbox Series X/S consoles, which were released in the same month.",
    },
    review: {
      reviewerName: "kenneth Malida",
      rewiewerImg: ps_5,
      reviewText:
        "Lorem ipsum dolor sit amet consectetur. Augue quis justo amet tristique nibh. Elementum risus sem ultricies sed id. Quam enim sem eu egestas diam sit auctor nunc ultrices. In consectetur urna nibh molestie. Tincidunt dictumst ut pretium cursus urna sodales et. Duis adipiscing laoreet risus malesuada elementum.",
    },
  },
  {
    _id: 2,
    slug: "Nikon-camera",
    imgUrl: Nikon,
    itemName: "Nikon Camera",
    sellerName: "Ayomide",
    bid: 3,
    bidTimes: 6,
    price: "6000",
    countDown: "4D: 4H : 23M : 2S",
  },
  {
    _id: 3,
    slug: "Refrigerator",
    imgUrl: Fride,
    itemName: "Refrigerator",
    sellerName: "Ayomide",
    bid: 3,
    bidTimes: 6,
    price: "60000",
    countDown: "4D: 4H : 23M : 2S",
  },
  {
    _id: 4,
    slug: "Macbook-air",
    imgUrl: Macbook,
    itemName: "Macbook Air 20",
    sellerName: "Ayomide",
    bid: 3,
    bidTimes: 6,
    price: "230000",
    countDown: "4D: 4H : 23M : 2S",
  },
];
