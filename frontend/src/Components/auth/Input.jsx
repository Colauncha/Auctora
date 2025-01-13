import React from "react";

const Input = ({ title, htmlFor, type, id, className }) => {
  return (
    <div className="flex flex-col">
      <label htmlFor={htmlFor}> {title}</label>
      <input
        type={type}
        id={id}
        required
        className={`border-[1px] rounded-md w-full h-[35px] px-3 ${className}`}
      />
    </div>
  );
};

export default Input;
