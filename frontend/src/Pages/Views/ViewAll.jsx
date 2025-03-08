import Slider from "../../Components/Slider";
import AuctionListing from "../Home/AuctionListing";
import Breadcrumbs from "../../Components/Breadcrumbs";
import Pagination from "../../Components/Pagination";
import { useState } from "react";
import useModeStore from "../../Store/Store";
import { FaAngleDown } from "react-icons/fa";
import { filter_icom } from "../../Constants";
import Modal from "../../Components/Modal";




const ViewAll = () => {
  const {isMobile} = useModeStore()
  const [modalOpen, setModalOpen] = useState(false);
  const openModal = () => setModalOpen(true);
  const closeModal = () => setModalOpen(false);
  // pagination
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = 10; // Set the total number of pages

  const handlePageChange = (page) => {
    setCurrentPage(page);
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
            <div className="flex items-center justify-between pb-4">
             <h1 className="text-start text-[#9f3248] font-[700] text-[28px]">
                Ongoing Auctions
              </h1>
              {isMobile? <img src={filter_icom} onClick={openModal} className="cursor-pointer"/>
              :<div className="flex place-items-center">
                <div className="text-slate-400 text-sm">
                  Sorted by
                </div>: 
                  <span className="font-bold pl-2 text-sm flex gap-1 place-items-center cursor-pointer">Most Popular <FaAngleDown /></span>
              </div>}
            </div>
            <AuctionListing />
              <Modal isOpen={modalOpen} onClose={closeModal}>
                <Slider/>
              </Modal>
          </div>
        </div>
        <>
        <Pagination
        totalPages={totalPages}
        currentPage={currentPage}
        onPageChange={handlePageChange}
      />
        </>
      </div>
    </div>
  );
};

export default ViewAll;
