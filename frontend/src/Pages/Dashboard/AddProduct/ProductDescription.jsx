import React from "react";
import BreadCrumb from "../../../Components/Breadcrumbs";
import StepProgress from "../../../Components/StepProgress";
import UploadDetails from "../../../Components/UploadDetails";
import Units from "../../../Components/Units";
import Button from "../../../Components/Button";

const ProductDescription = () => {
  return (
    <>
      <div className="formatter">
        <BreadCrumb />
      </div>
      <div className="bg-slate-50 my-10 py-5">
        <div className="formatter">
          <div className=" bg-white py-10 px-5 rounded-md  shadow-md">
            <div className="w-full flex flex-col gap-2">
              <StepProgress />
              <strong className="text-xl lg:text-lg text-[#9f3247] font-extrabold mb-6">
                Add Product
              </strong>
              <div className="flex flex-col xl:flex-row justify-between gap-4 lg:gap-0">
                <UploadDetails />
                <Units />
              </div>
              <Button label={`Next`} className={`w-[200px]`} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ProductDescription;
