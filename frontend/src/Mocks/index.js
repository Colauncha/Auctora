import ps_5 from "../assets/uploads/ps_5.png";
import Nikon from "../assets/uploads/Nikon.png";
import Fride from "../assets/uploads/Fridge.png";
// import AC from "../assets/uploads/Air_conditioner.png";
import Macbook from "../assets/uploads/Macbook20.png";

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
