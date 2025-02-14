import React from "react";
import Input from "./auth/Input";
import TextFieldMore from "./TextFieldMore";
import Button from "./Button";

const UploadDetails = () => {
  return (
    // title, htmlFor, type, id, className, placeholder
    <div className="flex flex-col gap-4">
      <Input
        placeholder={`item Name`}
        className={`w-full lg:w-[810px]`}
        title={`Product Name`}
        htmlFor={`name`}
        id={`product-name`}
      />
      <TextFieldMore
        placeholder={`"Enter the description here"`}
        label={`Description`}
        className={`lg:w-[810px] lg:h-[210px]`}
      />
    </div>
  );
};

export default UploadDetails;
