import React from "react";

const Stopwatch = ({ days, hours, minutes, seconds }) => {
  return (
    <div className="w-[320px] h-[40px] flex items-center justify-between">
      <div className="w-12 h-12 bg-black rounded-[50%] text-white text-[14px] ">
        <div className="flex flex-col place-items-center pt-2 ">
          <span>{days}</span>
          <span className="text-[8px]">Days</span>
        </div>
      </div>
      <div className="w-12 h-12 bg-black rounded-[50%] text-white text-[14px] ">
        <div className="flex flex-col place-items-center pt-2 ">
          <span>{hours}</span>
          <span className="text-[8px]">Hours</span>
        </div>
      </div>
      <div className="w-12 h-12 bg-black rounded-[50%] text-white text-[14px] ">
        <div className="flex flex-col place-items-center pt-2 ">
          <span>{minutes}</span>
          <span className="text-[8px]">Minutes</span>
        </div>
      </div>
      <div className="w-12 h-12 bg-black rounded-[50%] text-white text-[14px] ">
        <div className="flex flex-col place-items-center pt-2">
          <span>{seconds}</span>
          <span className="text-[8px]">Seconds</span>
        </div>
      </div>
    </div>
  );
};

export default Stopwatch;
