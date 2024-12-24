import { productListArr } from "../../Constants";
import Card from "../../Components/Card";
import { useState } from "react";
import Button from "../../Components/Button";
<<<<<<< Updated upstream
=======
import { useNavigate, useLocation } from "react-router-dom";
import useSearchStore from "../../Store/Search";
>>>>>>> Stashed changes

// const buildArr = {

//     imgUrl: String;
//     itemName: String;
//     sellerName: String;
//     bid:Number;
//     bidTimes:Number;
//     price:Number;
//     countDown:Number;
// }
const AuctionListing = () => {
<<<<<<< Updated upstream
  const [visibleCards, setVisibleCards] = useState(4); // Show 4 cards initially

  const isDesktop = window.innerWidth >= 768; // Example breakpoint
=======
  const { searchTerms, category } = useSearchStore();

  const [visibleCards, setVisibleCards] = useState(2);
  const isDesktop = window.innerWidth >= 768;
>>>>>>> Stashed changes

  const loadMore = () => {
    setVisibleCards((prev) => Math.min(prev + 4, productListArr.length));
  };

  const displayedCards = isDesktop
    ? productListArr
    : productListArr.slice(0, visibleCards);
  return (
<<<<<<< Updated upstream
    <div className="mt-10">
      <div className="formatter grid place-items-center grid-cols-2 gap-2 lg:gap-x-4 lg:grid-cols-3 xl:grid-cols-4">
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
=======
    <div className="">
      <div
        className={`grid place-items-center grid-cols-2 gap-2 lg:gap-x-4 lg:grid-cols-3 xl:grid-cols-${cardRows}`}
      >
        {displayedCards
          .filter((product) => {
            const matchesSearchTerm = product.name
              ? product.name.toLowerCase().includes(searchTerms.toLowerCase())
              : false;

            const matchesCategory =
              category === "" || product.category === category;

            return matchesSearchTerm && matchesCategory;
          })
          .map((item, idx) => {
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
>>>>>>> Stashed changes
      </div>
      <div className="formatter flex justify-center">
<<<<<<< Updated upstream
        <div className="w-full mt-5 ">
          <Button
            label={`View All`}
            onClick={loadMore}
            className={`md:w-[200px]`}
          />
=======
        <div className="w-full mt-5 lg:flex lg:justify-center">
          {isHomePath ? (
            <Button
              label={`View All`}
              onClick={viewAll}
              className={`md:w-[200px]`}
            />
          ) : null}
>>>>>>> Stashed changes
        </div>
      </div>
    </div>
  );
};

export default AuctionListing;
