import { productListArr } from "../../Constants";
import Card from "../../Components/Card";
import { useState } from "react";
import Button from "../../Components/Button";
import { useNavigate, useLocation } from "react-router-dom";

const AuctionListing = () => {
  const [visibleCards, setVisibleCards] = useState(2);
  const isDesktop = window.innerWidth >= 768;

  const loadMore = () => {
    setVisibleCards((prev) => Math.min(prev + 4, productListArr.length));
  };

  const displayedCards = isDesktop
    ? productListArr
    : productListArr.slice(0, visibleCards);

  const navigate = useNavigate();
  const viewAll = () => {
    navigate("/Ongoing-Auction");
  };

  const location = useLocation();
  const cardRows = location.pathname === "/" ? 4 : 4;
  const isHomePath = location.pathname === "/" ? true : false;

  return (
    <div className="">
      <div
        className={`grid place-items-center grid-cols-2 gap-2 lg:gap-x-4 lg:grid-cols-3 xl:grid-cols-${cardRows}`}
      >
        {displayedCards.map((item, idx) => {
          return (
            <Card
              key={idx}
              imgUrl={item.imgUrl}
              itemName={item.itemName}
              bid={item.bid}
              bidTimes={item.bidTimes}
              sellerName={item.sellerName}
              price={item.price}
              countDown={item.countDown}
            />
          );
        })}
      </div>
      {/* Button to view all */}
      <div className="formatter flex justify-center">
        <div className="w-full mt-5 ">
          {isHomePath ? (
            <Button
              label={`View All`}
              onClick={viewAll}
              className={`md:w-[200px]`}
            />
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default AuctionListing;
