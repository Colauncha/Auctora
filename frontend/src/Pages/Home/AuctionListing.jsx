import { productListArr } from "../../Constants";
import Card from "../../Components/Card";
import { useState } from "react";
import Button from "../../Components/Button";
import { useNavigate, useLocation } from "react-router-dom";
import useModeStore from "../../Store/Store";

const AuctionListing = () => {
  const {isMobile} = useModeStore()
  const [visibleCards, setVisibleCards] = useState(4);
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
  const isHomePath = location.pathname === "/" ? true : false;
  const mobile = '';
  const desktop= 'flex justify-center'
  return (
    <div className={`${isHomePath? `formatter`: ``}`}>
      <div
        className={`${isHomePath? `grid place-items-center grid-cols-2 md:grid-cols-3 lg:grid-cols-4`: `grid place-items-center grid-cols-2 lg:grid-cols-3 space-x-10`}`}
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
              to={`/category/${item.slug}`}
            />
          );
        })}
      </div>
      {/* Button to view all */}
      <div className="formatter">
        
       <div className={`${isMobile ? mobile: desktop }`}>
         { isHomePath?<Button
            label="View All"
            onClick={viewAll}
            className="bg-gradient-to-r from-[#7B2334] to-[#9F3247] w-full lg:w-[200px]"
          />: null}
       </div>
      </div>
    </div>
  );
};

export default AuctionListing;
