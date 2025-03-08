import React from "react";
import { upload } from "../Constants";

const FileInput = ({ text, className }) => {
  return (
    <div
      className={`${className} flex items-center cursor-pointer justify-center border-[1px] p-3 w-full lg:w-[400px] border-gray-200 rounded-lg bg-gray-50 hover:bg-gray-100`}
    >
      <div className="relative">
        <input type="file" id="file-input" className="hidden" />

        <label htmlFor="file-input" className="cursor-pointer">
          <div className="flex flex-col items-center">
            <img
              src={upload}
              alt="Upload Icon"
              className="w-4 h-4 lg:w-6 lg:h-6 mb-4"
            />
            <span className="text-slate-500 text-[13px]">{text}</span>
          </div>
        </label>
        <p id="file-name" className="mt-2 text-sm text-gray-600"></p>
      </div>
    </div>
  );
};

export default FileInput;
