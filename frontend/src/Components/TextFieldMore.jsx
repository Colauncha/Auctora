import React from "react";

const TextFieldMore = ({ value, label, className, placeholder }) => {
  return (
    <div className="flex flex-col">
      <p className="text-slate-500">{label}</p>
      <textarea
        name="address"
        value={value}
        className={`w-full p-2 border rounded focus:outline-[#9f3247] bg-gray-50 ${className} `}
        placeholder={placeholder}
      ></textarea>
    </div>
  );
};

export default TextFieldMore;
