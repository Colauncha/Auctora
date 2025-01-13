import React from "react";

const AuthNote = ({ heading, body, button }) => {
  return (
    <div className="w-[620px] h-[500px]  bg-gradient-to-r from-[#7B2334] to-[#9F3247] rounded-tr-md rounded-br-md flex place-content-center place-items-center flex-col p-10 gap-4">
      <h3 className="font-[700] text-[30px] text-white">{heading}</h3>
      <p className="text-center text-[13px] text-white w-[500px]">{body}</p>
      <div>{button}</div>
    </div>
  );
};

export default AuthNote;
