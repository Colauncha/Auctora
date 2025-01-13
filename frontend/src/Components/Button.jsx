import React from "react";

const Button = ({ label, className, onClick }) => {
  return (
    <div>
      <button
        className={`bg-[#9F3247] text-white px-4 w-full h-[42px] rounded-[62px] ${className}`}
        onClick={onClick}
      >
        {label}
      </button>
    </div>
  );
};

export default Button;
