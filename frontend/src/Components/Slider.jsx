import { filter_icom } from "../Constants";
import Button from "./Button";
import PriceRange from "./PriceRange";

const Slider = ({ className }) => {
  const filter = () => {
    console.log("filter");
  };
  return (
    <div
      className={`border-[1px] w-[19rem] h-[24rem] rounded-md py-4 px-6 ${className}`}
    >
      <div className="flex justify-between">
        <h3 className="font-[700] text-[#9f3248]">Filter</h3>
        <img src={filter_icom} className="cursor-pointer" onClick={filter} />
      </div>
      <span className="w-full h-[30px] border-t-[1px] border-b-[1px] my-4 block"></span>
      <div className="my-10">
        <PriceRange />
      </div>
      <span className="w-full h-[30px] border-t-[1px] border-b-[1px] my-4 block"></span>
      {/* <span className="w-full h-[15px]  border-b-[1px] mb-4 block"></span> */}
      <Button label="Apply Filter" className="w-full" />
    </div>
  );
};

export default Slider;
