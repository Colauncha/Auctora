import { useState } from "react";
import { FaAngleDown, FaAngleRight, FaAngleUp } from "react-icons/fa";
import Slider from "./Slider"; // Ensure Slider is correctly implemented

const MAX = 50000;
const MIN = 1000;

// PriceRange component
const PriceRange = () => {
  const [open, setOpen] = useState(true);
  const [values, setValues] = useState([MIN, MAX]);

  // Toggles the visibility of the price range slider
  const toggle = () => {
    setOpen((prev) => !prev);
  };

  return (
    <div className="flex flex-col p-4 bg-gray-50 rounded-md shadow-md">
      {/* Header with toggle */}
      <div className="flex justify-between items-center mb-2">
        <h3 className="font-bold text-[#9f3248]">Price</h3>
        <div className="cursor-pointer" onClick={toggle}>
          {open ? (
            <FaAngleUp size={16} color="#9f3248" />
          ) : (
            <FaAngleDown size={16} color="#9f3248" />
          )}
        </div>
      </div>

      {/* Slider Section */}
      {open && (
        <>
          {/* Display selected range */}
          <small className="text-[#9f3248] flex items-center justify-center mb-2">
            <FaAngleRight className="mr-2" />N{values[0].toLocaleString()} - N
            {values[1].toLocaleString()}
          </small>

          {/* Slider component */}
          <div className="mt-4">
            {/* <Slider
              value={values}
              onChange={setValues} // Updates value state on slider move
              min={MIN}
              max={MAX}
            /> */}
          </div>
        </>
      )}
    </div>
  );
};

export default PriceRange;
