import Slider from "../../Components/Slider";
import AuctionListing from "../Home/AuctionListing";
import Breadcrumbs from "../../Components/Breadcrumbs";
import Pagination from "../../Components/Pagination";
import { useState } from "react";
import useModeStore from "../../Store/Store";
import { FaAngleDown, FaTimes } from "react-icons/fa";
import { filter_icom } from "../../Constants";
import Modal from "../../Components/Modal";
import Notify from "./Notify";

const Notification = () => {
  const { isMobile } = useModeStore();
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
            <div className="flex items-center justify-end pb-4">
              <h1 className="text-start text-[#9f3248] font-[700] text-[18px] hidden">
                Notifications
              </h1>
              {isMobile ? (
                <img
                  src={filter_icom}
                  onClick={openModal}
                  className="cursor-pointer w-5"
                />
              ) : (
                <div className="flex place-items-center">
                  <FaTimes className="text-[#9f3248] cursor-pointer sm:hidden" />
                </div>
              )}
            </div>
            <Notify />
            <Modal isOpen={modalOpen} onClose={closeModal}>
              <Slider />
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

export default Notification;
