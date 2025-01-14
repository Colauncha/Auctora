import React from "react";

const CategoryCard = ({ title, icon, className }) => {
  return (
    <div
      className={`w-[120px] h-[150px] lg:flex place-content-center place-items-center lg:border-[1px] lg:w-[254px] lg:h-[200px] lg:bg-[#faf3f4c3] rounded-[8px] ${className} `}
    >
      <div className="flex flex-col items-center">
        <div className="w-[80px] h-[80px] border-[1px] flex place-items-center place-content-center rounded-full mb-[20px] lg:bg-gradient-to-r from-[#7b2335a4] to-[#9f3248af] text-[#9f3247] lg:text-white">
          <img src={icon} alt="" />
        </div>
        <div className="text-[16px] font-[400] capitalize">{title}</div>
      </div>
    </div>
  );
};

export default CategoryCard;
