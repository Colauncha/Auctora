import Slider from "../../Components/Slider";
import AuctionListing from "../Home/AuctionListing";
import Breadcrumbs from "../../Components/Breadcrumbs";
import Pagination from "../../Components/Pagination";
import { useState } from "react";

const ViewAll = () => {
  const [sliderModal, setSliderModal] = useState();
  const toggleModal = () => {
    setSliderModal((prev) => !prev);
  };
  return (
    <div className="formatter">
      <Breadcrumbs />
      <div className="flex flex-col items-center lg:my-10">
        <div className="w-full flex flex-col justify-between lg:flex-row  ">
          <div className="w-full lg:w-[15%] hidden lg:block p-2">
            <Slider />
          </div>
          <div className="w-full lg:w-[70%]">
            <div className="flex items-center justify-between">
              <h1 className="text-start text-[#9f3248] font-[700] text-[28px] py-5">
                Ongoing Auctions
              </h1>
              {sliderModal && (
                <div className="cursor-pointer z-10" onClick={toggleModal}>
                  <Slider />
                </div>
              )}
            </div>
            <AuctionListing />
          </div>
        </div>
        <Pagination />
      </div>
    </div>
  );
};

export default ViewAll;
