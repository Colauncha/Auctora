import Slider from "../../Components/Slider";
import AuctionListing from "../Home/AuctionListing";
import Breadcrumbs from "../../Components/Breadcrumbs";
import Pagination from "../../Components/Pagination";
import { useState } from "react";
import { FaAngleDown } from "react-icons/fa";

const ViewAll = () => {
  const [sliderModal, setSliderModal] = useState();
  const toggleModal = () => {
    setSliderModal((prev) => !prev);
  };

  const select = ()=>{
    console.log("open sought");
    
  }
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
              <h1 className="text-start text-[#9f3248] font-[700] text-[28px] pb-5">
                Ongoing Auctions
              </h1>
              <div className="flex place-items-center">
                <div className="text-slate-400 text-sm">
                  Sorted by
                </div>: 
                  <span className="font-bold pl-2 text-sm flex gap-1 place-items-center cursor-pointer" onClick={select}>Most Popular <FaAngleDown /></span>
              </div>
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
